# import library
from music_code import music_code

# initialize MusiCode, set BPM
m = music_code.MusicCode(bpm=120)

""" Test MusicCode and Wave class methods"""
    
class MusicCode_Tests:

    def __init__(self):
        self.no_errors=True

    # create_wave method tests

    def create_wave_tests(self):

        print("\nCREATE_WAVE METHOD TESTS\n")

        # default values
        default_note_labels = ['A2',440]
        default_wave_type='sine'
        default_duration=1/4
        default_wt_pos=1

        # NOTE_LABELS
        note_labels_set = [ [440], [50], ['C3'], ['C3','E3','G3'], ['F#3','A3','C#4'], ['Ab3','C3','Eb3'] ]
        for note_labels in note_labels_set:
            try:
                waveform = m.create_wave(note_labels=note_labels, 
                                         wave_type=default_wave_type, 
                                         duration=default_duration, 
                                         wt_pos=default_wt_pos)

                print("success: ", note_labels, default_wave_type, default_duration, default_wt_pos)
            except:
                self.no_errors = False
                print("CREATE_WAVE TEST FAILED: ", note_labels, default_wave_type, default_duration, default_wt_pos)


        # WAVE_TYPE        
        wave_type_set = ['sine','tri','square','saw1','saw2','sine-tri','sine-saw','sine-square','saw-square','tri-saw','tri-square']
        for wave_type in wave_type_set:
            try:
                waveform = m.create_wave(note_labels=default_note_labels, 
                                         wave_type=wave_type, 
                                         duration=default_duration, 
                                         wt_pos=default_wt_pos)

                print("success: ", default_note_labels, wave_type, default_duration, default_wt_pos)
            except:
                self.no_errors = False
                print("CREATE_WAVE TEST FAILED: ", default_note_labels, wave_type, default_duration, default_wt_pos)


        # DURATION        
        duration_set = [1/64,1/32,1/24,1/16, 1/8, 1/4, 1/2, 1]
        for duration in duration_set:
            try:
                waveform = m.create_wave(note_labels=default_note_labels, 
                                         wave_type=default_wave_type, 
                                         duration=duration, 
                                         wt_pos=default_wt_pos)

                print("success: ", default_note_labels, default_wave_type, duration, default_wt_pos)
            except:
                self.no_errors = False
                print("CREATE_WAVE TEST FAILED: ", default_note_labels, default_wave_type, duration, default_wt_pos)


        # WT_POS        
        wt_pos_set = [1, 2, 5, 33, 66, 999]
        for wt_pos in wt_pos_set:
            try:
                waveform = m.create_wave(note_labels=default_note_labels, 
                                         wave_type=default_wave_type, 
                                         duration=default_duration, 
                                         wt_pos=default_wt_pos)

                print("success: ", default_note_labels, default_wave_type, default_duration, default_wt_pos)
            except:
                self.no_errors = False
                print("CREATE_WAVE TEST FAILED: ", default_note_labels, default_wave_type, default_duration, default_wt_pos)

        print('\nALL CREATE_WAVE TESTS SUCCESSFUL\n')        


    # sequence method tests

    def sequence_tests(self):

        print("SEQUENCE METHOD TESTS\n")

        # default values
        default_note_labels = ['A2', 440, 'rest']
        default_wave_type = 'tri'
        default_duration = 1
        default_rhythm = 1/8
        default_wt_pos = 1
        in_curve = 3
        out_curve = 7

        # NOTE_LABELS
        note_labels_set = [[220, 440, 880], 
                           [50, 100, 200, 400, 800], 
                           ['C3','E3','G3','A2'], 
                           ['A2','rest','G3','C4'], 
                           ['E2','rest','rest', 'C2'], 
                           ['Ab3',440,'Eb3']]

        for note_labels in note_labels_set:
            try:
                waveform = m.sequence(note_labels=note_labels, 
                                         wave_type=default_wave_type, 
                                         duration=default_duration,
                                         rhythm=default_rhythm,
                                         wt_pos=default_wt_pos)

                print("success: ", note_labels, default_wave_type, default_duration, default_rhythm, default_wt_pos)
            except:
                self.no_errors = False
                print("SEQUENCE TEST FAILED: ", note_labels, default_wave_type, default_duration, default_rhythm, default_wt_pos)



        # WAVE_TYPE
        wave_type_set = ['sine','tri','square','saw1','saw2','sine-tri','sine-saw','sine-square','saw-square','tri-saw','tri-square']

        for wave_type in wave_type_set:
            try:
                waveform = m.sequence(note_labels=default_note_labels, 
                                         wave_type=wave_type, 
                                         duration=default_duration,
                                         rhythm=default_rhythm,
                                         wt_pos=default_wt_pos)

                print("success: ", default_note_labels, wave_type, default_duration, default_rhythm, default_wt_pos)
            except:
                self.no_errors = False
                print("SEQUENCE TEST FAILED: ", default_note_labels, wave_type, default_duration, default_rhythm, default_wt_pos)                  


        # DURATION
        duration_set = [1/8, 1/4, 1/2, 1, 2]

        for duration in duration_set:
            try:
                waveform = m.sequence(note_labels=default_note_labels, 
                                         wave_type=default_wave_type, 
                                         duration=duration,
                                         rhythm=default_rhythm,
                                         wt_pos=default_wt_pos)

                print("success: ", default_note_labels, default_wave_type, duration, default_rhythm, default_wt_pos)
            except:
                self.no_errors = False
                print("SEQUENCE TEST FAILED: ", default_note_labels, default_wave_type, duration, default_rhythm, default_wt_pos)                 

        # RHYTHM
        rhythm_set = [1/64, 1/32, 1/16, 1/12, 1/8]

        for rhythm in rhythm_set:
            try:
                waveform = m.sequence(note_labels=default_note_labels, 
                                         wave_type=default_wave_type, 
                                         duration=default_duration,
                                         rhythm=rhythm,
                                         wt_pos=default_wt_pos)

                print("success: ", default_note_labels, default_wave_type, default_duration, rhythm, default_wt_pos)
            except:
                self.no_errors = False
                print("SEQUENCE TEST FAILED: ", default_note_labels, default_wave_type, default_duration, rhythm, default_wt_pos) 



        # WT_POS
        wt_pos_set = [1, 2, 5, 33, 66, 999]

        for wt_pos in wt_pos_set:
            try:
                waveform = m.sequence(note_labels=default_note_labels, 
                                         wave_type=default_wave_type, 
                                         duration=default_duration,
                                         rhythm=default_rhythm,
                                         wt_pos=wt_pos)

                print("success: ", default_note_labels, default_wave_type, default_duration, default_rhythm, wt_pos)
            except:
                self.no_errors = False
                print("SEQUENCE TEST FAILED: ", default_note_labels, default_wave_type, default_duration, default_rhythm, wt_pos)


        # ARP_TYPE
        arp_types = ['up','down','up-down','down-up']

        for arp_type in arp_types:
            try:
                waveform = m.sequence(note_labels=default_note_labels, 
                                         wave_type=default_wave_type, 
                                         duration=default_duration,
                                         rhythm=default_rhythm,
                                         wt_pos=default_wt_pos,
                                         arp_type=arp_type)

                print("success: ", default_note_labels, default_wave_type, default_duration, default_rhythm, default_wt_pos, arp_type)
            except:
                self.no_errors = False
                print("SEQUENCE TEST FAILED: ", default_note_labels, default_wave_type, default_duration, default_rhythm, default_wt_pos, arp_type)


        # ARP_TYPE
        fade_values = [1/64, 1/32, 1/12, 1/8]

        for fade_value in fade_values:
            try:
                waveform = m.sequence(note_labels=default_note_labels, 
                                         wave_type=default_wave_type, 
                                         duration=default_duration,
                                         rhythm=default_rhythm,
                                         wt_pos=default_wt_pos,
                                         fade_in=fade_value,
                                         fade_out=fade_value,
                                         in_curve=in_curve,
                                         out_curve=out_curve)

                print("success: ", default_note_labels, default_wave_type, default_duration, default_rhythm, default_wt_pos, fade_value, fade_value, in_curve, out_curve)
            except:
                self.no_errors = False
                print("SEQUENCE TEST FAILED: ", default_note_labels, default_wave_type, default_duration, default_rhythm, default_wt_pos, fade_value, fade_value, in_curve, out_curve)

        print('\nALL SEQUENCE TESTS SUCCESSFUL\n')


    def rest_tests(self):

        print("REST METHOD TESTS\n")

        duration_set = [1/8, 1/4, 1/2, 1, 2]

        # test relative time
        for duration in duration_set:
            try:
                waveform = m.rest(duration=duration)

                print("success: ", m.time_mode, duration)
            except:
                self.no_errors = False
                print("REST TEST FAILED: ", m.time_mode, duration)


        # test absolute time
        for duration in duration_set:
            try:
                m.time_mode='absolute'
                waveform = m.rest(duration=duration)

                print("success: ", m.time_mode, duration)
            except:
                self.no_errors = False
                print("REST TEST FAILED: ", m.time_mode, duration)

        m.time_mode='relative'       


        print('\nALL REST TESTS SUCCESSFUL\n')


    def sample_tests(self):

        print("SAMPLE METHOD TESTS\n")

        try:
            for sound_folder in ['kick','snare','clap','hihat','perc','cymbal','bass','fx','user','archive']:       
                waveform = m.sample(sound_folder=sound_folder,sample_id=0)
                print("success: ", sound_folder, str(0))
        except:
            self.no_errors = False
            print("SAMPLE TEST FAILED: ", sound_folder, str(0))


        try:
            for file_name in m.kick:
                waveform = m.sample(sound_folder='kick',sample_id=file_name)
                print("success: ", 'kick', file_name)
        except:
            self.no_errors = False
            print("SAMPLE TEST FAILED: ", 'kick', file_name)

        try:

            for file_name in m.snare:
                waveform = m.sample(sound_folder='snare',sample_id=file_name)
                print("success: ", 'snare', file_name)      

            for file_name in m.clap:
                waveform = m.sample(sound_folder='clap',sample_id=file_name)
                print("success: ", 'clap', file_name)

            for file_name in m.hihat:
                waveform = m.sample(sound_folder='hihat',sample_id=file_name)
                print("success: ", 'hihat', file_name)

            for file_name in m.perc:
                waveform = m.sample(sound_folder='perc',sample_id=file_name)
                print("success: ", 'perc', file_name)

            for file_name in m.cymbal:
                waveform = m.sample(sound_folder='cymbal',sample_id=file_name)
                print("success: ", 'cymbal', file_name)

            for file_name in m.bass:
                waveform = m.sample(sound_folder='bass',sample_id=file_name)
                print("success: ", 'bass', file_name)

            for file_name in m.fx:
                waveform = m.sample(sound_folder='fx',sample_id=file_name)
                print("success: ", 'fx', file_name)

            for file_name in m.user:
                waveform = m.sample(sound_folder='user',sample_id=file_name)
                print("success: ", 'user', file_name)

            print('\nALL SAMPLE TESTS SUCCESSFUL\n')

        except:
            self.no_errors = False
            print("SAMPLE TEST FAILED: ", "Check file names")


    def arpeggio_tests(self):

        print("ARPEGGIO METHOD TESTS\n")

        # default values
        default_chord_label = 'maj triad'
        default_start_note = 'C3'
        default_wave_type = 'tri'
        default_duration = 1
        default_rhythm = 1/8
        in_curve = 3
        out_curve = 7

        # Chord Labels
        chord_label_set = m.all_chords

        for chord_label in chord_label_set:
            try:
                waveform = m.arpeggio(chord_label=chord_label, 
                                         start_note=default_start_note,
                                         wave_type=default_wave_type, 
                                         duration=default_duration,
                                         rhythm=default_rhythm)

                print("success: ", chord_label, default_start_note, default_wave_type, default_duration, default_rhythm)
            except:
                self.no_errors = False
                print("ARPEGGIO TEST FAILED: ", chord_label, default_start_note, default_wave_type, default_duration, default_rhythm)


        # Chord Labels
        chord_label_set = m.all_chords

        for start_note in ['A1', 'C2', 'Gb3', 'F#4',]:
            try:
                waveform = m.arpeggio(chord_label=default_chord_label, 
                                         start_note=start_note,
                                         wave_type=default_wave_type, 
                                         duration=default_duration,
                                         rhythm=default_rhythm)

                print("success: ", default_chord_label, start_note, default_wave_type, default_duration, default_rhythm)
            except:
                self.no_errors = False
                print("ARPEGGIO TEST FAILED: ", default_chord_label, start_note, default_wave_type, default_duration, default_rhythm)



        # WAVE_TYPE
        wave_type_set = ['sine','tri','square','saw1','saw2','sine-tri','sine-saw','sine-square','saw-square','tri-saw','tri-square']

        for wave_type in wave_type_set:
            try:
                waveform = m.arpeggio(chord_label=default_chord_label, 
                                         start_note=default_start_note,
                                         wave_type=wave_type, 
                                         duration=default_duration,
                                         rhythm=default_rhythm)

                print("success: ", default_chord_label, default_start_note, wave_type, default_duration, default_rhythm)
            except:
                self.no_errors = False
                print("ARPEGGIO TEST FAILED: ", default_chord_label, default_start_note, wave_type, default_duration, default_rhythm)                  


        # DURATION
        duration_set = [1/8, 1/4, 1/2, 1, 2]

        for duration in duration_set:
            try:
                waveform = m.arpeggio(chord_label=default_chord_label, 
                                         start_note=default_start_note,
                                         wave_type=default_wave_type, 
                                         duration=duration,
                                         rhythm=default_rhythm)

                print("success: ", default_chord_label, default_start_note, default_wave_type, duration, default_rhythm)
            except:
                self.no_errors = False
                print("ARPEGGIO TEST FAILED: ", default_chord_label, default_start_note, default_wave_type, duration, default_rhythm)                 

        # RHYTHM
        rhythm_set = [1/64, 1/32, 1/16, 1/12, 1/8]

        for rhythm in rhythm_set:
            try:
                waveform = m.arpeggio(chord_label=default_chord_label, 
                                         start_note=default_start_note,
                                         wave_type=default_wave_type, 
                                         duration=default_duration,
                                         rhythm=rhythm)

                print("success: ", default_chord_label, default_start_note, default_wave_type, default_duration, rhythm)
            except:
                self.no_errors = False
                print("ARPEGGIO TEST FAILED: ", default_chord_label, default_start_note, default_wave_type, default_duration, rhythm) 



        # ARP_TYPE
        arp_types = ['up','down','up-down','down-up']

        for arp_type in arp_types:
            try:
                waveform = m.arpeggio(chord_label=default_chord_label, 
                                         start_note=default_start_note,
                                         wave_type=default_wave_type, 
                                         duration=default_duration,
                                         rhythm=default_rhythm,
                                         arp_type=arp_type)

                print("success: ", default_chord_label, default_start_note, default_wave_type, default_duration, default_rhythm, arp_type)
            except:
                self.no_errors = False
                print("ARPEGGIO TEST FAILED: ", default_chord_label, default_start_note, default_wave_type, default_duration, default_rhythm, arp_type)


        # FADES
        fade_values = [1/64, 1/32, 1/12, 1/8]

        for fade_value in fade_values:
            try:
                waveform = m.arpeggio(chord_label=default_chord_label, 
                                         start_note=default_start_note,
                                         wave_type=default_wave_type, 
                                         duration=default_duration,
                                         rhythm=default_rhythm,
                                         fade_in=fade_value,
                                         fade_out=fade_value,
                                         in_curve=in_curve,
                                         out_curve=out_curve)

                print("success: ", default_chord_label, default_start_note, default_wave_type, default_duration, default_rhythm, fade_value, fade_value, in_curve, out_curve)
            except:
                self.no_errors = False
                print("ARPEGGIO TEST FAILED: ", default_chord_label, default_start_note, default_wave_type, default_duration, default_rhythm, fade_value, fade_value, in_curve, out_curve)


        print('\nALL ARPEGGIO TESTS SUCCESSFUL\n')



    def chord_tests(self):

        print("CHORD METHOD TESTS\n")

        # default values
        default_chord_label = 'maj triad'
        default_start_note = 'C3'
        default_wave_type = 'tri'
        default_duration = 1
        in_curve = 3
        out_curve = 7

        # Chord Labels
        chord_label_set = m.all_chords

        for chord_label in chord_label_set:
            try:
                waveform = m.chord(chord_label=chord_label, 
                                         start_note=default_start_note,
                                         wave_type=default_wave_type, 
                                         duration=default_duration)

                print("success: ", chord_label, default_start_note, default_wave_type, default_duration)
            except:
                self.no_errors = False
                print("CHORD TEST FAILED: ", chord_label, default_start_note, default_wave_type, default_duration)


        # Chord Labels
        chord_label_set = m.all_chords

        for start_note in ['A1', 'C2', 'Gb3', 'F#4',]:
            try:
                waveform = m.chord(chord_label=default_chord_label, 
                                         start_note=start_note,
                                         wave_type=default_wave_type, 
                                         duration=default_duration)

                print("success: ", default_chord_label, start_note, default_wave_type, default_duration)
            except:
                self.no_errors = False
                print("CHORD TEST FAILED: ", default_chord_label, start_note, default_wave_type, default_duration)



        # WAVE_TYPE
        wave_type_set = ['sine','tri','square','saw1','saw2','sine-tri','sine-saw','sine-square','saw-square','tri-saw','tri-square']

        for wave_type in wave_type_set:
            try:
                waveform = m.chord(chord_label=default_chord_label, 
                                         start_note=default_start_note,
                                         wave_type=wave_type, 
                                         duration=default_duration)

                print("success: ", default_chord_label, default_start_note, wave_type, default_duration)
            except:
                self.no_errors = False
                print("CHORD TEST FAILED: ", default_chord_label, default_start_note, wave_type, default_duration)                  


        # DURATION
        duration_set = [1/8, 1/4, 1/2, 1, 2]

        for duration in duration_set:
            try:
                waveform = m.chord(chord_label=default_chord_label, 
                                         start_note=default_start_note,
                                         wave_type=default_wave_type, 
                                         duration=duration)

                print("success: ", default_chord_label, default_start_note, default_wave_type, duration)
            except:
                self.no_errors = False
                print("CHORD TEST FAILED: ", default_chord_label, default_start_note, default_wave_type, duration)                 


        print('\nALL CHORD TESTS SUCCESSFUL\n')



    def time_tests(self):

        try:
            # generate waveforms
            waveform1 = m.create_wave(['C2'], 'sine', 1/16)
            waveform2 = m.sequence(['C2'], 'sine', rhythm=1/16, duration=1/8)

            # test method
            waveform1.time()
            waveform2.time()

            # verify
            print('\nALL TIME TESTS SUCCESSFUL\n')

        except:
            self.no_errors = False
            print("\nTIME TEST FAILED")


    def time_edit_tests(self):

        try:
            # generate waveforms
            waveform1 = m.create_wave(['C2'], 'sine', 1/4)
            waveform2 = m.sequence(['C2'], 'sine', rhythm=1/8, duration=1/4)

            # test method
            waveform1.time_edit(1/2)
            waveform2.time_edit(1/8)

            # verify
            print('\nALL TIME EDIT TESTS SUCCESSFUL\n')

        except:
            self.no_errors = False
            print("\nTIME EDIT TEST FAILED")


    def vol_tests(self):

        try:
            # generate waveforms
            waveform1 = m.create_wave(['C2'], 'sine', 1/16)
            waveform2 = m.sequence(['C2'], 'sine', rhythm=1/16, duration=1/8)

            # test method
            waveform1.vol(2)
            waveform2.vol(1/4)

            # verify
            print('\nALL VOLUME TESTS SUCCESSFUL\n')

        except:
            self.no_errors = False
            print("\nVOLUME TEST FAILED")    


    def bounce_tests(self):

        try:
            # generate waveforms
            waveform1 = m.create_wave(['C2'], 'sine', 1/4)
            waveform2 = m.sequence(['C2'], 'sine', rhythm=1/8, duration=1/4)

            # test method
            waveform1.bounce()
            waveform2.bounce('test.wav')
            waveform2.bounce('test1.wav',show_visual=False)

            # verify
            print('\nALL BOUNCE TESTS SUCCESSFUL\n')

        except:
            self.no_errors = False
            print("\nBOUNCE TEST FAILED") 


    def view_tests(self):

        try:
            # generate waveforms
            waveform1 = m.create_wave(['E0','B3'], 'square', 1/4)


            # test method
            waveform1.view()

            # verify
            print('\nALL VIEW TESTS SUCCESSFUL\n')

        except:
            self.no_errors = False
            print("\nVIEW TEST FAILED") 


    def loop_tests(self):

        try:
            # generate waveforms
            waveform1 = m.create_wave(['C2'], 'sine', 1/4)
            waveform2 = m.sequence(['C2'], 'sine', rhythm=1/8, duration=1/4)

            # test method
            waveform1.loop(2)
            waveform2.loop(4)

            # verify
            print('\nALL LOOP TESTS SUCCESSFUL\n')

        except:
            self.no_errors = False
            print("\nLOOP TEST FAILED")    


    def reverse_tests(self):

        try:
            # generate waveforms
            waveform1 = m.create_wave(['C2'], 'sine', 1/4)
            waveform2 = m.sequence(['C2'], 'sine', rhythm=1/8, duration=1/4)

            # test method
            waveform1.reverse()
            waveform2.reverse()

            # verify
            print('\nALL REVERSE TESTS SUCCESSFUL\n')

        except:
            self.no_errors = False
            print("\nREVERSE TEST FAILED") 


    def pan_tests(self):

        try:
            # generate waveforms
            waveform1 = m.create_wave(['C2'], 'sine', 1/4)
            waveform2 = m.sequence(['C2'], 'sine', rhythm=1/8, duration=1/4)

            # test methods
            waveform1.pan('C')
            waveform1.pan('L50')
            waveform2.pan('R50')

            # verify
            print('\nALL PAN TESTS SUCCESSFUL\n')

        except:
            self.no_errors = False
            print("\nPAN TEST FAILED")        


    def fade_tests(self):

        try:
            # generate waveforms
            waveform1 = m.create_wave(['C2'], 'sine', 1/4)
            waveform2 = m.sequence(['C2'], 'sine', rhythm=1/8, duration=1/4)

            # test method
            waveform1.fade(fade_in=1/8, fade_out=1/8, in_curve=3, out_curve=5)
            waveform2.fade(fade_in=1/4, fade_out=1/16)

            # verify
            print('\nALL FADE TESTS SUCCESSFUL\n')

        except:
            self.no_errors = False
            print("\nFADE TEST FAILED") 


    def LPF_tests(self):

        try:
            # generate waveforms
            waveform1 = m.create_wave(['C2'], 'saw1', 1/4)
            waveform2 = m.sequence(['C2'], 'square', rhythm=1/8, duration=1/4)

            # test method
            waveform1.LPF(cutoff=2000)
            waveform2.LPF(cutoff=700)

            # verify
            print('\nALL LPF TESTS SUCCESSFUL\n')

        except:
            self.no_errors = False
            print("\nLPF TEST FAILED")


    def HPF_tests(self):

        try:
            # generate waveforms
            waveform1 = m.create_wave(['C2'], 'saw1', 1/4)
            waveform2 = m.sequence(['C2'], 'square', rhythm=1/8, duration=1/4)

            # test method
            waveform1.HPF(cutoff=4000)
            waveform2.HPF(cutoff=1000)

            # verify
            print('\nALL HPF TESTS SUCCESSFUL\n')

        except:
            self.no_errors = False
            print("\nHPF TEST FAILED")


    def LFO_tests(self):

        try:
            # generate waveforms
            waveform1 = m.create_wave(['C2'], 'saw1', 1/4)
            waveform2 = m.sequence(['C2'], 'square', rhythm=1/8, duration=1/4)

            # test method
            waveform1.LFO(25, 'sine')
            waveform2.LFO(9, 'sine')

            # verify
            print('\nALL LFO TESTS SUCCESSFUL\n')

        except:
            self.no_errors = False
            print("\nLFO TEST FAILED")


    def delay_tests(self):

        try:
            # generate waveforms
            waveform1 = m.create_wave(['C2'], 'saw1', 1/4)
            waveform2 = m.sequence(['C2'], 'square', rhythm=1/8, duration=1/4)

            # test method
            waveform1.delay(time=1/16, feedback=5, mix=25, spread=50, stereo = True, start_side = 'L' , sync=True)
            waveform2.delay(time=1/24, feedback=10, mix=50, spread=50, stereo = False, start_side = 'R' , sync=False)

            # verify
            print('\nALL DELAY TESTS SUCCESSFUL\n')

        except:
            self.no_errors = False
            print("\nDELAY TEST FAILED")

tests = MusicCode_Tests()                    

""" run test functions """
tests.create_wave_tests()
tests.sequence_tests()
tests.rest_tests()
tests.sample_tests()
tests.arpeggio_tests()
tests.chord_tests()
tests.time_tests()
tests.time_edit_tests()
tests.vol_tests()
tests.bounce_tests()
tests.view_tests()
tests.loop_tests()
tests.reverse_tests()
tests.pan_tests()
tests.fade_tests()
tests.LPF_tests()
tests.HPF_tests()
tests.LFO_tests()
tests.delay_tests()

if tests.no_errors==True:
    print("\nAll Music-Code systems are working properly!")
else:
    print("\nErrors Detected")
