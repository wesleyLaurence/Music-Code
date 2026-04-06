# Music-Code: refactor and framework notes

## Vision

- **Music-Code** should be a **flexible, modular, plug-and-play** Python system for composing with code.
- **Primary audience:** humans *and* coding agents that need to **discover, compose with, and chain** building blocks like in a DAW.
- **Stretch:** agent skills (or similar) for **how to use tools**, creative prompts, and methodology—not only API docs.

## Current state

- **Bulk of behavior** lives in `core/music_code.py` (single large module / one main class carrying most functionality).
- **Pain:** hard to navigate, reuse, and extend; not a sustainable shape for a framework.

## Refactor goals (first principles)

- **Readable:** small, named units with obvious responsibilities.
- **Reusable:** sampler, synth, effects, and sequencing should be **composable**, not buried in one type.
- **Efficient:** structure for clarity first; optimize hot paths where measurement says it matters.
- **Agent-friendly:** predictable names, thin public surfaces, and docs that map **intent → API** (e.g. “sidechain compression” → the right calls).

**Not a constraint:** **backward compatibility with current `songs/` (or the old monolithic API) is not required.** The point is a first-principles redesign; breaking changes and rewriting examples are fine. Update tests to match the new design rather than preserving legacy call shapes.

## Suggested module boundaries

| Area | Role |
|------|------|
| **Waveform / buffer** | Core audio array type, I/O, metadata (channels, sample rate). |
| **Timeline / time** | BPM, bar/beat vs seconds, duration math. |
| **Sequencer** | Ordering events: `sequence`, rests, patterns. |
| **Sampler** | Load/play audio files, indexing, folders. |
| **Synthesizer** | Oscillators, envelopes, modulation; ideally **programmable / modular** for richer patterns. |
| **Effects** | Per-unit processors: delay, filters, etc. |
| **Effects chains** | Ordered graphs: serial/parallel, wet/dry, automation hooks later. |
| **Mix / master** | Levels, pan, sum buses, (later) limiting, compression, EQ. |
| **Signal processing** | Shared DSP primitives effects and synth both use. |

Optional **facade** (e.g. `MusicCode`) that delegates to these packages for a simple default workflow—shape it for the new API, not for mirroring the old one.

## Core primitives to name explicitly

- **Time:** relative (bars) vs absolute (seconds); alignment to grid.
- **Transport:** BPM, (optional) swing, meter.
- **Sources:** samples vs generated waveforms.
- **Streams:** mono/stereo, length, trimming rules when combining.
- **Combination:** concatenate vs mix (`join` vs `add`), gain staging.
- **Processing:** stateless vs stateful (e.g. delay line).
- **Output:** bounce/export, normalization, peak safety.

## DAW-parity tool checklist (aspirational)

**Already in scope:** volume, pan, mix, delay, filters, LFO-ish modulation.

**Often added for a fuller DAW feel:** reverb, saturation/overdrive, EQ, compression, limiting, (simple) automation, sends/returns, basic mastering chain.

Treat this as a **roadmap**: implement shared abstractions first, then hang specific effects on them.

## Synth direction

- Start with a **small fixed synth** (few oscillators + ADSR) behind a stable API.
- Evolve toward **modular / patchable** synthesis only when the buffer + time + parameter model is solid.

## Making it intuitive for people and agents

- **One sentence per concept** in top-level docs: “A `Wave` is…”, “Sequencing means…”.
- **Stable verbs:** `load`, `play`, `mix`, `chain`, `bounce`—match mental models from DAWs.
- **Examples as contracts:** `songs/` entries that each demonstrate one subsystem.
- **Skills / guides:** recipes (“four-on-the-floor + sidechain feel”) that point to real function names.

## Open questions

- **Import graph:** avoid circular deps (e.g. effects depending on high-level `MusicCode`).
- **Plugin shape:** pure functions on arrays vs objects with state (delays, reverbs).

## One-line goal

The goal is an **easy-to-learn surface for humans** and a **predictable, composable API for agents**.
