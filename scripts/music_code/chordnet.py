# import music-code modules
from music_code import MusicCode
from sql_kit import SQL_Kit

# audio
import pyaudio
import wave

# data
import numpy as np
import pandas as pd
import mysql.connector
from mysql.connector import MySQLConnection, Error

# plotting
import matplotlib.pyplot as plt
import seaborn

# GUI
from tkinter import *
import tkinter as tk

# more
from pathlib import Path
import datetime
import sys
import os
import threading
import getpass


# Generate random chord using music-code
class random_chord:
    
    def __init__(self):
        
        """ Generate chord with random quality, root note and waveform type """
        
        # initialize Music-Code
        self.m = MusicCode(bpm=120)
        
        # waveform types
        self.waveform_types = ['sine', 'tri', 'saw1', 'saw2', 'square', 'sine-tri', 'sine-saw', 'sine-square', 'saw-square', 'tri-saw', 'tri-square']
        
        # chord labels
        self.all_chord_labels = self.m.all_chords[:73]

        # select 4 octaves for root notes
        excess_notes_list = list(self.m.freq_note_table_sharp.values())  
        
        all_root_notes = []
        for item in excess_notes_list:
            if ('0' in item) or ('1' in item) or ('5' in item) or ('6' in item) or ('7' in item):
                pass
            else:
                all_root_notes.append(item)
                
        all_root_notes.sort() 
        self.all_root_notes = all_root_notes  
    
    def new_chord(self):
        
        """ Generate chord """
        
        # select random chord label
        chord_label_index = int(np.random.randint(0,len(self.all_chord_labels)))
        chord_label = self.all_chord_labels[chord_label_index]
        
        # select random root note
        root_note_index = int(np.random.randint(0,len(self.all_root_notes)))
        root_note = self.all_root_notes[root_note_index]

        # select random waveform type
        waveform_type_index = np.random.randint(0,len(self.waveform_types))
        waveform_type = self.waveform_types[waveform_type_index]
        
        # generate chord using music-code
        chord_waveform = self.m.chord(chord_label,root_note,waveform_type,2)
        
        # file name
        file_name_wav = root_note + ' '+ chord_label + '_' + waveform_type +'.wav'
        
        # bounce WAV audio
        chord_waveform.bounce(file_name_wav,show_visual=False)
        
        return file_name_wav


    
""" Tkinter GUI with MySQL database connection """    
    
