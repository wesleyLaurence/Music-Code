from datetime import datetime
import os
from pathlib import Path
import sys
import warnings

REPO_ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = REPO_ROOT / "images" / ".mplcache"
MPL_DIR = CACHE_DIR / "matplotlib"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
MPL_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("XDG_CACHE_HOME", str(CACHE_DIR))
os.environ.setdefault("MPLCONFIGDIR", str(MPL_DIR))

import matplotlib

matplotlib.use("Agg")
warnings.filterwarnings(
    "ignore",
    message="Matplotlib is currently using agg",
    category=UserWarning,
)

LIB_DIR = REPO_ROOT / "core"
sys.path.insert(0, str(LIB_DIR))

from music_code import MusicCode


BPM = 118


BAR_SPECS = [
    {
        "center": "C Lydian",
        "root": "C3",
        "upper_root": "D4",
        "pad_chord": "maj 7 #11",
        "upper_chord": "maj triad",
        "accent_chord": "dream chord",
        "cluster": ["B4", "D5", 739.989],
        "bass_line": ["C2", "G1", "D2", "E2", "C2", "G1", "B1", "D2"],
        "ostinato": ["E4", "F#4", "G4", "D4", "B4"],
        "lead": [
            "E5",
            "F#5",
            "G5",
            "B5",
            "A5",
            "G5",
            "F#5",
            "E5",
            "D5",
            "E5",
            "G5",
            "A5",
            "B5",
            "A5",
            "F#5",
            "E5",
        ],
        "counter": [
            "G4",
            "A4",
            "B4",
            "F#4",
            "G4",
            "E4",
            "D4",
            "E4",
            "F#4",
            "A4",
            "G4",
            "E4",
        ],
    },
    {
        "center": "E Lydian",
        "root": "E3",
        "upper_root": "F#4",
        "pad_chord": "maj 13",
        "upper_chord": "maj 6 9",
        "accent_chord": "elektra chord",
        "cluster": ["D#5", "F#5", "A#5"],
        "bass_line": ["E2", "B1", "F#2", "G#2", "E2", "C#2", "D#2", "B1"],
        "ostinato": ["G#4", "A#4", "B4", "F#4", "D#5"],
        "lead": [
            "G#5",
            "A#5",
            "B5",
            "D#6",
            "C#6",
            "B5",
            "A#5",
            "G#5",
            "F#5",
            "G#5",
            "B5",
            "C#6",
            "D#6",
            "C#6",
            "A#5",
            "G#5",
        ],
        "counter": [
            "B4",
            "C#5",
            "D#5",
            "A#4",
            "B4",
            "G#4",
            "F#4",
            "G#4",
            "A#4",
            "C#5",
            "B4",
            "G#4",
        ],
    },
    {
        "center": "Bb Lydian",
        "root": "Bb2",
        "upper_root": "C4",
        "pad_chord": "maj 7 #11",
        "upper_chord": "maj triad",
        "accent_chord": "dream chord",
        "cluster": ["A4", "C5", 659.255],
        "bass_line": ["Bb1", "F1", "C2", "D2", "Bb1", "F1", "A1", "C2"],
        "ostinato": ["D4", "E4", "F4", "C4", "A4"],
        "lead": [
            "D5",
            "E5",
            "F5",
            "A5",
            "G5",
            "F5",
            "E5",
            "D5",
            "C5",
            "D5",
            "F5",
            "G5",
            "A5",
            "G5",
            "E5",
            "D5",
        ],
        "counter": [
            "F4",
            "G4",
            "A4",
            "E4",
            "F4",
            "D4",
            "C4",
            "D4",
            "E4",
            "G4",
            "F4",
            "D4",
        ],
    },
    {
        "center": "Gb Lydian",
        "root": "Gb2",
        "upper_root": "Ab3",
        "pad_chord": "maj 13",
        "upper_chord": "maj 6 9",
        "accent_chord": "farben chord",
        "cluster": ["F4", "Ab4", 523.251],
        "bass_line": ["Gb1", "Db1", "Ab1", "Bb1", "Gb1", "Db1", "F1", "Ab1"],
        "ostinato": ["Bb3", "C4", "Db4", "Ab3", "F4"],
        "lead": [
            "Bb4",
            "C5",
            "Db5",
            "F5",
            "Eb5",
            "Db5",
            "C5",
            "Bb4",
            "Ab4",
            "Bb4",
            "Db5",
            "Eb5",
            "F5",
            "Eb5",
            "C5",
            "Bb4",
        ],
        "counter": [
            "Db4",
            "Eb4",
            "F4",
            "C4",
            "Db4",
            "Bb3",
            "Ab3",
            "Bb3",
            "C4",
            "Eb4",
            "Db4",
            "Bb3",
        ],
    },
    {
        "center": "D Lydian",
        "root": "D3",
        "upper_root": "E4",
        "pad_chord": "maj 7 #11",
        "upper_chord": "maj triad",
        "accent_chord": "elektra chord",
        "cluster": ["C#5", "E5", "G#5"],
        "bass_line": ["D2", "A1", "E2", "F#2", "D2", "A1", "C#2", "E2"],
        "ostinato": ["F#4", "G#4", "A4", "E4", "C#5"],
        "lead": [
            "F#5",
            "G#5",
            "A5",
            "C#6",
            "B5",
            "A5",
            "G#5",
            "F#5",
            "E5",
            "F#5",
            "A5",
            "B5",
            "C#6",
            "B5",
            "G#5",
            "F#5",
        ],
        "counter": [
            "A4",
            "B4",
            "C#5",
            "G#4",
            "A4",
            "F#4",
            "E4",
            "F#4",
            "G#4",
            "B4",
            "A4",
            "F#4",
        ],
    },
    {
        "center": "Ab Lydian",
        "root": "Ab2",
        "upper_root": "Bb3",
        "pad_chord": "maj 13",
        "upper_chord": "maj 6 9",
        "accent_chord": "farben chord",
        "cluster": ["G4", "Bb4", "D5"],
        "bass_line": ["Ab1", "Eb1", "Bb1", "C2", "Ab1", "Eb1", "G1", "Bb1"],
        "ostinato": ["C4", "D4", "Eb4", "Bb3", "G4"],
        "lead": [
            "C5",
            "D5",
            "Eb5",
            "G5",
            "F5",
            "Eb5",
            "D5",
            "C5",
            "Bb4",
            "C5",
            "Eb5",
            "F5",
            "G5",
            "F5",
            "D5",
            "C5",
        ],
        "counter": [
            "Eb4",
            "F4",
            "G4",
            "D4",
            "Eb4",
            "C4",
            "Bb3",
            "C4",
            "D4",
            "F4",
            "Eb4",
            "C4",
        ],
    },
    {
        "center": "F Lydian",
        "root": "F2",
        "upper_root": "G3",
        "pad_chord": "maj 7 #11",
        "upper_chord": "maj triad",
        "accent_chord": "dream chord",
        "cluster": ["E4", "G4", "B4"],
        "bass_line": ["F1", "C2", "G1", "A1", "F1", "C2", "E2", "G1"],
        "ostinato": ["A3", "B3", "C4", "G3", "E4"],
        "lead": [
            "A4",
            "B4",
            "C5",
            "E5",
            "D5",
            "C5",
            "B4",
            "A4",
            "G4",
            "A4",
            "C5",
            "D5",
            "E5",
            "D5",
            "B4",
            "A4",
        ],
        "counter": [
            "C4",
            "D4",
            "E4",
            "B3",
            "C4",
            "A3",
            "G3",
            "A3",
            "B3",
            "D4",
            "C4",
            "A3",
        ],
    },
    {
        "center": "C Lydian Return",
        "root": "C3",
        "upper_root": "D4",
        "pad_chord": "maj 13",
        "upper_chord": "maj 6 9",
        "accent_chord": "elektra chord",
        "cluster": ["B4", "D5", "F#5"],
        "bass_line": ["C2", "G1", "D2", "E2", "C2", "B1", "A1", "G1"],
        "ostinato": ["G4", "A4", "B4", "F#4", "E5"],
        "lead": [
            "G5",
            "A5",
            "B5",
            "D6",
            "C6",
            "B5",
            "A5",
            "G5",
            "F#5",
            "G5",
            "B5",
            "C6",
            "D6",
            "C6",
            "A5",
            "G5",
        ],
        "counter": [
            "B4",
            "C5",
            "D5",
            "A4",
            "B4",
            "G4",
            "F#4",
            "G4",
            "A4",
            "C5",
            "B4",
            "G4",
        ],
    },
]


