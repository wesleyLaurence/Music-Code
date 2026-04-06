# AGENTS.md

## Purpose

Music-Code is a local Python audio engine for composing, sampling, editing, and exporting music with code. Most of the implementation lives in one module, `core/music_code.py`, backed by repo-local data and sample folders.

Use this file as a working guide when you need to understand the codebase quickly or make changes safely.

## First Files To Read

- `core/music_code.py`
- `songs/song_1.py`
- `tests/tests.py`
- `data/chords_blueprint.csv`
- `data/frequency_musical notes.csv`

## Main Mental Model

- `MusicCode` creates sound material at a chosen BPM.
- `Wave` stores audio as a `numpy.ndarray` subclass and adds editing/export methods.
- Most tasks follow the same pattern: generate sources with `MusicCode`, transform them with `Wave`, combine them with `join_waves` or `add_waves`, then export with `bounce`.

## Key API Surface

Creation methods on `MusicCode`:

- `create_wave`
- `sequence`
- `rest`
- `chord`
- `arpeggio`
- `join_waves`
- `add_waves`
- `sample`

Editing and output methods on `Wave`:

- `vol`
- `time`
- `bounce`
- `view`
- `time_edit`
- `loop`
- `reverse`
- `pan`
- `fade`
- `LPF`
- `HPF`
- `LFO`
- `delay`

## Timing Model

- Default timing mode is `relative`.
- In relative mode, durations are measured in bars relative to `bpm`.
- In absolute mode, durations are measured in seconds.
- Sample rate is `44100`.

This matters everywhere: synthesis, sequencing, fades, delays, and time edits all depend on the active time mode.

## Combination Rules

- `join_waves(waves_tuple)` concatenates audio in time.
- `add_waves(waves_tuple)` mixes audio together.
- `add_waves` trims to the shortest input length.
- Mixing mono with stereo auto-expands mono to stereo.

When behavior looks wrong, check whether the issue is sequencing vs layering first.

## Notes, Chords, And Samples

- Notes can be passed as note names like `C3`, `Bb2`, or `F#4`, or as raw frequencies.
- Chord names come from `data/chords_blueprint.csv`.
- Frequency lookup comes from `data/frequency_musical notes.csv`.
- Sample folders are `kick`, `snare`, `clap`, `hihat`, `perc`, `cymbal`, `bass`, `fx`, `user`.
- `sample(sound_folder, sample_id)` accepts either a sorted integer index or an exact file name.
- `sample("archive", ...)` reads from `export/`.

## Repository Layout

- `core/`: main library code
- `data/`: CSV lookup data
- `samples/`: bundled WAV libraries
- `songs/`: composition scripts
- `tests/`: smoke test script
- `export/`: rendered WAV output
- `images/`: saved image output
- `notebooks/`: tutorials and visualization experiments

The code expects these folders to exist at the repo root.

## Useful Commands

Render the example song:

```bash
python3 songs/song_1.py
```

Run the smoke tests:

```bash
python3 tests/tests.py
```

Quick import smoke check:

```bash
python3 -c 'from pathlib import Path; import sys; sys.path.insert(0, str(Path("core").resolve())); from music_code import MusicCode; print(MusicCode(120).Fs)'
```

## Editing Guidance

- Keep path-sensitive folders in place unless you are intentionally updating path resolution.
- Treat `export/` and `images/` as user output directories.
- Prefer small Python smoke commands or `songs/song_1.py` to verify changes before touching notebooks.
- Avoid mass-editing notebooks unless the task specifically calls for it.
- If you change sample folder names or asset-loading behavior, update both `MusicCode.__init__` and `sample()`.
- If you change data schemas in `data/`, verify all note and chord generation paths.

## Practical Gotchas

- `Wave` methods usually return new `Wave` objects, so chaining is the normal usage style.
- `bounce()` creates files in `export/` and auto-increments duplicate file names.
- `view()` and some test paths rely on Matplotlib; in headless environments, `MPLBACKEND=Agg` is useful.
- `Wave.__init__` reloads note-frequency CSV data, so repeated wave creation is not free.
- Notebooks are useful references, but some of them may need small import or path adjustments before running cleanly.
