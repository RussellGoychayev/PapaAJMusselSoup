
from flask import Flask, render_template, session, request, redirect 
import sqlite3
import requests
import utl.database as dataFrame 
from api import *

app = Flask(__name__)

app.secret_key = "abc123";#Q: what is the app secret key?
#If u remove the line above (app.secret_key = "abc123") then the debugger throws an error
#RuntimeError: The session is unavailable because no secret key was set.  Set the secret_key on the application to something unique and secret.

# initiate tables 
dataFrame.createSession 


DB_FILE="data.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()

#c.execute("DROP TABLE IF EXISTS user_info;")
c.execute("CREATE TABLE IF NOT EXISTS user_info (username TEXT, password TEXT, stories_ids TEXT);")

#c.execute("DROP TABLE IF EXISTS pages;")
c.execute("CREATE TABLE IF NOT EXISTS pages(story_id int, title text, content text, edit_ids text)");

@app.route('/login', methods = ['GET', 'POST'])
def login():
	#url =  "https://api.edamam.com/api/recipes/v2"
	#res = requests.get(url, params={'type':'public', 'app_id':"904296dd", 'app_key':"58228c816ae6f1c88cca02d85c4da325", 'q': 'chicken'})
	#print(res.json()['hits'][0]['recipe']['label']) # prints the name of the first chicken recipe 
	
	url2 = "https://api.spoonacular.com/recipes/716429/information?apiKey=7081bf709f0d44b7984587105086357f"
	#res2 = requests.get(url2)
	#recipes_api_summary = res2.json()['summary']

	url3 = 'https://api.mymemory.translated.net/get?' #url of API
	res3 = requests.get(url3, params={'q':'Hello', 'langpair':'en|es'}) #q is the source text you want to translate. langpair is <source language>|<target language>
	#print(res3.json())
	# print(res3.json()['responseData']['translatedText']) #prints the Spanish translation of 'Hello'
	return render_template('login.html')

@app.route('/login_helper', methods = ['POST'])
def login_helper():
	# The login route. This is the route that the login form on the landing page sends the information to

	'''
	PSEUDOCODE:

	username = username from form
	password = password from form

	if it's in that database:
		create a session

	else:
		return an error page or something
	'''
	username = request.form['username']
	password = request.form['password']

	c.execute("SELECT * FROM user_info")
	users = c.fetchall()

	for tuple in users:
		if (username == tuple[0]):
			if (password == tuple[1]):
				session["username"] = [username]
				# return render_template("dashboard.html")
				return redirect("/")
				print("login_helper: logged u in")
			else:
				return render_template("login.html", error_message ="Incorrect Password")
				print("login_helper: wrong password")
	print("login_helper: wrong username and/or password, sending u to /login")
	return redirect("/login")

# This route returns the form which will allow a user to sign up. The form passes its inputs
# to the route called "/register_helper"
@app.route('/register', methods = ['GET'])
def register(): 
	return render_template('register.html')

# This route receives info from the form on the route "/register" and enters the user into the SQL
# database and creates their session.
@app.route('/register_helper', methods = ['POST'])
def register_helper():
	print("register_helper")
	
	'''
	PSEUDOCODE:

	username = username from form
	password = password from form

	if it's in that database:
		return an error page

	else:
		enter row into sql table with appropriate information
		log user in
	'''
	username = request.form["username"]
	password = request.form["password"]

	c.execute("SELECT * FROM user_info")
	users = c.fetchall()

	for tuple in users:
		if (username == tuple[0]):
			print("username alr exists. sent u back to /register")
			return redirect('/register')

	c.execute('INSERT INTO user_info VALUES(?, ?, "")', [username, password])
	db.commit()
	print("register helper: success")
	return redirect("/login")

# This route  is the index. It checks if user is in session. If yes, they are brought to home. If not, they are brought to login.
@app.route('/', methods = ['GET', 'POST'])
def index(): 
	if 'username' in session:
		return redirect("/home")
	return render_template('/login.html')
	#render template here

# This route is the home page. It will allow you to travel to the login, singup, leaderboards, friends,
# and other routes.
@app.route('/home', methods = ['GET', 'POST'])
def home(): 
	return render_template('landing.html')
	#render template here

# OUTLINE FOR WEB FRAME
@app.route('/friends', methods = ['GET', 'POST'])
def friendpage(): 
	return render_template('friends.html')
# 	#render template here

@app.route('/explore', methods = ['GET', 'POST'])
def explorepage():
	#try block because some recipes don't have images
	try:       								
		info = makeList(5)
		title = info[0]
		image = info[1]
		url = info[2]
		summary = info[3]
		return render_template('explore.html', i=zip(title, image, url, summary))
	except:
		return render_template('explore.html', error="An unexpected error has occured")
# 	#render template here

# @app.route('/leaderboard', methods = ['GET', 'POST'])
# def viewLeader(): 
# 	#render template here

@app.route('/search', methods = ['GET', 'POST'])
def search():
	try:
		#print(request.form['search'])
		results = search_recipe(request.form['search'], 0, 12)
		return render_template('search.html', r=results, s=request.form['search'])
	except:
		return render_template('search.html', error="No results found 😭")

@app.route('/<name>', methods = ['GET', 'POST'])
def results(name):
	try:
		k = get_key('keys/key_edamam.txt')
		url =  "https://api.edamam.com/api/recipes/v2"
		res = requests.get(url, params={'type':'public', 'app_id':"904296dd", 'app_key':k, 'q': name})
		#print(res.json()['hits'][0]['recipe'].keys())
		c = int(res.json()['hits'][0]['recipe']['calories'])
		#print(c)
		i = res.json()['hits'][0]['recipe']['image'] # picture of food
		#print(i)
		u = res.json()['hits'][0]['recipe']['url'] #source url
		#print(u)
		ct = res.json()['hits'][0]['recipe']['cuisineType'] #type of cuisine (American, South American...)
		#print(ct)
		ing = res.json()['hits'][0]['recipe']['ingredientLines'] #list of ingredients
		#print(ing)
		d = res.json()['hits'][0]['recipe']['digest'] #nutrition
		#print(d)
		f = int(res.json()['hits'][0]['recipe']['digest'][0]['total']) #fat content
		#print(f)
		carb = int(res.json()['hits'][0]['recipe']['digest'][1]['total']) #carb content
		#print(carb)
		p = int(res.json()['hits'][0]['recipe']['digest'][2]['total']) #protein content
		#print(p)
		chol = int(res.json()['hits'][0]['recipe']['digest'][3]['total']) #cholesterol content
		#print(chol)
		sod = int(res.json()['hits'][0]['recipe']['digest'][4]['total']) #sodium content
		#print(sod)
		y = int(res.json()['hits'][0]['recipe']['yield']) #number of servings
		#print(y)
		#return res.json()['hits'][0]['recipe']
		return render_template("results.html", n=name, c=c, i=i, ct=ct[0], ing=', '.join(ing), f=f, carb=carb, p=p, chol=chol, y=y, sod=sod, u=u)
	except:
		return render_template("results.html", error="Unable to retrieve data")

@app.route('/logout') 
def logout(): 
	session.pop("username")
	#session.pop("password")
	return redirect("/login")

if __name__ == '__main__':
	app.debug = True
	app.run()
