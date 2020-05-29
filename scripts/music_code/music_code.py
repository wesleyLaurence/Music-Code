# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 16:42:34 2020

@author: Wesley Laurence

Additional credit to Henry Franklin for help with delay & midi, and Owen Burrow for wavetable positions!
"""

# MySQL connection
from .sql_kit import SQL_Kit
import mysql.connector

# import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
from datetime import datetime
from scipy.signal import butter, lfilter, freqz
from sklearn.preprocessing import MinMaxScaler
import soundfile as sf
import IPython.display as ipd
import os
import sys
import warnings
from pathlib import Path
import getpass

# default style
plt.style.use('seaborn-dark-palette')


class MusicCode:    

    def __init__(self,bpm):

        
        """ User Settings """
        
        # set file path to your music-code program files location
        self.program_files_location = 'C:/Users/wesle/Desktop/Code Portfolio/music-code-master_v16/program files/'
        
        # Connect and update MySQL database
        self.database_connect=False
        self.userID = None
        self.password=None
    
        # sound settings
        self.Fs = 44100          
        self.bpm = bpm     
        self.time_mode = 'relative'   
        
        
        """ Music-Code Setup """
        
        # import clean chords dataset
        chords_blueprint_path = Path(self.program_files_location+'datasets/chords_blueprint.csv')
        chords_blueprint = pd.read_csv(chords_blueprint_path, encoding='latin1')
        
        #chords_blueprint = pd.read_excel(self.home_directory+"Program Files\\datasets"+'\\'+'chords_blueprint_v3.xlsx')
        self.chords_blueprint = chords_blueprint 
        self.all_chords = list(chords_blueprint['chord'])
        
        # Music Note --> Frequency
        # create dictionary to convert between musical notes and frequencies
        notes_freqs_path = Path(self.program_files_location+'datasets/frequency_musical notes.csv')
        notes_freqs = pd.read_csv(notes_freqs_path, encoding='latin1')
        
        # Sharps
        self.note_freq_table_sharp = dict(zip(list(notes_freqs['sharps']), list(notes_freqs['frequency'])))
        self.freq_note_table_sharp = dict(zip(list(notes_freqs['frequency']), list(notes_freqs['sharps'])))
        # Flats
        self.note_freq_table_flat = dict(zip(list(notes_freqs['flats']), list(notes_freqs['frequency'])))
        self.freq_note_table_flat = dict(zip(list(notes_freqs['frequency']), list(notes_freqs['flats'])))
        
        # SET UP SAMPLE LIBRARY
        self.kick = os.listdir(Path(self.program_files_location+'samples/kick'))
        self.kick.sort()
        self.snare = os.listdir(Path(self.program_files_location+'samples/snare'))
        self.snare.sort()
        self.clap = os.listdir(Path(self.program_files_location+'samples/clap'))
        self.clap.sort()
        self.hihat = os.listdir(Path(self.program_files_location+'samples/hihat'))
        self.hihat.sort()
        self.perc = os.listdir(Path(self.program_files_location+'samples/perc'))
        self.perc.sort()
        self.cymbal = os.listdir(Path(self.program_files_location+'samples/cymbal'))
        self.cymbal.sort()
        self.bass = os.listdir(Path(self.program_files_location+'samples/bass'))
        self.bass.sort()
        self.fx = os.listdir(Path(self.program_files_location+'samples/fx'))
        self.fx.sort()
        self.user = os.listdir(Path(self.program_files_location+'samples/user')) 
        self.user.sort()
        
        # set up archive library
        self.archive = os.listdir(Path(self.program_files_location+'archive')) 
        
        
    # GETTERS
    def get_bpm(self):
        return self.bpm
        
    def get_time_mode(self):
        return self.time_mode
    
    def get_database_connect(self):
        return self.database_connect
      
    # SETTERS
    def set_bpm(self, new_bpm):
        self.bpm = new_bpm
        
    def set_time_mode(self, time_mode):
        self.time_mode = time_mode   
        
    
    def connect(self):
        
        self.database_connect = True
        self.userID = input('User ID: ')
        self.password = getpass.getpass('Password: ')

        
    # Sound Wave Generator
    def create_wave(self, note_labels, wave_type, duration, wt_pos=1, wave_context="create_wave"):
        
        """ create_wave        

        Required Parameters
        note_labels: list of strings and/or integers. Strings are musical note labels i.e. ['C2','Ab4','G#2'] and integer values are frequencies measured in Hertz (Hz) i.e. [440, 220, 110]
        
        wave_type: string value representing the waveform shape in abbreviated form. Here are all the avaiable waveform shapes: 'sine', 'tri', 'saw1', 'saw2', 'square'. You can blend shapes like 'saw-tri'.
        
        duration: float or integer value representing the waveform duration in measures. For example 1/8 is an eighth note, based on the set BPM. 1 is a full measure/bar. 4 is 4 measures and so on

        Optional Parameters
        wt_pos: integer value defining the wavetable position. This parameter adjusts the tone & timbre of the sound
        
        """
        
        if self.time_mode == 'relative':
            rhythm_duration = (60/self.bpm)*4*(duration)
        else:
            rhythm_duration = duration
        final_waveform=np.array([0])

        # for each note in note_label
        for note_label in note_labels:
            if isinstance(note_label, int) or isinstance(note_label, float):
                freq = note_label 
            else: 
                try:
                    freq = self.note_freq_table_sharp[note_label] # frequency
                except:
                    freq = self.note_freq_table_flat[note_label] # frequency

                    
            # number of samples in total file
            sample = self.Fs*rhythm_duration 
            
            # create wave
            x = np.arange(sample)

            # waveform types 
            if wave_type == 'sine':
                waveform = (np.sin(2 * np.pi * freq * x / self.Fs)**wt_pos)*0.5

            elif wave_type == 'tri':
                waveform = (signal.sawtooth(t=2 * np.pi * freq * x / self.Fs,width=.5)**wt_pos)*0.5

            elif wave_type == 'saw1':
                waveform = (signal.sawtooth(t=2 * np.pi * freq * x / self.Fs,width=1)**wt_pos)*.2

            elif wave_type == 'saw2':
                waveform = (signal.sawtooth(t=2 * np.pi * freq * x / self.Fs,width=0)**wt_pos)*.2

            elif wave_type == 'square':
                waveform = (signal.square(t=2 * np.pi * freq * x / self.Fs)**wt_pos)*.2
                
            elif wave_type == 'sine-tri' or wave_type == 'tri-sine':
                waveform = (np.sin(2 * np.pi * freq * x / self.Fs)**wt_pos)*0.21 + (signal.sawtooth(t=2 * np.pi * freq * x / self.Fs,width=.5)**wt_pos)*0.21
            elif wave_type == 'sine-saw'or wave_type == 'saw-sine':
                waveform = (np.sin(2 * np.pi * freq * x / self.Fs)**wt_pos)*0.21 + (signal.sawtooth(t=2 * np.pi * freq * x / self.Fs,width=1)**wt_pos)*.1
                
            elif wave_type == 'sine-square'or wave_type == 'square-sine':
                waveform = (np.sin(2 * np.pi * freq * x / self.Fs)**wt_pos)*0.21 + (signal.square(t=2 * np.pi * freq * x / self.Fs)**wt_pos)*.1
                
            elif wave_type == 'saw-square'or wave_type == 'square-saw':
                waveform = (signal.sawtooth(t=2 * np.pi * freq * x / self.Fs,width=1)**wt_pos)*.1 + (signal.square(t=2 * np.pi * freq * x / self.Fs)**wt_pos)*.1
                
            elif wave_type == 'tri-saw'or wave_type == 'saw-tri':
                waveform = (signal.sawtooth(t=2 * np.pi * freq * x / self.Fs,width=.5)**wt_pos)*0.21 + (signal.sawtooth(t=2 * np.pi * freq * x / self.Fs,width=1)**wt_pos)*.1
                
            elif wave_type == 'tri-square'or wave_type == 'square-tri':
                waveform = (signal.sawtooth(t=2 * np.pi * freq * x / self.Fs,width=.5)**wt_pos)*0.21 + (signal.square(t=2 * np.pi * freq * x / self.Fs)**wt_pos)*.1
                
            # sum current waveform and new waveform, then move to next note in note_labels list    
            final_waveform=final_waveform+waveform
            
        
        # while volume is quiet, gradually make louser until threshold is reached
        while abs(final_waveform).max() < .5:
            final_waveform = final_waveform*1.25

        # while volume is clipping, make quiter
        while abs(final_waveform).max() > 1:
            final_waveform = final_waveform*.75

        # convert to wave object    
        self.waveform = Wave(final_waveform, self.bpm, self.time_mode, self.program_files_location, self.database_connect, self.userID, self.password)
        
        # subtle fade in to avoid audible clicks and pops
        self.waveform = self.waveform.fade(fade_in=1/128,fade_out=1/128)
        
        
        # update MySQL database 
        if self.database_connect == True and wave_context=='create_wave':
            db = SQL_Kit(userID=self.userID, password=self.password, database='musiccode')
            db.createwave_table(note_labels, wave_type, wt_pos, duration, self.get_bpm(), self.get_time_mode())     
            
        # if no database connection, pass
        else:
            pass
          
        return self.waveform

    # Wave Sequencer
    def sequence(self, note_labels, wave_type, rhythm, duration, wt_pos=1, arp_type = 'up', fade_in=1/128, fade_out = 1/128, in_curve = False, out_curve=False, wave_context='sequence'):
        
        """ sequence 

        Required Parameters
        note_labels: list of strings and/or integers. Strings are musical note labels i.e. ['C2','Ab4','G#2'] and integer values are frequencies measured in Hertz (Hz) i.e. [440, 220, 110]
        
        wave_type: string value representing the waveform shape in abbreviated form. Here are all the avaiable waveform shapes: 'sine', 'tri', 'saw1', 'saw2', 'square'. You can blend shapes like 'saw-tri'.
        
        duration: float or integer value representing the waveform duration in measures. For example 1/8 is an eighth note, based on the set BPM. 1 is a full measure/bar. 4 is 4 measures and so on

        Optional Parameters
        wt_pos: integer value defining the wavetable position. This parameter adjusts the tone & timbre of the sound
        
        """
        
        # rhythm & duration
        rhythm_duration = ((60/self.bpm)*4)*(rhythm)
        total_duration = ((60/self.bpm)*4)*(duration)
        total_samples = int(round(total_duration*44100))

        # sample rate for WAV audio
        sample_rate=self.Fs    

        # container for master waveform
        master_wave = np.zeros(1)
        
        # iterate through all items in note_labels
        for note in note_labels:
            
            # if note is wave type
            if type(note).__name__ == 'Wave':
                waveform = note
            
            # if note is float type
            elif isinstance(note, float) or isinstance(note, int):
                waveform = self.create_wave([note], wave_type, rhythm, wt_pos, wave_context).fade(fade_in,in_curve,fade_out,out_curve)
                
            # if note is string type
            elif isinstance(note, str):
                if note== 'rest':
                    waveform = self.rest(rhythm)
                else:
                    # generate waveform for note in note list
                    waveform = self.create_wave([note], wave_type, rhythm, wt_pos, wave_context).fade(fade_in,in_curve,fade_out,out_curve)

            # concatenate new waveform to master_waveform
            master_wave=self.join_waves((master_wave,waveform),wave_context)

        if arp_type == 'up':

            # single loop through each note in note_labels
            one_loop = master_wave

            # concatenate master_wave until it reaches full duration
            while master_wave.shape[0] < total_samples:
                master_wave = self.join_waves((master_wave,one_loop),wave_context)

        elif arp_type == 'down':

            # flip waveform to get descending order
            master_wave = np.flip(master_wave)
            one_loop = master_wave

            # concatenate master_wave until it reaches full duration
            while master_wave.shape[0] < total_samples:
                master_wave = self.join_waves((master_wave,one_loop),wave_context)

        elif arp_type == 'up-down':

            # flip waveform to get descending order
            master_wave = self.join_waves((master_wave,np.flip(master_wave)),wave_context)
            one_loop = master_wave

            # concatenate master_wave until it reaches full duration
            while master_wave.shape[0] < total_samples:
                master_wave = self.join_waves((master_wave,one_loop),wave_context)

        elif arp_type == 'down-up':

            # flip waveform to get descending order
            master_wave = self.join_waves((np.flip(master_wave),master_wave),wave_context)
            one_loop = master_wave

            # concatenate master_wave until it reaches full duration
            while master_wave.shape[0] < total_samples:
                master_wave = self.join_waves((master_wave,one_loop),wave_context)


        master_wave = master_wave[:total_samples]
        self.waveform = Wave(master_wave, self.bpm, self.time_mode, self.program_files_location, self.database_connect, self.userID, self.password)
        
        # update MySQL database 
        if self.database_connect == True and wave_context=='sequence':
            db = SQL_Kit(userID=self.userID, password=self.password, database='musiccode')
            db.sequence_table(note_labels, wave_type, wt_pos, rhythm, duration, arp_type, fade_in, fade_out, in_curve, out_curve, self.bpm, self.time_mode)      
        # if no database connection, pass
        else:
            pass
           
        return self.waveform
      
        
    # Silence   
    def rest(self, duration):
        
        """ rest

        Required Parameters
        duration: float or integer value representing the waveform duration in bars. For example 1/8 is an eighth note, based on the set BPM. 1 is a full measure/bar. 4 is 4 measures and so on
        
        """
        
        input_rhythm = duration
        if self.time_mode == 'relative':
            rhythm_duration = (60/self.bpm)*4*(duration)
        else:
            rhythm_duration = duration
        
        self.waveform = Wave(np.zeros(round(self.Fs*rhythm_duration)), self.bpm, self.time_mode, self.program_files_location, self.database_connect, self.userID, self.password)   
        
        # update MySQL database 
        if self.database_connect == True:
            db = SQL_Kit(userID=self.userID, password=self.password, database='musiccode')
            db.rest_table(duration, self.bpm, self.time_mode)     
        # if no database connection, pass
        else:
            pass
            
        return self.waveform
        
        
    # generate chord arpeggio
    def arpeggio(self, chord_label, start_note, wave_type, rhythm, duration, tonal_system=12, arp_type='up', fade_in=1/128, fade_out = 1/128, in_curve=False, out_curve=False, wt_pos=1, wave_context='arpeggio'):
        
        """ arpeggio

        Required Parameters
        chord_label: 
        
        start_note:
        
        wave_type: string value representing the waveform shape in abbreviated form. Here are all the avaiable waveform shapes: 'sine', 'tri', 'saw1', 'saw2', 'square'. You can blend shapes like 'saw-tri'.
        
        rhythm: 
        
        duration: float or integer value representing the waveform duration in measures. For example 1/8 is an eighth note, based on the set BPM. 1 is a full measure/bar. 4 is 4 measures and so on

        Optional
        tonal_system:
        
        fade_in:
        
        fade_out:
        
        in_curve:
        
        out_curve:
        
        wt_pos: integer value defining the wavetable position. This parameter adjusts the tone & timbre of the sound
        
        """
    
        rhythm_duration = ((60/self.bpm)*4)*(rhythm)
      
        if isinstance(start_note, int) or isinstance(start_note, float):
            freq = start_note

        else: 
            try:
                freq = self.note_freq_table_sharp[start_note] # frequency
            except:
                freq = self.note_freq_table_flat[start_note] # frequency

    
        log_scale = float(2**(1/tonal_system))
        scale_freqs = [freq]
        scale_wave = np.array([0])
    
        degrees_in_chord = np.array(self.chords_blueprint[self.chords_blueprint['chord']==chord_label].iloc[0,1].split()).astype(int)
        max_degree = degrees_in_chord.max()
    
        for i in range(max_degree):
            freq=round(freq*log_scale,3)
            scale_freqs.append(freq)    
            
        degree_freqs_main = []
        for degree in list(degrees_in_chord):
            degree_freq = scale_freqs[degree]
            degree_freqs_main.append(degree_freq)

        #sequence(self, note_labels, wave_type, rhythm, duration, arp_type = 'up', pan_pos = 'C', fade_type='line', fade_length = 1/128, curve_slope = 3, fade_in=True, fade_out=True, wt_pos=1)
        final_waveform = self.sequence(degree_freqs_main,wave_type=wave_type,rhythm=rhythm,duration=duration,arp_type=arp_type,fade_in=fade_in,in_curve=in_curve,fade_out=fade_out,out_curve=out_curve, wt_pos=wt_pos,wave_context='arpeggio')
        self.waveform = Wave(final_waveform, self.bpm, self.time_mode, self.program_files_location, self.database_connect, self.userID, self.password)
        
        # update MySQL database 
        if self.database_connect == True:
            db = SQL_Kit(userID=self.userID, password=self.password, database='musiccode')
            db.arpeggio_table(chord_label, start_note, wave_type, rhythm, duration, tonal_system, arp_type, fade_in, fade_out, in_curve, out_curve, wt_pos, self.bpm, self.time_mode)     
        # if no database connection, pass
        else:
            pass
        
        return self.waveform
    
    
    # generate chord
    def chord(self, chord_label, start_note, wave_type, duration, tonal_system=12, fade_in=1/128, fade_out=1/128, in_curve=False, out_curve=False, wt_pos=1, wave_context='chord'):
        
        """ chord

        Required Parameters
        chord_label: 
        
        start_note:
        
        wave_type: string value representing the waveform shape in abbreviated form. Here are all the avaiable waveform shapes: 'sine', 'tri', 'saw1', 'saw2', 'square'. You can blend shapes like 'saw-tri'.
        
        duration: float or integer value representing the waveform duration in measures. For example 1/8 is an eighth note, based on the set BPM. 1 is a full measure/bar. 4 is 4 measures and so on

        Optional
        tonal_system:
        
        fade_in:
        
        fade_out:
        
        in_curve:
        
        out_curve:
        
        wt_pos: integer value defining the wavetable position. This parameter adjusts the tone & timbre of the sound
        
        """
    
        if isinstance(start_note, int) or isinstance(start_note, float):
            freq = start_note
        else: 
            try:
                freq = self.note_freq_table_sharp[start_note] # frequency
            except:
                freq = self.note_freq_table_flat[start_note] # frequency
                
        log_scale = float(2**(1/tonal_system))
        scale_freqs = [freq]
        scale_wave = np.array([0])
    
        degrees_in_chord = np.array(self.chords_blueprint[self.chords_blueprint['chord']==chord_label].iloc[0,1].split()).astype(int)
        max_degree = degrees_in_chord.max()
    
        for i in range(max_degree):
            freq=round(freq*log_scale,3)
            scale_freqs.append(freq)    
            
        degree_freqs_main = []
        for degree in list(degrees_in_chord):
            degree_freq = scale_freqs[degree]
            degree_freqs_main.append(degree_freq)

        final_waveform = self.create_wave(degree_freqs_main,wave_type,duration,wt_pos=wt_pos,wave_context='chord')
        
        self.waveform = Wave(final_waveform, self.bpm, self.time_mode, self.program_files_location, self.database_connect, self.userID, self.password)
        self.waveform = self.waveform.fade(fade_in=fade_in,fade_out=fade_out,in_curve=in_curve ,out_curve=out_curve)
        
        # update MySQL database 
        if self.database_connect == True:
            db = SQL_Kit(userID=self.userID, password=self.password, database='musiccode')
            db.chord_table(chord_label, start_note, wave_type, duration, tonal_system, fade_in, fade_out, in_curve, out_curve, wt_pos, self.bpm, self.time_mode)     
        # if no database connection, pass
        else:
            pass
        
        return self.waveform
    
    
    # join (concatenate) waveforms into sequence
    def join_waves(self, waves_tuple, join_context='user'):
        
        """ join_waves 

        Required Parameters
        waves_tuple: a tuple data type of all wave objects you want to add together

        """
        
        wave_channels = []
        for waveform in waves_tuple:
            wave_channels.append(waveform.ndim)
        
        if 2 in wave_channels:
            stereo_waves = []
            for waveform in waves_tuple:
                
                if waveform.ndim == 2:
                    stereo_waves.append(waveform)
                        
                elif waveform.ndim == 1:
                    waveform = np.array([waveform,waveform]).T
                    stereo_waves.append(waveform)
       
            master = np.concatenate(tuple(stereo_waves))                 
        else:
             master = np.concatenate(waves_tuple)
        
        self.waveform = master
        self.waveform = Wave(self.waveform, self.bpm, self.time_mode, self.program_files_location, self.database_connect, self.userID, self.password)
        
        
        return self.waveform
    
    
    # add waveforms to create harmony
    def add_waves(self, waves_tuple, add_context='user'):
        
        """ add_waves

        Required Parameters
        waves_tuple: 

        """
        
        sample_counts = []
        for waveform in waves_tuple:
            sample_counts.append(len(waveform))
        sample_cutoff = min(sample_counts)
   
        channel_types = []
        for waveform in waves_tuple:
            if waveform.ndim == 2:
                channel_types.append('stereo')
            else:
                channel_types.append('mono')
         
        stereo_waves = []
        if 'stereo' in channel_types:
            for waveform in waves_tuple:
                if waveform.ndim == 2:
                    stereo_waves.append(np.array(waveform[:sample_cutoff]))
                else:
                    waveform = np.array([waveform[:sample_cutoff],waveform[:sample_cutoff]]).T
                    stereo_waves.append(waveform)
       
            master = np.array([np.zeros(1),np.zeros(1)]).T        
            
            for waveform in stereo_waves:
                master = np.add(master,waveform)
        
        else: 
            master = np.zeros(1)
            for waveform in waves_tuple: 
                master = np.add(master,waveform)[:sample_cutoff] 
     
        
        # while volume is quiet, gradually make louser until threshold is reached
        while float(abs(master).max()) < .5:
            master = master*1.5

        # while volume is clipping, make quiter
        while float(abs(master).max()) > 1:
            master = master*.75
        
        self.waveform = master 
        self.waveform = Wave(self.waveform, self.bpm, self.time_mode, self.program_files_location, self.database_connect, self.userID, self.password)
            
        return self.waveform
    
    
    # load WAV file from sample library  
    def sample(self, sound_folder, sample_id):
        
        """ sample 

        Required Parameters
        sound_folder:
        
        sample_id: 

        """

        try:
            if sound_folder == 'kick':
                # if user passes in file name in string format
                if isinstance(sample_id,str):
                    file_path = Path(self.program_files_location+'samples/kick/'+sample_id)
                # if user passes in file id in integer format
                elif isinstance(sample_id,int):
                    file_path = Path(self.program_files_location+'samples/kick/'+self.kick[sample_id])
                   
            elif sound_folder == 'snare':
                # if user passes in file name in string format
                if isinstance(sample_id,str):
                    file_path = Path(self.program_files_location+'samples/snare/'+sample_id)
                # if user passes in file id in integer format
                else:
                    file_path = Path(self.program_files_location+'samples/snare/'+self.snare[sample_id])
             
            elif sound_folder == 'clap':
                # if user passes in file name in string format
                if isinstance(sample_id,str):
                    file_path = Path(self.program_files_location+'samples/clap/'+sample_id)
                # if user passes in file id in integer format
                else:
                    file_path = Path(self.program_files_location+'samples/clap/'+self.clap[sample_id])
              
            elif sound_folder == 'hihat':
                # if user passes in file name in string format
                if isinstance(sample_id,str):
                    file_path = Path(self.program_files_location+'samples/hihat/'+sample_id)
                # if user passes in file id in integer format
                else:
                    file_path = Path(self.program_files_location+'samples/hihat/'+self.hihat[sample_id])
              
            elif sound_folder == 'perc':
                # if user passes in file name in string format
                if isinstance(sample_id,str):
                    file_path = Path(self.program_files_location+'samples/perc/'+sample_id)
                # if user passes in file id in integer format
                else:
                    file_path = Path(self.program_files_location+'samples/perc/'+self.perc[sample_id])
              
            elif sound_folder == 'cymbal':
                # if user passes in file name in string format
                if isinstance(sample_id,str):
                    file_path = Path(self.program_files_location+'samples/cymbal/'+sample_id)
                # if user passes in file id in integer format
                else:
                    file_path = Path(self.program_files_location+'samples/cymbal/'+self.cymbal[sample_id])     
                
            elif sound_folder == 'bass':
                # if user passes in file name in string format
                if isinstance(sample_id,str):
                    file_path = Path(self.program_files_location+'samples/bass/'+sample_id)
                # if user passes in file id in integer format
                else:
                    file_path = Path(self.program_files_location+'samples/bass/'+self.bass[sample_id])
                
            elif sound_folder == 'user':
                # if user passes in file name in string format
                if isinstance(sample_id,str):
                    file_path = Path(self.program_files_location+'samples/user/'+sample_id)
                # if user passes in file id in integer format
                else:
                    file_path = Path(self.program_files_location+'samples/user/'+self.user[sample_id])
              
            elif sound_folder == 'fx':
                # if user passes in file name in string format
                if isinstance(sample_id,str):
                    file_path = Path(self.program_files_location+'samples/fx/'+sample_id)
                # if user passes in file id in integer format
                else:
                    file_path = Path(self.program_files_location+'samples/fx/'+self.fx[sample_id])   
              
            elif sound_folder == 'archive':
                # if user passes in file name in string format
                if isinstance(sample_id,str):
                    file_path = Path(self.program_files_location+'samples/archive/'+sample_id)
                # if user passes in file id in integer format
                else:
                    file_path = Path(self.program_files_location+'samples/user/'+self.user[sample_id])
            
            data, sr = sf.read(file_path)    
        
        except:
            print('Sample could not be found')
                
        self.waveform = Wave(data, self.bpm, self.time_mode, self.program_files_location, self.database_connect, self.userID, self.password)
        duration_seconds = len(self.waveform)/self.Fs
        
        # SQL data
        file_name = str(file_path).split('\\')[-1]
        duration = round(self.waveform.shape[0]/self.Fs, 3)
        num_channels = int(self.waveform.ndim)
        sample_rate = int(sr)
        max_vol = round(float(self.waveform.max()),3)
        
        # update MySQL database 
        if self.database_connect == True:
            db = SQL_Kit(userID=self.userID, password=self.password, database='musiccode')
            db.sample_table(sound_folder, file_name, duration, num_channels, sample_rate, max_vol)     
        # if no database connection, pass
        else:
            pass
        
        return self.waveform
            

"""The wave object is the primary data structure for audio waveforms in music-code. Wave is a sub class of a numpy array. The wave object has the & efficiency of a numpy array and is extended with custom methods for audio editing. This is built for music making, experimentation with DSP, data production or any other way you can think to use it!"""

class Wave(np.ndarray):
    
    
    # initialize wave data type
    # sub class of np.array
    
    def __new__(cls, waveform, bpm, time_mode, program_files_location, database_connect, userID, password):
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = np.asarray(waveform).view(cls)
        # add the new attribute to the created instance
        obj.waveform = obj
        # Finally, we must return the newly created object:
        return obj

    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        if obj is None: return
        self.waveform = getattr(obj, 'waveform', None)
       
    # Initialize all variables and import data
    
    def __init__(self, waveform, bpm, time_mode, program_files_location, database_connect, userID, password):
      
        self.waveform = waveform
        self.bpm = bpm
        self.time_mode = time_mode
        self.program_files_location = program_files_location
        self.database_connect = database_connect
        self.userID = userID
        self.password = password
        
        # Music Note --> Frequency
        # create dictionary to convert between musical notes and frequencies
        notes_freqs = pd.read_csv(Path(self.program_files_location+'datasets/frequency_musical notes.csv'), encoding='latin1')  
        
        # default sample rate
        self.Fs = 44100 
        
        # set up archive library
        self.archive = os.listdir(Path(program_files_location+'archive'))      
    
    
    def time(self):
        len_in_seconds = self.waveform.shape[0]/self.Fs

        # relative... does not work: new_time = ((60/self.bpm)*4*(len_in_seconds))/4
        
        waveform_duration_seconds = round(len_in_seconds,3)
        
        # update MySQL database 
        if self.database_connect == True:
            db = SQL_Kit(userID=self.userID, password=self.password, database='musiccode')
            db.timemethod_table(waveform_duration_seconds, self.bpm, self.time_mode)      
        # if no database connection, pass
        else:
            pass
        
        return print(waveform_duration_seconds)
    
    
    def vol(self, volume_level):
        self.waveform = Wave(self.waveform*volume_level, self.bpm, self.time_mode, self.program_files_location, self.database_connect, self.userID, self.password)
        
        # update MySQL database 
        if self.database_connect == True:
            db = SQL_Kit(userID=self.userID, password=self.password, database='musiccode')
            db.volume_table(volume_level)      
        # if no database connection, pass
        else:
            pass
        
        return self.waveform
    
    
    """  Audio export, playback and waveform visualizations """
     
    # export WAV to directory
    def bounce(self, file_name='user_playback.wav', sample_rate=44100, show_visual=True):
        
        data = self.waveform
        
        wav_files = os.listdir(Path(self.program_files_location+'archive'))

        if file_name in wav_files:
            file_name = file_name[:-4] + '_'+str(1)+'.wav'
        else:
            pass

        i=1
        while file_name in wav_files:
            i+=1
            file_name_items = file_name[:-4].split('_')
            iteration_num =int(file_name[:-4].split('_')[-1])
            iteration_num+=1
            file_name_items[-1] = str(iteration_num)
            file_name = '_'.join(file_name_items)+'.wav'
 
        length_seconds = data.shape[0]/sample_rate
        file_path = Path(self.program_files_location+'archive/'+file_name)
        
        sf.write(file_path, data, sample_rate)        
        
        if show_visual == True: 
            
            
            # if waveform is stereo...
            if self.waveform.T.shape[0] == 2:
                wave_l = self.waveform.T[0]
                wave_r = self.waveform.T[1]
                fig, axs = plt.subplots(2, sharex=True, sharey=True,figsize=(700/96, 200/96), dpi=96)
                
           
                if 'user_playback' in file_name:
                    pass
                else:
                    fig.suptitle(file_name)
                    
                axs[0].plot(wave_l, color='mediumblue')
                axs[1].plot(wave_r, color='mediumblue')
                plt.show()

            else:
                # if waveform is mono...
                wave_mono = self.waveform[0]

                wave_mono = self.waveform
                fig, axs = plt.subplots(1,figsize=(700/96, 200/96), dpi=96)
                
                if 'user_playback' in file_name:
                    pass
                else:
                    fig.suptitle(file_name)

                axs.plot(wave_mono,color='mediumblue')
                plt.show()     
        else:
            pass
        
        # SQL data
        duration = round(self.waveform.shape[0]/self.Fs, 3)
        max_vol = round(float(self.waveform.max()),3)
        num_channels = int(self.waveform.ndim)
        
        
        # update MySQL database 
        if self.database_connect == True:
            db = SQL_Kit(userID=self.userID, password=self.password, database='musiccode')
            db.bounce_table(file_name, duration, sample_rate, num_channels, max_vol)      
        # if no database connection, pass
        else:
            pass
          
        return ipd.Audio(file_path)
    
    
    def view(self, plot_type='all' ,title=None, freq_range=(20,20000)):
        
        
        # WAVE VISUAL functions

        def wave_view(waveform):
            fig,ax = plt.subplots(figsize=(12, 4),dpi=96)
            plt.subplot(212)
            plt.plot(waveform,color='mediumblue')
            plt.xlabel('Samples')
            plt.ylabel('Amplitude')
            plt.title('Waveform')
            plt.show()

        def spectrogram(waveform):

            signalData = waveform 
            samplingFrequency = 44100

            fig,ax = plt.subplots(figsize=(12, 4),dpi=96)
            plt.subplot(212)
            plt.specgram(signalData,Fs=samplingFrequency)
            plt.ylim(freq_range[0],freq_range[1])
            plt.xlabel('Time')
            plt.ylabel('Frequency')
            plt.title('Spectrogram')
            plt.show()

        def spectrum(waveform):
            """https://makersportal.com/blog/2018/9/13/audio-processing-in-python-part-i-sampling-and-the-fast-fourier-transform"""
            # sampling information
            Fs =self.Fs # sample rate
            N = len(waveform)
            t_vec = np.arange(N) # time vector for plotting


            # fourier transform and frequency domain
            #
            Y_k = np.fft.fft(waveform)[0:int(N/2)]/N # FFT function from numpy
            Y_k[1:] = 2*Y_k[1:] # need to take the single-sided spectrum only
            Pxx = np.abs(Y_k) # be sure to get rid of imaginary part

            f = Fs*np.arange((N/2))/N; # frequency vector

            # plotting
            fig,ax = plt.subplots(figsize=(12, 4),dpi=96)
            plt.plot(f,Pxx,linewidth=1,color='mediumblue')
            ax.grid(color='w', linestyle='-', linewidth=1, alpha=0.3)
            ax.set_xscale('log')
            ax.set_yscale('log')
            plt.title('Spectrum')
            plt.ylabel('Amplitude')
            plt.ylim(0.01,1)
            plt.xlabel('Frequency [Hz]')
            plt.xlim(freq_range[0],freq_range[1])
            plt.show()
        
        
        # if waveform is stereo
        if self.waveform.ndim == 2:
            wave_l = self.waveform.T[0]
            wave_r = self.waveform.T[1]
            summed_waveform = wave_l + wave_r

            if 'all' in plot_type:
                wave_view(summed_waveform)
                spectrum(summed_waveform)
                spectrogram(summed_waveform)
                
            elif 'wave' in plot_type:
                wave_view(summed_waveform)
            elif 'spectro' in plot_type:
                spectrogram(summed_waveform)
            elif 'spectrum' in plot_type:
                spectrum(summed_waveform)
         
        # if waveform is mono
        else:
            
            if 'all' in plot_type:
                wave_view(self.waveform)
                spectrum(self.waveform)
                spectrogram(self.waveform)
            elif 'wave' in plot_type:
                wave_view(self.waveform)
            elif 'spectro' in plot_type:
                spectrogram(self.waveform)
            elif 'spectrum' in plot_type:
                spectrum(self.waveform)
                       
        duration = round(self.waveform.shape[0]/self.Fs, 3)    
        
            # update MySQL database 
        if self.database_connect == True:
            db = SQL_Kit(userID=self.userID, password=self.password, database='musiccode')
            db.view_table(duration)      
        # if no database connection, pass
        else:
            pass
        
        
    """ Digital Signal Processing """
    
    def time_edit(self, duration,slice_from_end=False,mode='relative'):
        if mode == 'relative':
            new_time = (60/self.bpm)*4*(duration)
        elif mode == 'abs':
            new_time = duration
   
        original_duration_seconds = self.waveform.shape[0]/44100
        samples = int(np.round(new_time*self.Fs))
        
        # If waveform is stereo...
        if self.waveform.ndim == 2:
            
            # if new_time > old_time
            if int(new_time*self.Fs) > int(self.waveform.shape[0]):
                
                original_length = self.waveform.shape[0]
                
                new_length = new_time*self.Fs
                
                # create silence
                difference = int(new_length - original_length)
                silence = np.zeros(difference)
                m=MusicCode(self.bpm)
                final_waveform = m.join_waves((self.waveform,silence))
                self.waveform = final_waveform   
                
            # if new_time < old_time    
            else:
                new_waveform_l = self.waveform.T[0]
                new_waveform_r = self.waveform.T[1]
                
                if slice_from_end == False:
                    new_waveform_l=new_waveform_l[:samples]
                    new_waveform_r=new_waveform_r[:samples]    
                else:
                    difference = int(self.waveform.shape[0] - new_time*self.Fs)
                    new_waveform_l=new_waveform_l[difference:]
                    new_waveform_r=new_waveform_r[difference:]
                
                final_waveform = np.array((new_waveform_l,new_waveform_r)).T
                self.waveform = final_waveform
            
        # if waveform is mono
        else:
            # if new_time > old_time
            if int(new_time*self.Fs) > int(self.waveform.shape[0]):
                
                original_length = self.waveform.shape[0]
                new_length = new_time*self.Fs
                
                # create silence
                difference = np.round(new_length - original_length).astype(int)
                silence = np.zeros(difference)
                m=MusicCode(self.bpm)
                final_waveform = m.join_waves((self.waveform,silence))
                self.waveform = final_waveform  
            else:
                self.waveform = self.waveform[:samples]

        self.waveform = Wave(self.waveform, self.bpm, self.time_mode, self.program_files_location, self.database_connect, self.userID, self.password)
        
        # update MySQL database 
        if self.database_connect == True:
            db = SQL_Kit(userID=self.userID, password=self.password, database='musiccode')
            db.timeedit_table(original_duration_seconds, new_time, self.bpm, self.time_mode)      
        # if no database connection, pass
        else:
            pass
        
        return self.waveform
    
    
    def loop(self, num_loops):
        # stereo
        if self.waveform.ndim == 2:
            left_channel = np.tile(self.waveform.T[0],num_loops)
            right_channel = np.tile(self.waveform.T[1],num_loops)
            self.waveform = np.array((left_channel,right_channel)).T
        else:
            self.waveform = np.tile(self.waveform,num_loops)
            
        self.waveform = Wave(self.waveform, self.bpm, self.time_mode, self.program_files_location, self.database_connect, self.userID, self.password)    
        
        # update MySQL database 
        if self.database_connect == True:
            db = SQL_Kit(userID=self.userID, password=self.password, database='musiccode')
            db.loopmethod_table(num_loops, self.waveform.ndim, self.bpm, self.time_mode)      
        # if no database connection, pass
        else:
            pass
        
        return self.waveform 
    
    
    def reverse(self):
        self.waveform = Wave(np.flip(self.waveform), self.bpm, self.time_mode, self.program_files_location, self.database_connect, self.userID, self.password)
        
        len_in_seconds = self.waveform.shape[0]/self.Fs
        waveform_duration_seconds = round(len_in_seconds,3)
        
        # update MySQL database 
        if self.database_connect == True:
            db = SQL_Kit(userID=self.userID, password=self.password, database='musiccode')
            db.reverse_table(waveform_duration_seconds, self.waveform.ndim, self.bpm, self.time_mode)      
        # if no database connection, pass
        else:
            pass
        
        return self.waveform
   
    
    def pan(self, pan_pos):
        sql_pan_pos = pan_pos
        if pan_pos == 'C':
            degree=0
        else:
            degree= int(pan_pos[1:])
            pan_pos= pan_pos[0]  
        
        degree = degree*2
        # scale pan degree
        degree=np.flip(np.linspace(0,1,101))[degree]

        # if waveform is stereo..

        if self.waveform.ndim == 2:
            m=MusicCode(self.bpm)
            summed_wave = m.add_waves((self.waveform.T[0],self.waveform.T[1]))

            if pan_pos =='R' or pan_pos == 'r':
                l_channel = summed_wave*degree
                r_channel = summed_wave*1
                stereo_wave = np.array([l_channel,r_channel]).T
            elif pan_pos =='L' or pan_pos == 'l':
                l_channel = summed_wave*1
                r_channel = summed_wave*degree
                stereo_wave = np.array([l_channel,r_channel]).T
            elif pan_pos =='C' or pan_pos == 'c':
                l_channel = summed_wave*1
                r_channel = summed_wave*1
                stereo_wave = np.array([l_channel,r_channel]).T     
        
        # if waveform is mono
        elif self.waveform.ndim == 1:
          
            if pan_pos =='R' or pan_pos == 'r':
                l_channel = self.waveform*degree
                r_channel = self.waveform*1
                stereo_wave = np.array([l_channel,r_channel]).T
            elif pan_pos =='L' or pan_pos == 'l':
                l_channel = self.waveform*1
                r_channel = self.waveform*degree
                stereo_wave = np.array([l_channel,r_channel]).T
            elif pan_pos =='C' or pan_pos == 'c':
                stereo_wave =self.waveform
                
        self.waveform = stereo_wave
        self.waveform = Wave(self.waveform, self.bpm, self.time_mode, self.program_files_location, self.database_connect, self.userID, self.password)
        
        # update MySQL database 
        if self.database_connect == True:
            db = SQL_Kit(userID=self.userID, password=self.password, database='musiccode')
            db.pan_table(sql_pan_pos)      
        # if no database connection, pass
        else:
            pass
        
        return self.waveform 
    
    
    def fade(self, fade_in=1/128, in_curve = False, fade_out=1/128, out_curve = False, curve_type='exp'):

        if self.time_mode == 'relative':  
            fade_in_duration = int((60/self.bpm)*4*(fade_in)*self.Fs)
            fade_out_duration = int((60/self.bpm)*4*(fade_out)*self.Fs)
        else:
            fade_in_duration = int(fade_in*self.Fs)
            fade_out_duration = int(fade_out*self.Fs)
            
        waveform_length = len(self.waveform)
        
        # set waveform fade length limits
        if fade_in_duration > waveform_length:
            fade_in_duration = waveform_length
        elif fade_out_duration > waveform_length:
            fade_out_duration = waveform_length
        
        ### stereo waveform fade
        if self.waveform.ndim == 2:
            left_channel = self.waveform.T[0]
            right_channel = self.waveform.T[1]
            no_fade_length = int(100) 
            # fade in
            if fade_in != False:         
                # linear
                if in_curve == False:
                    fade_in_wave = np.linspace(0,1,fade_in_duration)
                    right_channel[:fade_in_duration] = right_channel[:fade_in_duration]*fade_in_wave
                    left_channel[:fade_in_duration] = left_channel[:fade_in_duration]*fade_in_wave   
                # exponential
                elif in_curve != False and curve_type=='exp':
                    fade_in_wave = np.exp(np.linspace(0,1,fade_in_duration))**in_curve
                    fade_in_wave=fade_in_wave.reshape((fade_in_duration,1))
                    scaler = MinMaxScaler()
                    scaler.fit(fade_in_wave)
                    fade_in_wave = scaler.transform(fade_in_wave)
                    fade_in_wave = fade_in_wave.reshape(fade_in_duration)
                    right_channel[:fade_in_duration] = right_channel[:fade_in_duration]*fade_in_wave
                    left_channel[:fade_in_duration] = left_channel[:fade_in_duration]*fade_in_wave                 
                # logarithmic
                elif in_curve != False and curve_type=='log':
                    fade_in_wave = np.log(np.linspace(0.000001,1,fade_in_duration))**in_curve
                    fade_in_wave=fade_in_wave.reshape((fade_in_duration,1))
                    scaler = MinMaxScaler()
                    scaler.fit(fade_in_wave)
                    fade_in_wave = scaler.transform(fade_in_wave)
                    fade_in_wave = fade_in_wave.reshape(fade_in_duration)
                    right_channel[:fade_in_duration] = right_channel[:fade_in_duration]*fade_in_wave
                    left_channel[:fade_in_duration] = left_channel[:fade_in_duration]*fade_in_wave   
            # no fade in
            else:
                fade_in_wave = np.linspace(0,1,no_fade_length)
                right_channel[:no_fade_length] = right_channel[:no_fade_length]*fade_in_wave
                left_channel[:no_fade_length] = left_channel[:no_fade_length]*fade_in_wave     
            # fade out
            if fade_out != False:
                # linear
                if out_curve == False:
                    fade_out_wave = np.linspace(0,1,fade_out_duration)
                    fade_out_wave = np.flip(fade_out_wave)
                    right_channel[-fade_out_duration:] = right_channel[-fade_out_duration:]*fade_out_wave 
                    left_channel[-fade_out_duration:] = left_channel[-fade_out_duration:]*fade_out_wave    
                # exponential
                elif out_curve != False and curve_type=='exp':
                    fade_out_wave = np.exp(np.linspace(0,1,fade_out_duration))**out_curve
                    fade_out_wave=fade_out_wave.reshape((fade_out_duration,1))
                    scaler = MinMaxScaler()
                    scaler.fit(fade_out_wave)
                    fade_out_wave = scaler.transform(fade_out_wave)
                    fade_out_wave = fade_out_wave.reshape(fade_out_duration)
                    fade_out_wave = np.flip(fade_out_wave)
                    right_channel[-fade_out_duration:] = right_channel[-fade_out_duration:]*fade_out_wave    
                    left_channel[-fade_out_duration:] = left_channel[-fade_out_duration:]*fade_out_wave            
                # logarithmic
                elif out_curve != False and curve_type=='log':
                    fade_out_wave = np.log(np.linspace(0.000001,1,fade_out_duration))**out_curve
                    fade_out_wave=fade_out_wave.reshape((fade_out_duration,1))
                    scaler = MinMaxScaler()
                    scaler.fit(fade_out_wave)
                    fade_out_wave = scaler.transform(fade_out_wave)
                    fade_out_wave = fade_out_wave.reshape(fade_out_duration)
                    fade_out_wave = np.flip(fade_out_wave)
                    right_channel[-fade_out_duration:] = right_channel[-fade_out_duration:]*fade_out_wave    
                    left_channel[-fade_out_duration:] = left_channel[-fade_out_duration:]*fade_out_wave   
            # no fade
            else:
                fade_out_wave = np.linspace(0,1,int(100))
                fade_out_wave = np.flip(fade_out_wave)
                right_channel[-int(100):] = right_channel[-int(100):]*fade_out_wave
                left_channel[-int(100):] = left_channel[-int(100):]*fade_out_wave
            # 2D stereo waveform
            self.waveform = np.array([left_channel,right_channel]).T  
        
        ### mono waveform fade
        else:     
            # fade in    
            if fade_in != False:    
                # linear
                if in_curve == False:
                    fade_in_wave = np.linspace(0,1,fade_in_duration)
                    self.waveform[:fade_in_duration] = self.waveform[:fade_in_duration]*fade_in_wave       
                # exponential
                elif (in_curve != False) and (curve_type=='exp'):
                    fade_in_wave = np.exp(np.linspace(0,1,fade_in_duration))**in_curve
                    fade_in_wave=fade_in_wave.reshape((fade_in_duration,1))
                    scaler = MinMaxScaler()
                    scaler.fit(fade_in_wave)
                    fade_in_wave = scaler.transform(fade_in_wave)
                    fade_in_wave = fade_in_wave.reshape(fade_in_duration)
                    self.waveform[:fade_in_duration] = self.waveform[:fade_in_duration]*fade_in_wave           
                # logarithmic
                elif (in_curve != False) and (curve_type=='log'):
                    fade_in_wave = np.log(np.linspace(0.000001,1,fade_in_duration))**in_curve
                    fade_in_wave=fade_in_wave.reshape((fade_in_duration,1))
                    scaler = MinMaxScaler()
                    scaler.fit(fade_in_wave)
                    fade_in_wave = scaler.transform(fade_in_wave)
                    fade_in_wave = fade_in_wave.reshape(fade_in_duration)
                    self.waveform[:fade_in_duration] = self.waveform[:fade_in_duration]*fade_in_wave               
            # no fade
            else:
                no_fade_length = int(100)
                fade_in_wave = np.linspace(0,1,no_fade_length)
                self.waveform[:no_fade_length] = self.waveform[:no_fade_length]*fade_in_wave          
            # fade out
            if fade_out != False:
                # linear
                if out_curve == False:
                    fade_out_wave = np.linspace(0,1,fade_out_duration)
                    fade_out_wave = np.flip(fade_out_wave)
                    self.waveform[-fade_out_duration:] = self.waveform[-fade_out_duration:]*fade_out_wave     
                # exponential
                elif (out_curve != False) and (curve_type=='exp'):
                    fade_out_wave = np.exp(np.linspace(0,1,fade_out_duration))**out_curve
                    fade_out_wave=fade_out_wave.reshape((fade_out_duration,1))
                    scaler = MinMaxScaler()
                    scaler.fit(fade_out_wave)
                    fade_out_wave = scaler.transform(fade_out_wave)
                    fade_out_wave = fade_out_wave.reshape(fade_out_duration)
                    fade_out_wave = np.flip(fade_out_wave)
                    self.waveform[-fade_out_duration:] = self.waveform[-fade_out_duration:]*fade_out_wave             
                # logarithmic
                elif (out_curve != False) and (curve_type=='log'):
                    fade_out_wave = np.log(np.linspace(0.000001,1,fade_out_duration))**out_curve
                    fade_out_wave=fade_out_wave.reshape((fade_out_duration,1))
                    scaler = MinMaxScaler()
                    scaler.fit(fade_out_wave)
                    fade_out_wave = scaler.transform(fade_out_wave)
                    fade_out_wave = fade_out_wave.reshape(fade_out_duration)
                    fade_out_wave = np.flip(fade_out_wave)
                    self.waveform[-fade_out_duration:] = self.waveform[-fade_out_duration:]*fade_out_wave                  
            # no fade
            else:
                fade_out_wave = np.linspace(0,1,int(100))
                fade_out_wave = np.flip(fade_out_wave)
                self.waveform[-int(100):] = self.waveform[-int(100):]*fade_out_wave 
        
        # update wave object
        self.waveform = Wave(self.waveform, self.bpm, self.time_mode, self.program_files_location, self.database_connect, self.userID, self.password)
        
        # update MySQL database 
        if self.database_connect == True:
            db = SQL_Kit(userID=self.userID, password=self.password, database='musiccode')
            db.fade_table(fade_in, fade_out, in_curve, out_curve, self.bpm, self.time_mode)      
        # if no database connection, pass
        else:
            pass
        
        return self.waveform
    
    
    # LOW PASS FILTER
    def LPF(self, cutoff, order=5):

        def butter_lowpass(cutoff, fs, order=5):
            nyq = 0.5 * fs
            normal_cutoff = cutoff / nyq
            b, a = butter(order, normal_cutoff, btype='low', analog=False)
            return b, a

        def butter_lowpass_filter(data, cutoff, fs, order=5):
            b, a = butter_lowpass(cutoff, fs, order=order)
            y = lfilter(b, a, self.waveform)
            return y

        if self.waveform.ndim == 1: 
            data = self.waveform
            # Filter the data, and plot both the original and filtered signals.
            filtered_wave = butter_lowpass_filter(data, cutoff, self.Fs, order)
            waveform = filtered_wave
            
        else: 
            unfiltered_l = self.waveform.T[0]
            unfiltered_r = self.waveform.T[1]
            
            filtered_l = butter_lowpass_filter(unfiltered_l,cutoff,self.Fs,order)
            filtered_r = butter_lowpass_filter(unfiltered_r,cutoff,self.Fs,order)
            
            waveform = np.array([filtered_l,filtered_r]).T
       
        self.waveform = Wave(waveform, self.bpm, self.time_mode, self.program_files_location, self.database_connect, self.userID, self.password)
        
        # update MySQL database 
        if self.database_connect == True:
            db = SQL_Kit(userID=self.userID, password=self.password, database='musiccode')
            db.LPF_table(cutoff, order)     
        # if no database connection, pass
        else:
            pass
        
        return self.waveform
    
    
    # HIGH PASS FILTER
    def HPF(self, cutoff, order=5):

        def butter_highpass(cutoff, fs, order=5):
            nyq = 0.5 * fs
            normal_cutoff = cutoff / nyq
            b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
            return b, a

        def butter_highpass_filter(data, cutoff, fs, order=5):
            b, a = butter_highpass(cutoff, fs, order=order)
            y = signal.filtfilt(b, a, self.waveform)
            return y

        if self.waveform.ndim == 1: 
            data = self.waveform
            # Filter the data, and plot both the original and filtered signals.
            filtered_wave = butter_highpass_filter(data, cutoff, self.Fs, order)
            
        elif self.waveform.ndim == 2:
            unfiltered_l = self.waveform.T[0]
            unfiltered_r = self.waveform.T[1]
            
            filtered_l = butter_highpass_filter(unfiltered_l,cutoff,self.Fs,order)
            filtered_r = butter_highpass_filter(unfiltered_r,cutoff,self.Fs,order)
            
            filtered_wave = np.array([filtered_l,filtered_r]).T
            
        # hide weird warning about multi dimensional tuple indexing cause... IDK that is    
        def fxn():
            warnings.warn("deprecated", DeprecationWarning)
        
        self.waveform = filtered_wave
        self.waveform = Wave(self.waveform, self.bpm, self.time_mode, self.program_files_location, self.database_connect, self.userID, self.password)
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fxn()
            
        # update MySQL database 
        if self.database_connect == True:
            db = SQL_Kit(userID=self.userID, password=self.password, database='musiccode')
            db.HPF_table(cutoff, order)      
        # if no database connection, pass
        else:
            pass
        
        return self.waveform
    
    
    def LFO(self, freq, wave_type, wt_pos=1,vol=1):   
        length = len(self.waveform)/44100
        
        freq *= 10
        m = MusicCode(self.bpm)
        m.time_mode='absolute'
        LFO_waveform = m.create_wave([freq],wave_type=wave_type,duration=length,wt_pos=wt_pos)*vol
        m.time_mode='relative'
        # stereo
        if self.waveform.ndim == 2:
            LFO_waveform = np.array([LFO_waveform,LFO_waveform]).T
        else:
            pass
        final_waveform = self.waveform*LFO_waveform
        self.waveform = Wave(final_waveform, self.bpm, self.time_mode, self.program_files_location, self.database_connect, self.userID, self.password)
        
        # update MySQL database 
        if self.database_connect == True:
            db = SQL_Kit(userID=self.userID, password=self.password, database='musiccode')
            db.lfo_table(freq, wave_type, wt_pos, vol)      
        # if no database connection, pass
        else:
            pass
        
        return self.waveform
    
    
    
    def delay(self, time, feedback, mix, spread, stereo = False, start_side = 'L' , sync=True):

        # waveform: wave you want to apply delay to
        # time: time between each delay (if sync == False, time unit is milliseconds... if sync == True, time is measured in rhythmic values like in other music-code methods)
        # feedback: the number of delays that occur before the signal reaches silence
        # sync: This is a boolean value that determines whether the delay is synced to the BPM or not

        # initial parameters
        vol = 1

        ### Calculate time values based on sync variable

        # BPM synced delay
        if sync:
            m = MusicCode(self.bpm)
            delay_rest = m.rest(time)

        # millisecond based delay
        else:
            # set time mode to absolute to work with seconds instead of BPM rhyhtmic values
            self.time_mode='absolute'

            # convert from MS to seconds
            m = MusicCode(self.bpm)
            delay_rest = m.rest(time/1000)

            # rest time mode
            self.time_mode='relative'

        # container for final waveform    
        master_waveform = self.waveform 

        # basline for volume calculation
        full_volume_wave = self.waveform * (mix/100)

        # volume factor
        vol_change = 1/feedback
        
        if start_side=='L':
            LorR=True
        else:
            LorR=False

        iteration=0
        while vol_change > 0:
            # reduce volume depending on feedback
            master_waveform = m.join_waves((master_waveform,delay_rest)) # Equalizes the length of the waveform that already exists
            toadd = m.join_waves((m.rest(time*iteration),full_volume_wave*vol_change)) # Creates next "echo"
            
            if stereo==True:
                if LorR:            
                    toadd = toadd.pan('L'+ str(spread))#Pan Left
                else:
                    toadd = toadd.pan('R'+ str(spread))#Pan Right
                    
            wave_length = len(master_waveform)
            master_waveform = m.add_waves((master_waveform,toadd[:wave_length])) # adds waves
            
            iteration +=1 # iterates
            vol_change = round(1-(iteration/feedback),3) # changes volume
            LorR = not LorR #Switches value of the start_side bool

        self.waveform = Wave(master_waveform, self.bpm, self.time_mode, self.program_files_location, self.database_connect, self.userID, self.password)
        
        # update MySQL database 
        if self.database_connect == True:
            db = SQL_Kit(userID=self.userID, password=self.password, database='musiccode')
            db.delay_table(time, feedback, mix, spread, stereo, sync, start_side, self.bpm, self.time_mode)      
        # if no database connection, pass
        else:
            pass

        return self.waveform