class ChordNet(object):
    
    def __init__(self):
        
        # Connect and update MySQL database
        self.database_connect=False
        self.userID = None
        self.password=None
        
        # generate random chord
        self.c = random_chord()
        self.file_name = self.c.new_chord()
        
        # set WAV file path
        self.m = MusicCode(bpm=120)
        self.wav_file_path = self.m.program_files_location+"archive/"+self.file_name
        
        # parse data in file name
        self.chord_name = self.file_name.split('_')[0]
        self.waveform_type = self.file_name.split('_')[1][:-4]
        self.user_input = None
        
        # Tkinter attributes
        self.root= tk.Tk()
        self.canvas1 = tk.Canvas(self.root, width = 500, height = 350)
        self.label4 = None
        self.user_response = None
        self.HLP = None
    
    # MySQL connection, credentials required
    def connect(self):
        self.database_connect = True
        self.userID = input('User ID: ')
        self.password = getpass.getpass('Password: ')
    
    """Set up Tkinter GUI"""
    
    def play_audio(self):
        
        """ WAV audio playback """
        
        global is_playing
        chunk = 1024
        wf = wave.open(self.wav_file_path, 'rb')
        p = pyaudio.PyAudio()

        stream = p.open(
            format = p.get_format_from_width(wf.getsampwidth()),
            channels = wf.getnchannels(),
            rate = wf.getframerate(),
            output = True)

        data = wf.readframes(chunk)

        while data != '' and is_playing: # is_playing to stop playing
            stream.write(data)
            data = wf.readframes(chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def press_button_play(self):
        
        """ Tkinter Button for WAV audio playback """
        
        global is_playing
        global my_thread
        is_playing = False
        if not is_playing:
            is_playing = True
            my_thread = threading.Thread(target=self.play_audio)
            my_thread.start()
    
    def next_iteration(self):   
        self.c = random_chord()
        self.file_name = self.c.new_chord()
        self.wav_file_path = self.m.program_files_location+"archive/"+self.file_name
        self.chord_name = self.file_name.split('_')[0]
        self.waveform_type = self.file_name.split('_')[1][:-4]
        self.label4.destroy()  
    
    def select_maj(self):
        self.user_response='major'
        self.submission()
            
    def select_min(self):
        self.user_response='minor'
        self.submission()

    def select_dom(self):
        self.user_response='dominant'
        self.submission()

    def select_dim(self):
        self.user_response='diminished'
        self.submission()

    def select_aug(self):
        self.user_response='augmented'
        self.submission()
        
    def submission(self): 
        
        """ classify user response as correct or incorrect, display result to user, then update database """
        
        # classify chord prediction as either correct or incorrect
        if " "+self.user_response[:2] in self.chord_name:
            output = 'Correct'+'\n\n'+self.chord_name
        else:
            output = 'Incorrect'+'\n\n'+self.chord_name

        # create tkinter display to show user correct/incorrect message
        self.label4 = tk.Label(self.root, text= output)
        self.canvas1.create_window(250, 300, window=self.label4)
        
        # update MySQL database 
        if self.database_connect:
            
            # DATA PREP
            event_datetime = datetime.datetime.now()

            # actual label
            if ' maj' in self.chord_name:
                actual_label = 'major'
            elif ' min' in self.chord_name:
                actual_label = 'minor'
            elif ' dom' in self.chord_name:
                actual_label = 'dominant'
            elif ' dim' in self.chord_name:
                actual_label = 'diminished'
            elif ' aug' in self.chord_name:
                actual_label = 'augmented'
            
            # load user response
            response = self.user_response.lower()     
            
            # parse chord name to extract root note and chord label
            chord_root_note = self.chord_name.split(' ')[0]   
            chord_type = ""
            for item in self.chord_name.split(' ')[1:]:
                chord_type = str(chord_type +" "+item)
            chord_name_sql=chord_type[1:]
            
            # update database
            db = SQL_Kit(userID=self.userID, password=self.password, database='chordnet')
            db.chordlog_table(chord_root_note, chord_name_sql, response, actual_label, self.waveform_type)     
            
        # if no database connection, pass
        else:
            pass

    def main(self):
        
        """ MAIN """
        
        self.root.title("Chord Net")
        self.canvas1.pack()

        is_playing = False
        my_thread = None

        label1 = tk.Label(self.root, text='Chord Net')
        label1.config(font=('helvetica', 24))
        self.canvas1.create_window(250, 25, window=label1)

        label2 = tk.Label(self.root, text='What is the quality of this chord?')
        label2.config(font=('helvetica', 11))
        self.canvas1.create_window(250, 75, window=label2)

        label3 = tk.Label(self.root, text='major, minor, dominant, augmented or diminished')
        label3.config(font=('helvetica', 8))
        self.canvas1.create_window(250, 100, window=label3)

        button1 = Button(self.root, text="PLAY", command=self.press_button_play)
        self.canvas1.create_window(250, 150, window=button1)

        button3 = Button(self.root, text="NEXT", command=self.next_iteration)
        self.canvas1.create_window(250, 250, window=button3)
        
        button4 = Button(self.root, text="MAJ", command=self.select_maj)
        self.canvas1.create_window(150, 200, window=button4)

        button5 = Button(self.root, text="MIN", command=self.select_min)
        self.canvas1.create_window(200, 200, window=button5)

        button6 = Button(self.root, text="DOM", command=self.select_dom)
        self.canvas1.create_window(250, 200, window=button6)

        button7 = Button(self.root, text="DIM", command=self.select_dim)
        self.canvas1.create_window(300, 200, window=button7)

        button8 = Button(self.root, text="AUG", command=self.select_aug)
        self.canvas1.create_window(350, 200, window=button8)
        
        self.root.mainloop()
            
            
    """ SELECT * FROM table """
    def select_table(self, table):
        
        s = SQL_Kit(self.userID, self.password, 'chordnet')
        data = s.select_table(table)
        
        return data
    
            
    def KPI(self, total=True):
        
        """ Return key performance indicator (AVG % chords predicted correctly)"""
        
        data = self.select_table('ChordLog')
        correct = data[data['PredictedLabel'] == data['ActualLabel']]

        # % correctly predicted in chord net
        human_level_performance = (len(correct) / len(data)) * 100
        
        # round value
        human_level_performance = round(human_level_performance, 4)                          
        
        return human_level_performance
    
    
    def display(self):
        
        """ KPI MOVING AVERAGE """
        
        s = SQL_Kit(self.userID, self.password, 'chordnet')
        df = s.select_table('ChordLog')

        def day_of_year(datetime_entry):
            return datetime_entry.timetuple().tm_yday

        df['day_of_year'] = list(df.apply(lambda x: day_of_year(x['ChordDateTime']),axis=1))
        
        day_list = list(df['day_of_year'].unique())
        all_days = list(df['day_of_year'])
        
        averages = []
        for unique_day in day_list:
            
            data = df[df['day_of_year'] <= unique_day ].copy()
            
            correct = data[data['PredictedLabel'] == data['ActualLabel']]

            # % correctly predicted in chord net
            human_level_performance = (len(correct) / len(data)) * 100
            
            averages.append(human_level_performance)
        
        daily_count = df['day_of_year'].value_counts().sort_index()

        avg_move_df = pd.DataFrame([day_list,averages]).T
        avg_move_df.rename(columns={0: 'day_id', 1: 'moving_avg'},inplace=True)
        avg_move_df.set_index('day_id',inplace=True)
        
        fig1, ax1 = plt.subplots()
        ax1.plot(avg_move_df.index.astype(int),avg_move_df['moving_avg'], color='mediumspringgreen')
        ax1.set_title('KPI Moving AVG')
        ax1.set_xlabel('day_of_year')
        ax1.xaxis.set_ticks([min(all_days), max(all_days)])
        ax1.set_ylabel('% Correct')
        plt.show()
    
