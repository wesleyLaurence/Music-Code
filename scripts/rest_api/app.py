from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import getpass

app = Flask(__name__)

# configure db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = input('User ID: ')
app.config['MYSQL_PASSWORD'] = getpass.getpass('Password: ')
app.config['MYSQL_DB'] = 'musiccode'

mysql = MySQL(app)

@app.route('/addwaves')
def addwaves():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM addwaves;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('addwaves.html',all_columns=all_columns)

@app.route('/arpeggio')
def arpeggio():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM arpeggio;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('arpeggio.html',all_columns=all_columns)
    
@app.route('/bounce')
def bounce():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM bounce;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('bounce.html',all_columns=all_columns)
    
@app.route('/chord')
def chord():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM chord;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('chord.html',all_columns=all_columns)
    
@app.route('/createwave')
def createwave():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM createwave;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('createwave.html',all_columns=all_columns)
    
@app.route('/delay')
def delay():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM delay;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('delay.html',all_columns=all_columns)
    
@app.route('/fade')
def fade():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM fade;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('fade.html',all_columns=all_columns)
    
@app.route('/hpf')
def hpf():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM hpf;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('hpf.html',all_columns=all_columns)
    
@app.route('/joinwaves')
def joinwaves():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM joinwaves;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('joinwaves.html',all_columns=all_columns)
    
@app.route('/lfo')
def lfo():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM lfo;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('lfo.html',all_columns=all_columns)
    
@app.route('/loopmethod')
def loopmethod():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM loopmethod;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('loopmethod.html',all_columns=all_columns)
    
@app.route('/lpf')
def lpf():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM lpf;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('lpf.html',all_columns=all_columns)    
    
@app.route('/pan')
def pan():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM pan;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('pan.html',all_columns=all_columns)
    
@app.route('/rest')
def rest():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM rest;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('rest.html',all_columns=all_columns)
    
@app.route('/reverse')
def reverse():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM reverse;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('reverse.html',all_columns=all_columns)
    
@app.route('/sample')
def sample():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM sample;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('sample.html',all_columns=all_columns)
    
@app.route('/sequence')
def sequence():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM sequence;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('sequence.html',all_columns=all_columns)
    
@app.route('/timeedit')
def timeedit():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM timeedit;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('timeedit.html',all_columns=all_columns)
    
@app.route('/timemethod')
def timemethod():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM timemethod;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('timemethod.html',all_columns=all_columns)
    
@app.route('/viewmethod')
def viewmethod():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM viewmethod;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('viewmethod.html',all_columns=all_columns)
    
@app.route('/volume')
def volume():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM volume;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('volume.html',all_columns=all_columns)

if __name__== '__main__':
	app.run(debug=True)