# Music-Code Refactor Plan

## Goal

Rebuild Music-Code from first principles as a modular, composable audio framework that is easy for humans to learn and easy for coding agents to navigate. The target is not API compatibility with the current monolith. The target is a cleaner system with explicit concepts, stable verbs, predictable behavior, and a package layout that matches how audio software is actually composed.

## What The Current Code Is Telling Us

The note in `docs/notes.md` is directionally right, and the current implementation makes the case even more strongly:

- `core/music_code.py` combines transport, note lookup, chord logic, sample loading, synthesis, sequencing, mixing, plotting, and export in one file.
- `MusicCode` is both environment/config object and feature bucket.
- `Wave` is both array container and the home for editing, file output, plotting, and effect processing.
- The current design reloads data and re-creates heavy objects too often.
- Time logic is spread across methods and controlled by mutable state (`time_mode`) instead of explicit time values.
- Combining audio has implicit behavior like auto-normalization and auto-upmixing, which makes results hard to predict.
- Sample loading is hard-coded with folder-specific conditionals.
- Core runtime code imports notebook/display/plotting concerns directly.
- The tests are mostly smoke checks for “does not crash”, not behavioral contracts for timing, channel rules, or DSP correctness.

That means the refactor should not be a file split of the existing code. It should be a redesign around a few durable primitives.

## Architectural Decisions

### 1. Keep the import name, replace the shape

Use `core/music_code/` as a real package and retire `core/music_code.py` after the rewrite lands. This preserves the useful package name while allowing the internal structure to change completely.

Why this shape:

- It fits the current repo layout and example import style.
- It avoids inventing a second public identity for the project.
- It gives a clean boundary for modularization without pretending the old module can be maintained incrementally forever.

### 2. Use composition, not `numpy.ndarray` subclassing

Replace `Wave(np.ndarray)` with a small buffer object, for example `AudioBuffer`, that wraps a `numpy.ndarray` plus metadata.

Recommended fields:

- `samples: np.ndarray`
- `sample_rate: int`
- `channels: int`
- `metadata: dict[str, Any]`

Why:

- `ndarray` subclassing makes behavior hard to reason about and easy to break.
- A wrapper object is clearer for humans and more predictable for agents.
- It becomes straightforward to separate storage, DSP, I/O, and visualization.
- Type hints and tests are much simpler.

The wrapped array should still be plain NumPy under the hood. The refactor is about public shape and responsibility boundaries, not abandoning efficient arrays.

### 3. Remove mutable global time mode from the core API

Do not keep `self.time_mode = "relative" | "absolute"` as a hidden switch. Replace it with explicit time values.

Recommended time model:

- `Transport(bpm=120, sample_rate=44100, beats_per_bar=4, beat_unit=4)`
- `bars(x)`, `beats(x)`, `seconds(x)` helper constructors
- `TimeValue` or `Duration` objects that the transport resolves to sample counts

Why:

- It removes one of the biggest sources of implicit behavior in the current code.
- It makes APIs self-documenting.
- It allows relative and absolute durations to coexist safely in one program.
- It gives sequencing, fades, delays, and clip edits one shared source of truth.

### 4. Make mixing semantics explicit and non-magical

The new core should never silently normalize or “make louder until threshold” inside basic combine operations.

Recommended rules:

- `concat([...])` means join in time.
- `mix([...], align="shortest" | "longest", upmix=True)` means layer in parallel.
- `normalize(buffer, peak=0.95)` is explicit.
- `gain(buffer, db=...)` or `gain(buffer, factor=...)` is explicit.
- Stereo expansion rules are documented and deterministic.

Why:

- Auto-normalization inside `add_waves` makes gain staging unpredictable.
- Concatenate vs layer is a core mental model and should stay obvious.
- Explicit behavior is better for both composition and testing.

### 5. Separate core DSP from I/O and visualization

Plotting and playback helpers should not live in the same layer as synthesis and transforms.

Recommended split:

- Core package: transport, buffers, sequencing, synth, sampler, effects, mix.
- Optional I/O layer: read/write WAV.
- Optional visualization layer: waveform, spectrum, spectrogram.

That means `matplotlib` and `IPython.display` should not be required imports for core rendering.

### 6. Prefer stateless processors first, stateful processors only when needed

For the first refactor pass:

- Filters, gain, fade, pan, and trim/stretch logic should be plain functions or thin processor objects.
- Delay can be implemented as a processor object if that keeps the interface clearer.
- Reverb, compression, automation, and modular routing should wait until the buffer and transport model are stable.

This keeps the first framework version small and coherent.

## Target Package Layout

Recommended structure:

```text
core/
  music_code/
    __init__.py
    facade.py
    transport.py
    buffer.py
    errors.py
    io.py
    viz.py
    mix.py
    dsp/
      __init__.py
      envelopes.py
      filters.py
      windows.py
      utils.py
    theory/
      __init__.py
      notes.py
      chords.py
    synth/
      __init__.py
      oscillators.py
      voice.py
      presets.py
    sampler/
      __init__.py
      library.py
      player.py
    sequencing/
      __init__.py
      events.py
      pattern.py
      render.py
    effects/
      __init__.py
      gain.py
      pan.py
      fade.py
      filters.py
      delay.py
      chain.py
```

