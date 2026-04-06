# Music-Code

Music-Code is a Python toolkit for making music with code. It combines simple synthesis, chord and sequence generation, sample playback, basic DSP, waveform inspection, and WAV export in a single local project.

The repository includes the core library, bundled musical lookup data, sample libraries, notebooks, and example output. You can use it to sketch beats, build layered arrangements, experiment with timbre, or generate audio programmatically for larger workflows.

## Core Idea

Music-Code revolves around two classes:

- `MusicCode`: creates musical material at a given BPM
- `Wave`: represents audio and provides editing, analysis, and export methods

The usual workflow is:

1. Create a `MusicCode` object.
2. Generate audio with notes, chords, arpeggios, sequences, rests, or samples.
3. Combine sounds with `join_waves()` for arrangement and `add_waves()` for layering.
4. Shape the result with `Wave` methods like `fade()`, `pan()`, `LPF()`, `HPF()`, `LFO()`, `delay()`, or `time_edit()`.
5. Export the final result with `bounce()`.

## Repository Layout

- `core/music_code.py`: main library module
- `data/`: chord definitions and note-to-frequency lookup data
- `samples/`: built-in WAV sample library
- `export/`: rendered WAV files
- `images/`: saved waveform artwork examples
- `songs/song_1.py`: example composition script
- `tests/tests.py`: smoke-style regression script
- `notebooks/tutorials/`: tutorial notebooks
- `notebooks/visualize/`: visualization notebooks

The library resolves its data, sample, image, and export paths relative to the repository, so the folder structure should stay intact.

## Setup

The project does not currently ship with packaging metadata or a lockfile, so install the runtime dependencies in your Python environment directly.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install numpy pandas matplotlib scipy scikit-learn soundfile ipython seaborn
```

Music-Code was smoke-tested here with `python3` 3.8.13.

## Quick Start

Render the example song:

```bash
python3 songs/song_1.py
```

Run the smoke test script:

```bash
python3 tests/tests.py
```

Rendered audio is written to `export/`.

## Minimal Example

```python
from pathlib import Path
import sys

sys.path.insert(0, str(Path("core").resolve()))

from music_code import MusicCode

m = MusicCode(120)

kick = m.sample("kick", "kick_06.wav").time_edit(1 / 8)
snare = m.sample("snare", "snare_04.wav").time_edit(1 / 8)

drums = m.add_waves(
    (
        m.join_waves((kick, m.rest(1 / 8), kick, m.rest(1 / 8))),
        m.join_waves((m.rest(1 / 4), snare, m.rest(1 / 4))),
    )
)

pad = m.chord("min 9", "D3", "sine-tri", duration=1).fade(fade_in=1 / 16, fade_out=1 / 16)
bass = m.sequence(["D2", "D2", "A1", "C2"], "square", rhythm=1 / 4, duration=1).LPF(180)

song = m.add_waves((drums, pad, bass)).vol(0.8)
song.bounce("demo.wav", show_visual=False)
```

## How Timing Works

- `MusicCode` defaults to `relative` time mode.
- In relative mode, durations are measured in bars relative to BPM.
- For example, `1 / 4` means a quarter of a bar, `1` means one full bar, and `4` means four bars.
- You can switch to absolute timing by setting `m.time_mode = "absolute"`, in which case durations are interpreted as seconds.

The engine uses a sample rate of `44100` Hz.

## What `MusicCode` Builds

The main creation methods are:

- `create_wave(note_labels, wave_type, duration, wt_pos=1)`
- `sequence(note_labels, wave_type, rhythm, duration, ...)`
- `rest(duration)`
- `chord(chord_label, start_note, wave_type, duration, ...)`
- `arpeggio(chord_label, start_note, wave_type, rhythm, duration, ...)`
- `join_waves(waves_tuple)`
- `add_waves(waves_tuple)`
- `sample(sound_folder, sample_id)`

Notes can be passed as note names like `"C3"` or `"F#4"`, or as raw frequencies in Hz.

Available waveform types include:

- `sine`
- `tri`
- `saw1`
- `saw2`
- `square`
- blended forms such as `sine-tri`, `sine-saw`, `sine-square`, `saw-square`, `tri-saw`, and `tri-square`

## What `Wave` Does

`Wave` is a subclass of `numpy.ndarray`, so audio is represented directly as sample data while still exposing music-focused helper methods.

Common `Wave` methods include:

- `vol()`
- `time()`
- `bounce()`
- `view()`
- `time_edit()`
- `loop()`
- `reverse()`
- `pan()`
- `fade()`
- `LPF()`
- `HPF()`
- `LFO()`
- `delay()`

These methods are chainable because they return new `Wave` objects.

## Arrangement And Mixing

- `join_waves()` places sounds back-to-back to build a sequence or song structure.
- `add_waves()` mixes sounds together to create harmony, layered drums, stereo stacks, or combined textures.
- If stereo and mono waves are mixed together, mono sources are expanded to stereo automatically.
- When `add_waves()` combines different lengths, it trims to the shortest input.

## Samples

The bundled sample folders are:

- `kick`
- `snare`
- `clap`
- `hihat`
- `perc`
- `cymbal`
- `bass`
- `fx`
- `user`

Use `sample(sound_folder, sample_id)` with either:

- an integer index to select from the sorted folder contents
- a file name string to load a specific WAV

The special folder name `archive` loads previously exported files from `export/`.

## Export And Visualization

- `bounce()` writes WAV files to `export/`
- if a file name already exists, Music-Code automatically increments the name
- `view()` can show waveform, spectrum, and spectrogram plots

If you are running in a headless environment, `MPLBACKEND=Agg` can help with Matplotlib output.

## Included Content

- chord and interval data in `data/`
- note-to-frequency mappings in `data/`
- a built-in sample library in `samples/`
- example renders in `export/`
- waveform image examples in `images/`
- tutorial and visualization notebooks in `notebooks/`

## Where To Start

- Read `songs/song_1.py` for a complete example arrangement
- Read `core/music_code.py` for the full API
- Run `tests/tests.py` for a broad smoke pass across the synthesis and effect methods

## Contact

For questions about the project, email wesleylaurencetech@gmail.com.
