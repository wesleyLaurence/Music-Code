# Music-Code

Music-Code is a python library for creating music. You can create musical notes, chords, progressions, melodies, bass lines, drum beats, sound design and full songs! It has most of the core features of a digital audio workstation (DAW). In addition to creating music, you can also generate complex waveform visualizations for images and video. Music-Code is integrated with MySQL and provides and analytics dashboard to monitor system usage and data trends.

You can use Music-Code to automatically produce large audio datasets for use in deep learning applications. You can scan through different spaces of musical/tonal combinations, exporting each variation as a labeled WAV file. The long term purpose of Music-Code is to create vast musical datasets and build a superintelligent music AI.

## Setup

### Download Program Files
First, download the Music-Code program files here: [Music-Code Program Files](https://drive.google.com/file/d/1HCCqBaiAlhgpqMP7qnceEMxLg-eGJqEa/view?usp=sharing). Store the program files in a memorable location, then copy the file path (you will need this in a moment).

### Create Anaconda Environment
Anaconda is the optimal way to run Music-Code. 
1. Install [Anaconda](https://www.anaconda.com/products/individual) on your machine
2. Create new conda environment named music_code
3. Activate music_code environment
4. Install the following requirements:

#### Requirements
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
jupyter

### Installation
`pip install music-code`

### Set Program Files Path
1. Open your Anaconda3 folder, and locate the music_code installation. For my machine, the file is located here: <b>C:\Users\wesle\Anaconda3\envs\music_code\Lib\site-packages\music_code\music_code.py</b>
2. Open music_code.py, go to line 42, in the MusicCode __init__ function, find the <b>program_files_location</b> attribute. Copy and paste the file path to your program files folder, which you can download here: [Music-Code Program Files](https://drive.google.com/file/d/1HCCqBaiAlhgpqMP7qnceEMxLg-eGJqEa/view?usp=sharing). Once this path is set, the Music-Code file system is good to go. The program files folder contains the Music-Code sample library and datasets. All the WAV files and images you create are stored in this folder.

### MySQL (optional)
Connect Music-Code to a MySQL database to archive all system data and have access to an analytics dashboard. To create the Music-Code MySQL database, see the create_database.sql file.

### Test
Run the tests.py file inside your conda environment to ensure the all systems are working properly.

## Jupyter Notebook Tutorials
Check out the jupyter notebook tutorials. These demonstrate all the capabilities of the Music-Code library.

