# Music-Code Documentation

Welcome to the Music-Code documentation. Music-Code is a python library for creating music. You can create musical notes, intervals, chords, progressions, melodies, bass lines, drum beats and full songs! You can also generated complex waveform visualizations for images and video. Music-Code is integrated with MySQL and provides and analytics dashboard to monitor system usage and data trends.

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
<b>pip install music-code </b>

### Set Program Files Path
1. Open music_code.py in your conda environment. On my computer, the file is located here: C:\Users\wesle\Anaconda3\envs\music_code\Lib\site-packages\music_code\music_code.py
2. Go to line 42, in the MusicCode __init__ function, find the <b>program_files_location</b> attribute. Copy and paste the file path to your program files folder, which you can download here: [Music-Code Program Files](https://drive.google.com/file/d/1HCCqBaiAlhgpqMP7qnceEMxLg-eGJqEa/view?usp=sharing). Once this path is set, the Music-Code file system is good to go. The program files folder contains the Music-Code sample library and datasets. All the WAV files and images you create are stored in this folder.

### MySQL (optional)
Connect Music-Code to a MySQL database to archive all system data and have access to an analytics dashboard. To create the Music-Code MySQL database, see the database.txt file.

### Test
Run the tests.py file inside your conda environment to ensure the all systems are working properly.

## Jupyter Notebook Tutorials
Check out the jupyter notebooks tutorials. These demonstrate all the capabilities of the Music-Code library.

