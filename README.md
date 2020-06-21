# Music-Code

Music-Code is a python library for creating music. You can create musical notes, chords, progressions, melodies, bass lines, drum beats, sound design and full songs! There is a sequencer, arpeggiator, chord generator, audio sampler and various audio effects. There are also tools for time editing and arranging within a given BPM. It has most of the core features of a digital audio workstation (DAW). 

In addition to creating music, you can also generate HD waveform visualizations for images and video. Music-Code is integrated with MySQL and provides an analytics dashboard and Rest API to monitor system usage and data trends.

You can use Music-Code to automatically produce large audio datasets for use in deep learning applications. You can scan through different spaces of musical/tonal combinations, exporting each variation as a labeled WAV file. The long term purpose of Music-Code is to build open source music AI software.

## Setup

### Installation
`pip install music-code`

### Requirements
numpy==1.18.4 
pandas==1.0.3 
matplotlib==3.2.1 
seaborn==0.10.1 
soundfile==0.10.3.post1 
scipy==1.4.1 
sklearn==0.0 
datetime==4.3 
PyAudio==0.2.11 
wave==0.0.2 
mysql-connector-python==8.0.20 
psutil==5.7.0 

### Program Files
1. Either download/clone this repository or download the Music-Code program files here: [Music-Code Program Files](https://drive.google.com/file/d/1C1st6FFar_-QhCX9AW04DyAHwOtLP5nT/view?usp=sharing). Unzip and save the program files in a memorable location. Copy the file path.
2. Open your Anaconda3 folder, and locate the music_code installation. For my machine, the file is located here: <b>C:\Users\wesle\Anaconda3\envs\music_code\Lib\site-packages\music_code\music_code.py</b>
3. Open music_code.py, go to line 42, in the MusicCode __init__ function, find the <b>program_files_location</b> attribute. Copy and paste the file path to your program files folder, which you can download here: [Music-Code Program Files](https://drive.google.com/file/d/1C1st6FFar_-QhCX9AW04DyAHwOtLP5nT/view?usp=sharing). Once this path is set, the Music-Code file system is good to go. The program files folder contains the Music-Code sample library and datasets. All the WAV files and images you create are stored in this folder.

### MySQL (optional)
Connect Music-Code to a MySQL database to archive all system data and have access to an analytics dashboard. There is also a flask rest API for database access.

### Test
Run the tests.py file inside your conda environment to ensure the all systems are working properly.

### Jupyter Notebook Tutorials
Check out the jupyter notebook tutorials. These demonstrate all the capabilities of the Music-Code library.

### YouTube Tutorial
Soon I will post a video about geting started with Music-Code!

### Contact
For any other questions, email wesleylaurencetech@gmail.com
