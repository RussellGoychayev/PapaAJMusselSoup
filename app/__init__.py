
from flask import Flask, render_template, session, request, redirect 
import sqlite3
import requests
import utl.database as dataFrame 

app = Flask(__name__)
# initiate tables 
dataFrame.createSession 

@app.route('/', methods = ['GET', 'POST'])
def login():
	url =  "https://api.edamam.com/api/recipes/v2"
	res = requests.get(url, params={'type':'public', 'app_id':"904296dd", 'app_key':"58228c816ae6f1c88cca02d85c4da325", 'q': 'chicken'})
	print(res.json()['hits'][0]['recipe']['label']) # prints the name of the first chicken recipe 
	
	url2 = "https://api.spoonacular.com/recipes/716429/information?apiKey=7081bf709f0d44b7984587105086357f"
	res2 = requests.get(url2)
	a = res2.json()['summary']
	return render_template('login.html', s=a)

@app.route('/register', methods = ['GET', 'POST'])
def register(): 
	return render_template('register.html')
	#render template here

@app.route('/landing page', methods = ['GET', 'POST'])
def landing(): 
	return render_template('landing.html')
	#render template here

# OUTLINE FOR WEB FRAME
#  @app.route('/friends', methods = ['GET', 'POST'])
# def friendpage(): 
# 	#render template here

# @app.route('/explore', methods = ['GET', 'POST'])
# def explorepage(): 
# 	#render template here

# @app.route('/leaderboard', methods = ['GET', 'POST'])
# def viewLeader(): 
# 	#render template here

@app.route('/logout') 
def logout(): 
	session.pop("username")
	session.pop("password")
	return redirect("/")

if __name__ == '__main__':
	app.debug = True
	app.run()