def step_sequence(m, hit_wave, pattern, step):
    steps = []
    for hit in pattern:
        steps.append(hit_wave if hit else m.rest(step))
    return m.join_waves(tuple(steps)).time_edit(1)


def make_pad_bar(m, spec):
    foundation = (
        m.chord(
            spec["pad_chord"],
            spec["root"],
            "sine-tri",
            duration=1,
            wt_pos=7,
            fade_in=1 / 32,
            fade_out=1 / 16,
            in_curve=4,
            out_curve=4,
        )
        .HPF(150)
        .LFO(0.12, "sine", vol=0.55)
        .pan("L24")
        .vol(0.42)
    )
    upper = (
        m.chord(
            spec["upper_chord"],
            spec["upper_root"],
            "tri-saw",
            duration=1,
            wt_pos=3,
            fade_in=1 / 32,
            fade_out=1 / 16,
            in_curve=3,
            out_curve=3,
        )
        .HPF(320)
        .delay(1 / 16, 4, 28, 18, stereo=True)
        .pan("R18")
        .vol(0.22)
    )
    constellation = (
        m.create_wave(spec["cluster"], "sine-square", duration=1, wt_pos=4)
        .HPF(1250)
        .LFO(0.22, "tri", vol=0.5)
        .pan("R35")
        .vol(0.1)
    )
    return m.add_waves((foundation, upper, constellation)).time_edit(1)


