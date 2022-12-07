
from flask import Flask, render_template, session, request
import sqlite3

app = Flask(__name__)

DB_FILE="data.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
command = ""
c.execute(command) 

@app.route('/', methods = ['GET', 'POST'])
def login():
	return render_template('abc.html')

if __name__ == '__main__':
	app.debug = True
	app.run()