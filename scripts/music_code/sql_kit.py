import mysql.connector
from datetime import datetime
import pandas as pd

class SQL_Kit(object):
    
    """ This kit enables access to the Music-Code MySQL database """
    
    def __init__(self, userID=None, password=None, database=None):
        
        # parameters
        self.userID = userID
        self.password = password
        self.database = database
        self.host = "localhost"
        self.port = 3306
        
    # get data from SQL table
    def select_table(self, table): 

        # connect to database
        try: 
            mydb = mysql.connector.connect(
            host = self.host,
            port = self.port,
            user = self.userID,
            passwd = self.password,
            database = self.database
            )
        except:
            print("Could not connect to database")

        try: 
            # get data using SQL SELECT statement
            mycursor = mydb.cursor()
            #mycursor.execute("SELECT * FROM %s;", (table) )
            
            mycursor.execute("""SELECT * FROM `%s`""" % (table))

            myresult = mycursor.fetchall()
            mycursor.close()

            # get column names
            mycursor = mydb.cursor()
            #mycursor.execute("SHOW columns FROM %s;", (table) )
            mycursor.execute("""SHOW columns FROM `%s`""" % (table))
            column_names = list(pd.DataFrame(mycursor.fetchall())[0])
            mycursor.close()
            mydb.close()

        except Error as e:
            mycursor.close()
            mydb.close()
            print(e)
        
        # convert data into pandas dataframe
        df = pd.DataFrame(myresult,columns=column_names)
        df.set_index(column_names[0],inplace=True)

        return df
      
    def insert_row(self, sql, val):   
        """ 
        Required Parameters
        sql: a string of the SQL code you want executed.
        
        val: a tuple of all values being loaded into SQL table
        """   
        
        # connect to database
        try: 
            mydb = mysql.connector.connect(
            host = self.host,
            port = self.port,
            user = self.userID,
            passwd = self.password,
            database = self.database
            )
        except:
            print("Could not connect to database")
            
      
        try: 
            mycursor = mydb.cursor()
            mycursor.execute(sql, val)
            mydb.commit()
            mycursor.close()
            mydb.close()

        except Error as e:
            mycursor.close()
            mydb.close()
            print(e)
            
    # MusiCode class updates
    
    def createwave_table(self, note_labels, wave_type, wt_pos, duration, bpm, time_mode):         
            sql_note_labels = ""
            for note_label in note_labels:
                sql_note_labels = sql_note_labels+" "+str(note_label)
            sql_note_labels = sql_note_labels[1:]

            sql = "INSERT INTO createwave (NoteLabels, WaveType, WtPos, Duration, BPM, TimeMode, UserID, EventDateTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" 
            val = (sql_note_labels, wave_type, wt_pos, duration, bpm, time_mode, self.userID, datetime.now())     
            self.insert_row(sql,val)
            
                       
    def sequence_table(self, note_labels, wave_type, wt_pos, rhythm, duration, arp_type, fade_in, fade_out, in_curve, out_curve, bpm, time_mode):
            sql_note_labels = ""
            for note_label in note_labels:
                sql_note_labels = sql_note_labels+" "+str(note_label)
            sql_note_labels = sql_note_labels[1:]
 
            sql = "INSERT INTO sequence (NoteLabels, WaveType, WtPos, Rhythm, Duration, ArpType, FadeIn, FadeOut, InCurve, OutCurve, BPM, TimeMode, UserID, EventDateTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"          
            val = (sql_note_labels, wave_type, wt_pos, rhythm, duration, arp_type, fade_in, fade_out, in_curve, out_curve, bpm, time_mode, self.userID, datetime.now())  
            self.insert_row(sql,val) 
                
                
    def rest_table(self, rhythm, bpm, time_mode):
            sql = "INSERT INTO rest (Rhythm, BPM, TimeMode, UserID, EventDateTime) VALUES (%s, %s, %s, %s, %s)"            
            val = (rhythm, bpm, time_mode, self.userID, datetime.now())             
            self.insert_row(sql,val)
            
            
    def chord_table(self, chord_label, start_note, wave_type, duration, tonal_system, fade_in, fade_out, in_curve, out_curve, wt_pos, bpm, time_mode):       
            sql = "INSERT INTO chord (ChordLabel, RootNote, WaveType, WtPos, Duration, TonalSystem, FadeIn, FadeOut, InCurve, OutCurve, BPM, TimeMode, UserID, EventDateTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"           
            val = (chord_label, start_note, wave_type, wt_pos, duration, tonal_system, fade_in, fade_out, in_curve, out_curve, bpm, time_mode, self.userID, datetime.now())             
            self.insert_row(sql,val)
            
            
    def arpeggio_table(self, chord_label, start_note, wave_type, rhythm, duration, tonal_system, arp_type, fade_in, fade_out, in_curve, out_curve, wt_pos, bpm, time_mode):          
            sql = "INSERT INTO arpeggio (ChordLabel, RootNote, WaveType, WtPos, Rhythm, Duration, ArpType, TonalSystem, FadeIn, FadeOut, InCurve, OutCurve, BPM, TimeMode, UserID, EventDateTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"           
            val = (chord_label, start_note, wave_type, wt_pos, rhythm, duration, arp_type, tonal_system, fade_in, fade_out, in_curve, out_curve, bpm, time_mode, self.userID, datetime.now())             
            self.insert_row(sql,val)
            
            
    def joinwaves_table(self, total_waves, num_channels, join_context):          
            sql = "INSERT INTO joinwaves (TotalWaves, NumChannels, JoinContext, UserID, EventDateTime) VALUES (%s, %s, %s, %s, %s)" 
            val = (total_waves, num_channels, join_context, self.userID, datetime.now())           
            self.insert_row(sql,val)
            
            
    def addwaves_table(self, total_waves, num_channels, add_context):           
            sql = "INSERT INTO addwaves (TotalWaves, NumChannels, AddContext, UserID, EventDateTime) VALUES (%s, %s, %s, %s, %s)"      
            val = (total_waves, num_channels, add_context, self.userID, datetime.now())            
            self.insert_row(sql,val)
            
            
    def sample_table(self, sound_folder, file_name, duration, num_channels, sample_rate, max_vol):          
            sql = "INSERT INTO sample (SoundCategory, FileName, Duration, NumChannels, SampleRate, MaxVol, UserID, EventDateTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"           
            val = (sound_folder, file_name, duration, num_channels, sample_rate, max_vol, self.userID, datetime.now())            
            self.insert_row(sql,val)
    
    
    # wave class updates
    
    def timemethod_table(self, duration, bpm, time_mode):
            sql = "INSERT INTO timemethod (Duration, BPM, TimeMode, UserID, EventDateTime) VALUES (%s, %s, %s, %s, %s)"         
            val = (duration, bpm, time_mode, self.userID, datetime.now())          
            self.insert_row(sql,val)
            
            
    def timeedit_table(self, old_duration, new_duration, bpm, time_mode):
            sql = "INSERT INTO timeedit (OldDuration, NewDuration, BPM, TimeMode, UserID, EventDateTime) VALUES (%s, %s, %s, %s, %s, %s)"           
            val = (old_duration, new_duration, bpm, time_mode, self.userID, datetime.now())            
            self.insert_row(sql,val)
            
            
    def volume_table(self, volume_factor):
            sql = "INSERT INTO volume (VolumeFactor, UserID, EventDateTime) VALUES (%s, %s, %s)"       
            val = (volume_factor, self.userID, datetime.now())           
            self.insert_row(sql,val)
            
            
    def bounce_table(self, file_name, duration, sample_rate, num_channels, max_vol):
            sql = "INSERT INTO bounce (FileName, Duration, SampleRate, NumChannels, MaxVol, UserID, EventDateTime) VALUES (%s, %s, %s, %s, %s, %s, %s)"           
            val = (file_name, duration, sample_rate, num_channels, max_vol, self.userID, datetime.now())            
            self.insert_row(sql,val)
            
            
    def view_table(self, duration):
            sql = "INSERT INTO viewmethod (Duration, UserID, EventDateTime) VALUES (%s, %s, %s)"           
            val = (duration, self.userID, datetime.now())     
            self.insert_row(sql,val)
            
            
    def loopmethod_table(self, num_loops, num_channels, bpm, time_mode):
            sql = "INSERT INTO loopmethod (NumLoops, NumChannels, BPM, TimeMode, UserID, EventDateTime) VALUES (%s, %s, %s, %s, %s, %s)"  
            val = (num_loops, num_channels, bpm, time_mode, self.userID, datetime.now())  
            self.insert_row(sql,val)
            
            
    def pan_table(self, pan_factor):
            sql = "INSERT INTO pan (PanFactor, UserID, EventDateTime) VALUES (%s, %s, %s)"
            val = (pan_factor, self.userID, datetime.now()) 
            self.insert_row(sql,val)
            
            
    def fade_table(self, fade_in, fade_out, in_curve, out_curve, bpm, time_mode):
            sql = "INSERT INTO fade (FadeIn, FadeOut, InCurve, OutCurve, BPM, TimeMode, UserID, EventDateTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (fade_in, fade_out, in_curve, out_curve, bpm, time_mode, self.userID, datetime.now()) 
            self.insert_row(sql,val)
            
            
    def LPF_table(self, cutoff, filter_order):
            sql = "INSERT INTO LPF (Cutoff, FilterOrder, UserID, EventDateTime) VALUES (%s, %s, %s, %s)"
            val = (cutoff, filter_order, self.userID, datetime.now()) 
            self.insert_row(sql,val)
            
            
    def HPF_table(self, cutoff, filter_order):
            sql = "INSERT INTO HPF (Cutoff, FilterOrder, UserID, EventDateTime) VALUES (%s, %s, %s, %s)"
            val = (cutoff, filter_order, self.userID, datetime.now())  
            self.insert_row(sql,val)
            
            
    def reverse_table(self, duration, num_channels, bpm, time_mode):
            sql = "INSERT INTO reverse (Duration, NumChannels, BPM, TimeMode, UserID, EventDateTime) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (duration, num_channels, bpm, time_mode, self.userID, datetime.now()) 
            self.insert_row(sql,val)
            
            
    def lfo_table(self, frequency, wave_type, wt_pos, volume):
            sql = "INSERT INTO lfo (Frequency, WaveType, WtPos, Volume, UserID, EventDateTime) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (frequency, wave_type, wt_pos, volume, self.userID, datetime.now()) 
            self.insert_row(sql,val)
            
            
    def delay_table(self, time, feedback, mix, spread, stereo, sync, start_side, bpm, time_mode):
            sql = "INSERT INTO delay (Time, Feedback, Mix, Spread, Stereo, Sync, StartSide, BPM, TimeMode, UserID, EventDateTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (time, feedback, mix, spread, stereo, sync, start_side, bpm, time_mode, self.userID, datetime.now()) 
            self.insert_row(sql,val)