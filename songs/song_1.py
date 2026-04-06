from pathlib import Path
import sys

# Allow importing the local music_code module.
LIB_DIR = Path(__file__).resolve().parents[1] / "core"
sys.path.append(str(LIB_DIR))

from music_code import MusicCode


def step_sequence(m, hit_wave, pattern, step):
    steps = []
    for hit in pattern:
        steps.append(hit_wave if hit else m.rest(step))
    return m.join_waves(tuple(steps))


def make_pad(m, chord_label, root_note):
    left = (
        m.chord(chord_label, root_note, "sine", duration=1, wt_pos=555)
        .HPF(140)
        .pan("L30")
    )
    right = (
        m.chord(chord_label, root_note, "tri", duration=1, wt_pos=777)
        .HPF(140)
        .pan("R30")
    )
    return m.add_waves((left, right)).vol(0.65)


def make_arp(m, chord_label, root_note):
    return (
        m.arpeggio(chord_label, root_note, "saw1", rhythm=1 / 16, duration=1, wt_pos=3)
        .HPF(300)
        .vol(0.25)
        .pan("R20")
    )


def make_bass(m, notes):
    sub = m.sequence(
        notes, "sine", rhythm=1 / 4, duration=1, fade_in=1 / 16, fade_out=1 / 16
    ).LPF(140)
    mid = (
        m.sequence(
            notes,
            "square",
            rhythm=1 / 4,
            duration=1,
            fade_in=1 / 16,
            fade_out=1 / 16,
            wt_pos=2,
        )
        .LPF(240)
        .vol(0.6)
    )
    return m.add_waves((sub, mid)).vol(0.9)


def main():
    m = MusicCode(94)

    # Drum samples.
    kick = m.sample("kick", "kick_06.wav").time_edit(1 / 16).vol(1.2)
    snare = m.sample("snare", "snare_04.wav").time_edit(1 / 16).vol(1.0)
    clap = m.sample("clap", "clap_03.wav").time_edit(1 / 16).vol(0.6)
    hat_l = m.sample("hihat", "hihat_02.wav").time_edit(1 / 16).vol(0.45).pan("L20")
    hat_r = m.sample("hihat", "hihat_03.wav").time_edit(1 / 16).vol(0.4).pan("R20")
    open_hat = m.sample("cymbal", "open_00.wav").time_edit(1 / 4).vol(0.5)
    perc = m.sample("perc", "perc_04.wav").time_edit(1 / 16).vol(0.4).pan("R30")

    # One-bar drum patterns.
    kick_bar = step_sequence(
        m, kick, [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0], 1 / 16
    )
    snare_bar = step_sequence(
        m, snare, [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], 1 / 16
    )
    clap_bar = step_sequence(
        m, clap, [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], 1 / 16
    )
    hat_l_bar = step_sequence(
        m, hat_l, [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], 1 / 16
    )
    hat_r_bar = step_sequence(
        m, hat_r, [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], 1 / 16
    )
    perc_bar = step_sequence(
        m, perc, [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0], 1 / 16
    )
    open_hat_bar = m.join_waves((m.rest(3 / 4), open_hat))

    drum_bar = m.add_waves(
        (kick_bar, snare_bar, clap_bar, hat_l_bar, hat_r_bar, perc_bar, open_hat_bar)
    )

    # Harmonic progression (4 bars).
    progression = [
        ("min 9", "D3"),
        ("maj 7", "Bb2"),
        ("maj 7", "F3"),
        ("maj 9", "C3"),
    ]
    pad_bars = [make_pad(m, chord, root) for chord, root in progression]
    arp_bars = [make_arp(m, chord, root) for chord, root in progression]

    pads_4 = m.join_waves(tuple(pad_bars))
    pads_2 = m.join_waves(tuple(pad_bars[:2]))
    arp_4 = m.join_waves(tuple(arp_bars))
    arp_2 = m.join_waves(tuple(arp_bars[:2]))

    bass_notes = [
        ["D2", "D2", "A1", "C2"],
        ["Bb1", "Bb1", "F1", "A1"],
        ["F1", "F1", "C2", "E2"],
        ["C2", "C2", "G1", "A1"],
    ]
    bass_bars = [make_bass(m, notes) for notes in bass_notes]
    bass_4 = m.join_waves(tuple(bass_bars))

    # Melody (4 bars).
    phrase_1 = m.sequence(
        [
            "D4",
            "F4",
            "A4",
            "C5",
            "A4",
            "G4",
            "F4",
            "rest",
            "D4",
            "F4",
            "A4",
            "Bb4",
            "A4",
            "G4",
            "F4",
            "rest",
        ],
        "sine-tri",
        rhythm=1 / 8,
        duration=2,
        fade_in=1 / 32,
        fade_out=1 / 32,
        wt_pos=3,
    )
    phrase_2 = m.sequence(
        [
            "A4",
            "C5",
            "D5",
            "C5",
            "Bb4",
            "A4",
            "G4",
            "rest",
            "F4",
            "G4",
            "A4",
            "C5",
            "D5",
            "C5",
            "A4",
            "rest",
        ],
        "sine-tri",
        rhythm=1 / 8,
        duration=2,
        fade_in=1 / 32,
        fade_out=1 / 32,
        wt_pos=3,
    )
    melody_4 = m.join_waves((phrase_1, phrase_2)).HPF(350).vol(0.55).pan("L10")

    # Sections.
    intro = m.add_waves((pads_2, arp_2))
    drums_4 = drum_bar.loop(4)
    verse = m.add_waves((pads_4, bass_4, drums_4))
    chorus = m.add_waves((pads_4, arp_4, bass_4, drums_4, melody_4))
    outro = m.add_waves((pads_2, arp_2)).LPF(900)

    song = m.join_waves((intro, verse, chorus, outro))
    song.bounce("codex_song.wav", show_visual=False)


if __name__ == "__main__":
    main()