Responsibility split:

- `buffer.py`: `AudioBuffer`, channel helpers, duration helpers, shape validation.
- `transport.py`: BPM, bar/beat math, conversion to samples.
- `theory/notes.py`: note-to-frequency and frequency helpers.
- `theory/chords.py`: chord blueprint loading and interval lookup.
- `sampler/library.py`: sample folder indexing, archive loading, lookup rules.
- `sampler/player.py`: turning loaded files into playable buffers/clips.
- `synth/oscillators.py`: sine, triangle, saw, square, blend helpers.
- `synth/voice.py`: note rendering, chord rendering, arpeggio rendering, ADSR.
- `sequencing/events.py`: note events, audio events, rests, clip placement.
- `sequencing/pattern.py`: step and pattern utilities.
- `sequencing/render.py`: render patterns/events into buffers.
- `effects/*`: self-contained processors operating on `AudioBuffer`.
- `mix.py`: `concat`, `mix`, channel conversion, normalization, master utilities.
- `io.py`: `read_wav`, `write_wav`, export naming.
- `viz.py`: optional plotting only.
- `facade.py`: optional high-level API for quick workflows.

## Core Primitives

These should be the concepts the whole refactor orients around.

### `Transport`

This becomes the timing authority.

Suggested API:

```python
transport = Transport(bpm=94, sample_rate=44100)
transport.samples(bars(1/4))
transport.samples(seconds(0.5))
```

Responsibilities:

- convert time specs to samples
- hold BPM and sample rate
- later support swing or meter without contaminating unrelated modules

### `AudioBuffer`

This is the fundamental audio value.

Suggested API:

```python
buffer.duration_seconds
buffer.is_stereo
buffer.to_stereo()
buffer.to_mono()
```

Rules:

- buffer operations return new buffers
- metadata is lightweight and optional
- no plotting or file export methods on the buffer itself

### Events and Patterns

Do not hard-code sequencing into synth methods only. Sequencing should be its own layer.

Suggested concepts:

- `NoteEvent(pitch, start, duration, velocity=1.0)`
- `AudioEvent(buffer, start, gain=1.0, pan=0.0)`
- `Pattern(step=bars(1/16), length=bars(1), events=[...])`

This gives a reusable path for synth phrases, drum patterns, sample chops, and future automation.

### Processor / Chain

Effects need a shared shape early.

Suggested interface:

```python
processed = Chain(
    high_pass(300),
    fade(in_time=bars(1/32), out_time=bars(1/32)),
    delay(time=bars(1/8), feedback=4, mix=0.25),
).apply(buffer, transport)
```

This is enough for a DAW-like mental model without introducing a full plugin graph.

## Public API Direction

The public surface should use stable verbs that map directly to user intent:

- `load`
- `play`
- `render`
- `mix`
- `concat`
- `chain`
- `bounce`

One viable high-level facade:

```python
from music_code import (
    Transport,
    Sampler,
    Synth,
    Pattern,
    bars,
    mix,
    concat,
    bounce,
)

transport = Transport(bpm=94)
sampler = Sampler(root="samples")
synth = Synth(transport)

kick = sampler.load("kick", "kick_06.wav")
kick_step = kick.trim(bars(1/16), transport)

bass = synth.sequence(
    notes=["D2", "D2", "A1", "C2"],
    oscillator="sine",
    step=bars(1/4),
    length=bars(1),
)

song = concat([
    mix([...]),
    mix([...]),
])

bounce(song, "export/song.wav")
```

The facade should stay thin. The important thing is that each concept also exists below the facade in a focused module.

## What Should Not Survive The Rewrite

- hidden `time_mode` state
- `Wave` as an `ndarray` subclass
- broad `except:` blocks
- print-based return behavior like `time()`
- folder-specific sample logic implemented as long `if/elif` chains
- core methods that also plot, display, or write files
- combine functions that change gain implicitly
- repeated CSV and sample-index loading on hot paths
- helper methods that instantiate fresh `MusicCode(...)` objects internally

## Refactor Phases

### Phase 0: Freeze behavior worth keeping

Before moving code, define what the new system must preserve conceptually:

- 44.1 kHz default sample rate
- clear bar/beat vs second timing behavior
- deterministic concat and mix rules
- note and chord lookup from `data/`
- sample library loading from repo-local folders

Deliverables:

- architecture note approved in `docs/refactor.md`
- a small list of canonical behaviors to test in the new API
- decision to stop extending `core/music_code.py`

### Phase 1: Package skeleton and foundational types

Build:

- `core/music_code/`
- `Transport`
- `AudioBuffer`
- `errors.py`
- `io.py`

Acceptance criteria:

