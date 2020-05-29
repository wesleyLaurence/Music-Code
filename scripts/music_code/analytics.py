import mysql.connector
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .sql_kit import SQL_Kit
plt.style.use('seaborn-dark-palette')
import getpass

# Pandas settings
# display untruncated data from pandas
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', 999)
pd.set_option('display.max_rows', 100)

# this pulls data from the SQL database, then displays a dashboard of interactive plots, widgets and animations!

class Dashboard:
    
    """ This dashboard is designed to visualize trends in the Music-Code database """
    
    def __init__(self, database):
        
        # sql info
        self.userID = input('User ID: ')
        self.password = getpass.getpass('Password: ')
        self.database = database
    
    """ SELECT * FROM table """
    def select_table(self, table):
        
        s = SQL_Kit(self.userID, self.password, self.database)
        data = s.select_table(table)
        
        return data
    
        
    def display(self):
        
        """ visualize Music-Code database data """
        
        # initialize SQL kit to access database
        s = SQL_Kit(self.userID, self.password, self.database)
        
        
        """ Total Activity by hour """
        
        # get activity data
        all_date_times = self.activity().index

        all_days = []
        all_hours = []
        for item in all_date_times:
            all_days.append((item.timetuple().tm_yday))
            all_hours.append(item.hour)

        x = all_days
        y = all_hours
        x_labels = pd.Series(all_days).unique()

        fig1, ax1 = plt.subplots()
        ax1.set_title('Hourly Activity')
        ax1.scatter(x,y,color='mediumspringgreen',linewidths=1)
        ax1.set_xlabel('day of year')
        ax1.set_ylabel('hour')
        ax1.xaxis.grid(True)

        if len(x_labels) > 5:
            ax1.xaxis.set_ticks([min(all_days), max(all_days)])
        else:
            ax1.xaxis.set_ticks(x_labels)

        ax1.yaxis.grid(False) 
        plt.show()
        
        
        """ MOVING AVERAGE """
        
        df = self.activity().reset_index()

        def day_of_year(datetime_entry):
            return datetime_entry.timetuple().tm_yday

        df['day_of_year'] = list(df.apply(lambda x: day_of_year(x['EventDateTime']),axis=1))
        daily_count = df['day_of_year'].value_counts().sort_index()

        averages = []
        i=1
        for dab_count in daily_count:
            values = daily_count[:i]
            average = round(sum(values)/len(values),2)
            averages.append(average)
            i+=1

        day_list = list(df['day_of_year'].unique())

        avg_move_df = pd.DataFrame([day_list,averages]).T
        avg_move_df.rename(columns={0: 'day_id', 1: 'moving_avg'},inplace=True)
        avg_move_df.set_index('day_id',inplace=True)
        
        fig1, ax1 = plt.subplots()
        ax1.plot(avg_move_df.index.astype(int),avg_move_df['moving_avg'], color='mediumspringgreen')
        ax1.set_title('Moving AVG')
        ax1.set_xlabel('day_of_year')
        ax1.xaxis.set_ticks([min(all_days), max(all_days)])
        ax1.set_ylabel('Daily Activity')
        plt.show()
        
        
        
        """ Top 5 Samples """
        
        data = s.select_table('sample')['SoundCategory'].value_counts()
        
        objects = list(data)[:5]
        y_pos = list(data.index)[:5]

        # get class info from class_absence_stats dataframe
        #fig2 = plt.figure(2) 
        plt.bar(y_pos, objects, align='center', alpha=0.8, color='mediumspringgreen')
        plt.ylabel('Usage')
        plt.xlabel('Sound Category')
        plt.title('Top 5 Samples')
        plt.show()
        
        
        """ Top 3 Chords """
        
        data = s.select_table('chord')['ChordLabel'].value_counts()

        objects = list(data)[:3]
        y_pos = list(data.index)[:3]

        # get class info from class_absence_stats dataframe
        #fig2 = plt.figure(2) 
        plt.bar(y_pos, objects, align='center', alpha=0.8, color='mediumspringgreen')
        plt.ylabel('Usage')
        plt.xlabel('Chord Label')
        plt.title('Top 3 Chords')
        plt.show()
        
        
        """ Top 3 Wave Types """
        
        # get SQL table data
        set_1 = s.select_table('createwave')
        set_2 = s.select_table('sequence')
        set_3 = s.select_table('arpeggio')
        set_4 = s.select_table('chord')

        # concat tables into single pandas series
        all_wave_types = pd.concat([set_1['WaveType'], set_2['WaveType'], set_3['WaveType'], set_4['WaveType']])

        # sort values, show top 3
        top_3 = all_wave_types.value_counts().head(3)


        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = list(top_3.index)
        sizes = list(top_3.values)
        explode = (0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, colors=['g','b','r'], startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.set_title('Top Wave Types')

        plt.show()
        
        
        
    def activity(self):
        
        s = SQL_Kit(self.userID, self.password, self.database)
        
        # create chronological activity log
        
        # all sql tables in database
        all_tables = ['addwaves','arpeggio','bounce','chord','createwave','delay','fade','hpf',
                      'joinwaves','lfo','loopmethod','lpf','pan','rest','reverse','sample','sequence',
                      'timeedit','timemethod','viewmethod','volume']

        activity_log = pd.DataFrame(columns=['EventDateTime','method'])
        for table in all_tables:

            # get data from sql
            data = s.select_table(table)['EventDateTime']

            # convert to pandas dataframe
            data = pd.DataFrame(data)

            # create method column
            data['method'] = table

            # append activity to master dataframe
            activity_log = activity_log.append(data).sort_values('EventDateTime')

        activity_log.reset_index(inplace=True)
        activity_log.drop('index',axis=1, inplace=True)
        activity_log.set_index('EventDateTime', inplace=True)
        
        
        return activity_log