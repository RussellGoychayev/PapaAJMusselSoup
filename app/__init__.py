
from flask import Flask, render_template, session, request
import sqlite3
import requests

app = Flask(__name__)

DB_FILE="data.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
command = ""
c.execute(command) 

@app.route('/', methods = ['GET', 'POST'])
def login():
	url =  "https://api.edamam.com/api/recipes/v2"
	res = requests.get(url, params={'type':'public', 'app_id':"904296dd", 'app_key':"58228c816ae6f1c88cca02d85c4da325", 'q': 'chicken'})
	print(res.json()['hits'][0]['recipe']['label']) # prints the name of the first chicken recipe 
	
	url2 = "https://api.spoonacular.com/recipes/716429/information?apiKey=7081bf709f0d44b7984587105086357f"
	res2 = requests.get(url2)
	a = res2.json()['summary']
	return render_template('abc.html', s=a)

@app.route('/register', methods = ['GET', 'POST'])
def register():
	return "a"


if __name__ == '__main__':
	app.debug = True
	app.run()