- buffers can be created from mono/stereo arrays
- transport converts bars/beats/seconds to sample counts correctly
- WAV read/write works without importing plotting code

### Phase 2: Theory and data access

Build:

- `theory/notes.py`
- `theory/chords.py`
- data loaders with caching

Acceptance criteria:

- note name to frequency mapping is isolated and tested
- chord definitions load once and resolve correctly
- data access is no longer tied to `MusicCode.__init__`

### Phase 3: Sampler subsystem

Build:

- `SampleLibrary`
- sample indexing by folder and filename
- archive loading through the same library abstraction

Acceptance criteria:

- folder lookup is table-driven, not an `if/elif` ladder
- integer index and exact filename lookup both work
- errors are explicit when samples are missing

### Phase 4: Synth MVP

Build:

- oscillator functions
- a small `Synth` or `Voice` API
- ADSR or basic envelope support
- chord and arpeggio rendering on top of theory + transport

Acceptance criteria:

- single note rendering is deterministic
- chord and arpeggio rendering do not depend on sequencer internals being monolithic
- waveform generation does not require any global mutable state

### Phase 5: Mix and edit primitives

Build:

- `concat`
- `mix`
- `gain`
- `pan`
- `trim`
- `loop`
- `reverse`
- `fade`
- `normalize`

Acceptance criteria:

- mono/stereo rules are documented and tested
- no implicit normalization occurs during basic combine operations
- edits return new buffers cleanly

### Phase 6: Sequencing layer

Build:

- note events
- audio clip events
- rests
- step-pattern helpers
- renderers that turn patterns into buffers

Acceptance criteria:

- drum programming and melodic sequencing use the same timing model
- a pattern can target either samples or synth notes
- sequence logic is no longer buried inside one synth helper

### Phase 7: Effects and chains

Build:

- low-pass filter
- high-pass filter
- delay
- LFO/modulation helpers
- serial chain utility

Acceptance criteria:

- processors share one input/output contract
- core DSP does not depend on notebook display code
- delay and modulation have explicit time semantics

### Phase 8: Facade, examples, and docs

Build:

- thin `facade.py`
- rewrite `songs/` examples against the new API
- add short concept docs and recipe docs

Acceptance criteria:

- top-level docs define each core concept in one sentence
- examples demonstrate one subsystem each
- the facade is optional, not a second monolith

### Phase 9: Replace tests and retire the monolith

Build:

- new behavioral test suite
- one short integration render
- remove or archive `core/music_code.py`

Acceptance criteria:

- tests validate timing, channels, file I/O, sample lookup, and effect invariants
- old file is no longer the source of truth
- repo docs point only to the new package structure

## Testing Strategy

The current smoke-test script should be replaced by focused behavioral tests. The important contracts are:

- bars/beats/seconds convert to exact sample counts
- note names resolve predictably
- chord intervals map correctly
- sample lookup works by name and by index
- concat preserves order and length
- mix obeys documented trimming/alignment rules
- mono-to-stereo expansion is deterministic
- filters and fades preserve expected shapes and dimensions
- export writes files where expected without requiring interactive display

One integration test should render a short musical phrase using samples plus synth plus one effect chain and verify:

- output shape
- output duration
- no NaNs
- peak stays within a chosen ceiling unless explicitly allowed

## Documentation Strategy

Docs should be treated as part of the framework design, not as cleanup after the code lands.

Recommended docs:

- `docs/concepts.md`: one sentence per concept
- `docs/recipes.md`: intent to API mapping
- `songs/`: examples as executable contracts

Each example should answer one question:

- how to load and trim a sample
- how to sequence drum hits
- how to synthesize a bass line
- how to build a simple chain
- how to mix and bounce a track

This is especially important for agent use. Agents need obvious nouns and verbs plus a small number of canonical examples.

## Non-Goals For The First Rewrite

Do not try to build all of this in v1:

- full modular patch graph
- automation lanes
- compression, limiting, and mastering suite
- plugin marketplace shape
- real-time playback engine
- backward-compatible adapter for the old API

Those should come after the core package shape proves itself.

## Recommended Execution Order

If this were implemented now, the order should be:

1. package skeleton, transport, buffer, and I/O
2. theory loaders and caches
3. sampler
4. synth MVP
5. mix/edit primitives
6. sequencing
7. effects/chains
8. examples and docs
9. monolith removal

This order minimizes rework because sequencing and effects depend on transport and buffer semantics being settled first.

## Definition Of Done

The refactor is done when:

- `core/music_code.py` is no longer the implementation center
- the new package has small modules with single responsibilities
- time is explicit, not hidden in mutable mode switches
- buffers are plain wrapped arrays, not `ndarray` subclasses
- synth, sampler, sequencing, effects, and mixing can be used independently
- examples and tests reflect the new model rather than preserving the old one
- a human or an agent can discover the right tool by concept name and follow a short example to use it

That is the version of Music-Code that can grow into a real framework instead of a larger monolith.