def make_comp_bar(m, spec):
    stab_a = (
        m.chord(spec["accent_chord"], spec["upper_root"], "tri-square", duration=1 / 8, wt_pos=2)
        .HPF(420)
        .vol(0.18)
    )
    stab_b = (
        m.chord(spec["pad_chord"], spec["root"], "sine-saw", duration=1 / 8, wt_pos=2)
        .HPF(280)
        .vol(0.15)
    )
    stab_c = (
        m.create_wave(spec["cluster"], "square", duration=1 / 8, wt_pos=2)
        .HPF(1800)
        .vol(0.07)
    )
    comp = m.join_waves(
        (
            m.rest(1 / 8),
            stab_a,
            m.rest(1 / 8),
            stab_b,
            m.rest(1 / 8),
            stab_a,
            m.rest(1 / 8),
            stab_c,
        )
    )
    return comp.delay(1 / 12, 3, 22, 20, stereo=True).pan("R10").vol(0.8).time_edit(1)


def make_bass_bar(m, spec):
    sub = (
        m.sequence(
            spec["bass_line"],
            "sine",
            rhythm=1 / 8,
            duration=1,
            fade_in=1 / 64,
            fade_out=1 / 64,
        )
        .LPF(135)
        .vol(0.85)
    )
    attack = (
        m.sequence(
            spec["bass_line"],
            "sine-square",
            rhythm=1 / 8,
            duration=1,
            wt_pos=2,
            fade_in=1 / 64,
            fade_out=1 / 64,
        )
        .LPF(260)
        .vol(0.35)
    )
    motion = (
        m.sequence(
            spec["ostinato"],
            "tri",
            rhythm=1 / 20,
            duration=1,
            wt_pos=2,
            fade_in=1 / 64,
            fade_out=1 / 64,
        )
        .LPF(340)
        .vol(0.08)
    )
    return m.add_waves((sub, attack, motion)).time_edit(1).vol(0.82)


def make_arp_bar(m, spec):
    arp = (
        m.arpeggio(
            spec["pad_chord"],
            spec["root"],
            "saw1",
            rhythm=1 / 20,
            duration=1,
            wt_pos=2,
            arp_type="up-down",
            fade_in=1 / 64,
            fade_out=1 / 64,
        )
        .HPF(720)
        .delay(1 / 16, 5, 24, 18, stereo=True)
        .pan("R14")
        .vol(0.14)
    )
    lattice = (
        m.sequence(
            spec["ostinato"],
            "tri-square",
            rhythm=1 / 20,
            duration=1,
            wt_pos=2,
            fade_in=1 / 64,
            fade_out=1 / 64,
        )
        .HPF(1400)
        .LFO(0.3, "sine", vol=0.58)
        .pan("L16")
        .vol(0.09)
    )
    return m.add_waves((arp, lattice)).time_edit(1)


def make_counter_bar(m, spec):
    return (
        m.sequence(
            spec["counter"],
            "tri-sine",
            rhythm=1 / 12,
            duration=1,
            wt_pos=3,
            fade_in=1 / 64,
            fade_out=1 / 64,
        )
        .HPF(880)
        .delay(1 / 12, 3, 20, 16, stereo=True)
        .pan("R12")
        .vol(0.12)
        .time_edit(1)
    )


def make_lead_bar(m, spec):
    main = (
        m.sequence(
            spec["lead"],
            "sine-saw",
            rhythm=1 / 16,
            duration=1,
            wt_pos=3,
            fade_in=1 / 64,
            fade_out=1 / 64,
        )
        .HPF(640)
        .delay(1 / 16, 5, 26, 20, stereo=True)
        .pan("L10")
        .vol(0.16)
    )
    tail = (
        m.sequence(
            spec["counter"],
            "sine",
            rhythm=1 / 24,
            duration=1,
            wt_pos=2,
            fade_in=1 / 128,
            fade_out=1 / 64,
        )
        .HPF(1600)
        .pan("R18")
        .vol(0.05)
    )
    return m.add_waves((main, tail)).time_edit(1)


def make_intro_pulse_bar(m):
    ping = (
        m.create_wave([523.251, 739.989, 987.767], "sine-square", duration=1 / 8, wt_pos=5)
        .fade(1 / 128, 5, 1 / 64, 4)
        .HPF(2200)
        .LFO(0.45, "tri", vol=0.6)
        .pan("R28")
        .vol(0.1)
    )
    mirrored = ping.reverse().pan("L18").vol(0.8)
    return m.join_waves((ping, m.rest(3 / 8), mirrored, m.rest(3 / 8))).time_edit(1)


def make_transition_riser(m):
    return (
        m.sample("fx", "swell in.wav")
        .reverse()
        .time_edit(2.0, mode="abs", slice_from_end=True)
        .fade(1 / 32, 4, 1 / 16, 3)
        .pan("L30")
        .vol(0.16)
    )


def make_impact(m):
    return (
        m.sample("fx", "V_RIOT_fx_one_shot_space.wav")
        .time_edit(1 / 2)
        .fade(1 / 64, 3, 1 / 32, 3)
        .pan("R24")
        .vol(0.14)
    )


def main():
    m = MusicCode(BPM)
    render_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    halo_name = f"lydian_fusion_halo_{render_stamp}.wav"
    master_name = f"lydian_fusion_constellation_{render_stamp}.wav"

    kick = m.sample("kick", "kick_06.wav").time_edit(1 / 16).vol(1.1)
    snare = m.sample("snare", "snare_04.wav").time_edit(1 / 16).vol(0.9)
    clap = m.sample("clap", "clap_03.wav").time_edit(1 / 16).vol(0.35)
    ghost = m.sample("snare", "snare_11.wav").time_edit(1 / 16).vol(0.28)
    hat_16 = m.sample("hihat", "hihat_02.wav").time_edit(1 / 16).vol(0.28).pan("L18")
    hat_12 = m.sample("hihat", "UZ_hihat_tp_02.wav").time_edit(1 / 12).vol(0.16).pan("R20")
    perc_20 = m.sample("perc", "perc_04.wav").time_edit(1 / 20).vol(0.2).pan("R30")
    perc_16 = m.sample("perc", "perc_07.wav").time_edit(1 / 16).vol(0.14).pan("L24")
    open_hat = m.sample("cymbal", "open_00.wav").time_edit(1 / 8).vol(0.22).pan("R18")
    reverse_cym = (
        m.sample("cymbal", "open_01.wav")
        .reverse()
        .time_edit(1)
        .fade(1 / 16, 4, 1 / 16, 3)
        .vol(0.18)
        .pan("L22")
    )

    drum_bar_1 = m.add_waves(
        (
            step_sequence(m, kick, [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0], 1 / 16),
            step_sequence(m, snare, [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], 1 / 16),
            step_sequence(m, clap, [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], 1 / 16),
            step_sequence(m, hat_16, [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0], 1 / 16),
            step_sequence(m, hat_12, [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1], 1 / 12),
            step_sequence(m, perc_20, [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0], 1 / 20),
        )
    ).time_edit(1)
    drum_bar_2 = m.add_waves(
        (
            step_sequence(m, kick, [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0], 1 / 16),
            step_sequence(m, snare, [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], 1 / 16),
            step_sequence(m, ghost, [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 1 / 16),
            step_sequence(m, hat_16, [1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0], 1 / 16),
            step_sequence(m, hat_12, [1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0], 1 / 12),
            step_sequence(m, perc_16, [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0], 1 / 16),
        )
    ).time_edit(1)
    drum_bar_3 = m.add_waves(
        (
            step_sequence(m, kick, [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1], 1 / 16),
            step_sequence(m, snare, [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], 1 / 16),
            step_sequence(m, hat_16, [1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1], 1 / 16),
            step_sequence(m, hat_12, [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0], 1 / 12),
            step_sequence(m, perc_20, [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0], 1 / 20),
            m.join_waves((m.rest(3 / 4), open_hat)).time_edit(1),
        )
    ).time_edit(1)
    drum_fill = m.add_waves(
        (
            step_sequence(m, kick, [1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0], 1 / 16),
            step_sequence(m, snare, [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0], 1 / 16),
            step_sequence(m, hat_16, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 1 / 16),
            step_sequence(m, perc_20, [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], 1 / 20),
            reverse_cym,
        )
    ).time_edit(1)

    drum_cycle_a = m.join_waves((drum_bar_1, drum_bar_2, drum_bar_3, drum_fill)).loop(2).time_edit(8)
    drum_cycle_b = m.join_waves((drum_bar_2, drum_bar_3, drum_fill, drum_bar_1)).loop(2).time_edit(8)
    peak_drums = m.join_waves((drum_bar_3, drum_fill, drum_bar_1, drum_fill)).loop(2).time_edit(8)

    intro_triplets = step_sequence(
        m,
        hat_12,
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        1 / 12,
    ).loop(4)
    intro_pulse = make_intro_pulse_bar(m).loop(4)

    pad_bars = [make_pad_bar(m, spec) for spec in BAR_SPECS]
    comp_bars = [make_comp_bar(m, spec) for spec in BAR_SPECS]
    bass_bars = [make_bass_bar(m, spec) for spec in BAR_SPECS]
    arp_bars = [make_arp_bar(m, spec) for spec in BAR_SPECS]
    counter_bars = [make_counter_bar(m, spec) for spec in BAR_SPECS]
    lead_bars = [make_lead_bar(m, spec) for spec in BAR_SPECS]

    intro_harmony = m.join_waves(tuple(pad_bars[:4]))
    full_harmony = m.join_waves(tuple(pad_bars))
    full_comp = m.join_waves(tuple(comp_bars))
    full_bass = m.join_waves(tuple(bass_bars))
    full_arp = m.join_waves(tuple(arp_bars))
    full_counter = m.join_waves(tuple(counter_bars))
    full_lead = m.join_waves(tuple(lead_bars))
    outro_harmony = m.join_waves(tuple(pad_bars[4:]))

    halo_source = m.add_waves(
        (
            m.join_waves((pad_bars[0], pad_bars[1])),
            m.join_waves((arp_bars[0], arp_bars[1])).vol(0.9),
        )
    ).time_edit(2)
    halo_source.bounce(halo_name, show_visual=False)

    halo_texture = (
        m.sample("archive", halo_name)
        .reverse()
        .loop(4)
        .LFO(0.08, "sine", vol=0.7)
        .pan("R26")
        .vol(0.12)
        .time_edit(8)
    )
    outro_halo = (
        m.sample("archive", halo_name)
        .reverse()
        .loop(2)
        .LFO(0.08, "tri", vol=0.65)
        .pan("L20")
        .vol(0.1)
        .time_edit(4)
    )

    intro_fx = m.join_waves((m.rest(3), make_transition_riser(m))).time_edit(4)
    head_fx = m.join_waves((m.rest(7), make_transition_riser(m))).time_edit(8)
    development_fx = m.join_waves((m.rest(7), make_transition_riser(m))).time_edit(8)
    peak_fx = m.join_waves((make_impact(m), m.rest(7.5))).time_edit(8)
    outro_fx = (
        m.join_waves((m.rest(1.5), make_impact(m).reverse().time_edit(2.0, mode="abs", slice_from_end=True)))
        .time_edit(4)
        .vol(0.8)
    )

    intro = m.add_waves((intro_harmony.vol(0.9), intro_triplets.vol(0.8), intro_pulse, intro_fx))
    head = m.add_waves((full_harmony, full_comp, full_bass, full_arp, drum_cycle_a, head_fx))
    development = m.add_waves(
        (full_harmony, full_comp, full_bass, full_arp, full_counter, drum_cycle_b, halo_texture, development_fx)
    )
    peak = m.add_waves(
        (full_harmony, full_comp, full_bass, full_arp, full_counter, full_lead, halo_texture, peak_drums, peak_fx)
    )
    outro = m.add_waves((outro_harmony, m.join_waves(tuple(counter_bars[4:])).vol(0.8), outro_halo, outro_fx)).fade(
        fade_in=False,
        fade_out=1,
        out_curve=7,
    )

    song = m.join_waves((intro, head, development, peak, outro)).fade(
        fade_in=1 / 8,
        in_curve=4,
        fade_out=1,
        out_curve=8,
    )
    song = song.vol(0.92)

    peak.view(plot_type="wave", freq_range=(40, 14000))
    print("Song duration in seconds:")
    song.time()
    song.bounce(master_name, show_visual=False)

    print(f"Rendered halo stem: {REPO_ROOT / 'export' / halo_name}")
    print(f"Rendered master: {REPO_ROOT / 'export' / master_name}")


if __name__ == "__main__":
    main()
