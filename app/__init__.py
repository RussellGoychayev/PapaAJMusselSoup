
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

# c.execute("DROP TABLE IF EXISTS user_info")
# table for all user information 
#c.execute("DROP TABLE IF EXISTS user_info") #DELETES TABLE IN CASE YOU WANT TO MAKE CHANGES TO USER_INFO 
c.execute("CREATE TABLE IF NOT EXISTS user_info (username TEXT, password TEXT, followers TEXT, following TEXT, liked_recipes TEXT);")

#give the user some friends for testing purposes
# c.execute(f'UPDATE user_info SET friends = ? WHERE username = ?', ["john cena", session['username'][0]])

# table for recipe leaderboard - stretch goal !!
#c.execute("DROP TABLE IF EXISTS foods")
c.execute("CREATE TABLE IF NOT EXISTS foods(dish_name TEXT, likes INTEGER);")

@app.route('/login', methods = ['GET', 'POST'])
def login():
	#url =  "https://api.edamam.com/api/recipes/v2"
	#res = requests.get(url, params={'type':'public', 'app_id':"904296dd", 'app_key':"58228c816ae6f1c88cca02d85c4da325", 'q': 'chicken'})
	#print(res.json()['hits'][0]['recipe']['label']) # prints the name of the first chicken recipe 
	
	url2 = "https://api.spoonacular.com/recipes/716429/information?apiKey=7081bf709f0d44b7984587105086357f"
	#res2 = requests.get(url2)
	#recipes_api_summary = res2.json()['summary']

	url3 = 'https://api.mymemory.translated.net/get?' #url of API
	#res3 = requests.get(url3, params={'q':'Hello', 'langpair':'en|es'}) #q is the source text you want to translate. langpair is <source language>|<target language>
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
				return redirect("/home")
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
			return render_template("register.html", error_message = "Username already exists.")
		elif (" " in username): #no spaces in username
			return redirect('/register')

	c.execute('INSERT INTO user_info VALUES(?, ?, ?, ?, ?)', [username, password, "", "", ""])
	db.commit()
	print("register helper: success")
	return redirect("/login")

# This route  is the index. It checks if user is in session. If yes, they are brought to home. If not, they are brought to login.
@app.route('/', methods = ['GET', 'POST'])
def index():
	print("username:")
	#print(session['username'][0])
	print("route:")
	print("/")
	print(session)
	if len(session) > 0:
		if session['username'][0] in session:
			return redirect("/home")
	return redirect('/login')

# This route is the home page. It will allow you to travel to the login, singup, leaderboards, friends,
# and other routes.
@app.route('/home', methods = ['GET', 'POST'])
def home():
	try: 
		c.execute("SELECT * from foods")
		# print("foods")
		# print(c.fetchall())

		c.execute("SELECT * from user_info")
		#print(c.fetchall())
		c.execute("SELECT liked_recipes from user_info WHERE username = ?", [session['username'][0]])
		recipes = ""
		try:
			recipes = "".join(c.fetchall()[0]) #string of recipes
		except Exception as e:	
			print(f'caught {type(e)}: e')
			
		#print(recipes)
		spacedlist = []
		urllist = [] 
		if (" " in recipes):
			likedlist = recipes.split() #list of all liked recipes
			print(likedlist)
			for i in likedlist: #removes placeholder none and replaces _ with spaces
				urllist.append(get_url(i.replace("_", " "))) #url of liked recipes
				spacedlist.append(i.replace("_", " "))

		#print(urllist)
		c.execute("SELECT following from user_info where username = ?", [session['username'][0]])
		following = []
		try:
			following = "".join(c.fetchall()[0]).split()
			print("FOllowing")
		except Exception as e:	
			print(f'caught {type(e)}: e')
		c.execute("SELECT followers from user_info where username = ?", [session['username'][0]])
		followers = []
		try:
			followers = "".join(c.fetchall()[0]).split()
			print("Stern SUCKS")
		except Exception as e:	
			print(f'caught {type(e)}: e')
	
	#give us info on our mistakes please ;,)
	except Exception as e:	
		print(f'caught {type(e)}: e')
		return render_template('landing.html', error="An unexpected error has occurred")
	return render_template('landing.html', liked=zip(spacedlist, urllist), user=session['username'][0], following=following, followingcount=len(following), followers=followers, followercount=len(followers), likecount=len(spacedlist))
	#render template here

# OUTLINE FOR WEB FRAME
@app.route('/friends', methods = ['GET', 'POST'])
def friendpage():
	# #give me all of this user's friends
	bestFriends = [] 
	person = session['username'][0]
	#store all users that are not me in a list of tuples

	#prevents recommending users you already follow
	c.execute("SELECT * from user_info")
	alreadyfollowing = []
	for row in c.fetchall(): #each row of the table
		if person in row[2]:
			alreadyfollowing.append(row[0]) #list of people you already follow

	#store all users that are not me in a list
	everyone = c.execute('SELECT username from user_info where username != ?', [person])
	allUsers = everyone.fetchall()
	listofusers = []
	for x in allUsers:
		listofusers.append("".join(x))
	# print(listofusers)
	# print(alreadyfollowing)

	#removes users from list that are already followed
	for i in alreadyfollowing:
		#print(i)
		if i in listofusers:
			listofusers.remove(i)
	# print(listofusers)
	# loop through love calculator 
	for x in listofusers:
		loveNumber = int(getLove(person,x))
		# print(loveNumber)
		if(loveNumber>=0):
			bestFriends.append(x)
	# print(bestFriends)
	# testing!
	# print("allUsers:")
	# print(allUsers)
	# print("bestFriends:")
	#print(bestFriends)
	return render_template('addfriends.html', bestfriend=bestFriends, l=len(bestFriends))

@app.route("/otherprofile/<user>", methods=["GET", "POST"])
def profile(user):
	try:
		c.execute("SELECT * from user_info")
		#print(c.fetchall())
		c.execute("SELECT liked_recipes from user_info WHERE username = ?", [user])
		recipes = "".join(c.fetchall()[0]) #string of recipes
		spacedlist = [] 
		urllist = []
		if (" " in recipes):
			likedlist = recipes.split() #list of all liked recipes
			for i in likedlist: #removes placeholder none and replaces _ with spaces
				urllist.append(get_url(i.replace("_", " "))) #url of liked recipes
				spacedlist.append(i.replace("_", " "))

		c.execute("SELECT following from user_info where username = ?", [user])
		following = []
		try:
			following = "".join(c.fetchall()[0]).split()
			#print("FOllowing")
		except:
			print("Let MAy win the lottery")
		c.execute("SELECT followers from user_info where username = ?", [user])
		followers = []
		try:
			followers = "".join(c.fetchall()[0]).split()
			#print("Stern SUCKS")
		except:
			print("Winning lottery is hard tho")

	except:
		return render_template("profile.html", error="An unexpected error has occurred")
	return render_template("profile.html", user=user, liked=zip(spacedlist, urllist), following=following, followingcount=len(following), followers=followers, followercount=len(followers), likecount=len(spacedlist))

@app.route("/addfriend/<user>", methods=["GET", "POST"])
def add(user):

# for i in liked:
# 		current = current + "".join(i) + " " #string of liked recipes separated by a space
# 	c.execute("UPDATE user_info SET liked_recipes = ? where username=?", [current+t.replace(" ","_"), session['username'][0]]) #adds liked recipe to table, replace spaces with _
# 	#c.execute('SELECT liked_recipes FROM user_info')
# 	#test = c.fetchall()
# 	db.commit()
	print("========================================================================================")
	print(user)
	c.execute("SELECT followers from user_info WHERE username= ?", [user])
	following = c.fetchall() #followers of the person you are going to follow
	c.execute("SELECT following from user_info WHERE username= ?", [session['username'][0]])
	followers = c.fetchall() #people who you are currently following
	
	#updates the person who you are following's followers
	followinglist = ""
	for f in following:
		followinglist = followinglist + "".join(f) + " " #current followers
	c.execute("UPDATE user_info SET followers = ? where username = ?", [followinglist+session['username'][0], user])
	#updates your following
	followerlist = ""
	# print("followers:")
	# print(followers)
	# print("following:")
	# print(following)
	for f in followers:
		followerlist = followerlist + "".join(f) + " " #current followers
	# print("followerlist:")
	# print(followerlist)
	c.execute("UPDATE user_info SET following = ? where username = ?", [followerlist+user, session['username'][0]])

	db.commit()
	return redirect("/home")
# #this function will return a list of all your best friends (using love calculator)
# def makeFriends():
# 	allUsers = [] 
# 	bestFriends = [] 
# 	person = session['username'][0]
# 	#store all users that are not me in a list of tuples
# 	everyone = c.execute(f'SELECT username FROM user_info WHERE user!= {person}')
# 	#store all users that are not me in a list
# 	allUsers.append(everyone.fetchall())
# 	# loop through love calculator 
# 	for x in len(allUsers):
# 		if(getLove(person,allUsers[x])>0):
# 			bestFriends.append(allUsers[x])
# 	return bestFriends

# 	#render template here

#This is the explore page. Here you can browse recipies and like them.
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
		return render_template('explore.html', error="An unexpected error has occurred")
# 	#render template here

@app.route('/leaderboard', methods = ['GET', 'POST'])
def viewLeader():
	namelist = []
	likelist = []
	links = []
	alreadyliked = []
	c.execute('SELECT liked_recipes FROM user_info WHERE username=?', [session['username'][0]])
	liked = c.fetchall()
	alreadyliked = liked[0][0].split(" ") # list of already liked recipes
	for i in range(len(alreadyliked)): # replaces _ with spaces
		alreadyliked[i] = alreadyliked[i].replace("_"," ")
	# print(alreadyliked)
	c.execute("SELECT * from foods")
	for recipelikes in c.fetchall(): #tuple of (recipename, number of likes)
		name = recipelikes[0] # name of recipe
		# links.append(get_url(name))
		likes = recipelikes[1] # number of likes it has
		namelist.append(name)
		likelist.append(likes)
	
	print(likelist)
	return render_template("leaderboard.html", info=zip(namelist, likelist), alreadyliked=alreadyliked) # , links

# 	#render template here
@app.route('/liked_recipes/<t>', methods= ['GET', 'POST'])
def like(t):
	#give me all of this user's liked recipes
	c.execute('SELECT liked_recipes FROM user_info WHERE username=?', [session['username'][0]])
	liked = c.fetchall()
	# print("liked before:")
	# print(liked)
	
	#update this user's liked recipes
	current = "" #string to append t to liked_recipes

	for i in liked:
		current = current + "".join(i) + " " #string of liked recipes separated by a space
	c.execute("UPDATE user_info SET liked_recipes=? WHERE username=?", [current+t.replace(" ","_"), session['username'][0]]) #adds liked recipe to table, replace spaces with _

	c.execute('SELECT liked_recipes FROM user_info WHERE username=?', [session['username'][0]])
	liked = c.fetchall()
	# print("liked after:")
	# print(liked)

	c.execute("SELECT dish_name from foods")
	foodarray = c.fetchall()
	if len(foodarray) > 0: # checks if there is anything in food table 
		for foodtuple in foodarray:
			if t in foodtuple: #dish is already liked
				c.execute("SELECT likes from foods where dish_name = ?", [t])
				likes = c.fetchall()[0]
				print(likes)
				c.execute("UPDATE foods set likes = ? where dish_name = ?",[likes[0]+1, t] )
				db.commit()
				return redirect("/home") #breaks loop so recipes aren't added multiple times
			else: # new entry
				c.execute("INSERT into foods values (?, ?)", [t, 1])
				db.commit()
				return redirect("/home")

	else:
		c.execute("INSERT into foods values (?, ?)", [t, 1])

	c.execute("SELECT * from foods")
	print(c.fetchall())
	#c.execute("CREATE TABLE IF NOT EXISTS foods(dish_name TEXT, likes INTEGER);")

	#c.execute("CREATE TABLE IF NOT EXISTS foods(dish_name TEXT, likes INTEGER, comments TEXT);")
	#give me the number of likes this dish has
	# c.execute('SELECT likes FROM foods WHERE dish_name=?', t)
	# likes = c.fetchall()[0]
	# print("LIKES HERE aiosudhaodihqwodiqhweoriqwheio/n" + likes)
	#update the number of likes this dish has to be (previous + 1)
	# c.execute('UPDATE foods SET liked=? WHERE dish_name=?', t)

	
	#c.execute('SELECT liked_recipes FROM user_info')
	#test = c.fetchall()
	db.commit()
	return redirect("/home")

@app.route('/liked_recipes_leaderboard/<t>', methods= ['GET', 'POST'])
def likeleaderboard(t):
	#give me all of this user's liked recipes
	c.execute('SELECT liked_recipes FROM user_info WHERE username=?', [session['username'][0]])
	liked = c.fetchall()
	# print("liked before:")
	# print(liked)
	
	current = ""
	#update this user's liked recipes
	for i in liked:
		current = current + "".join(i) + " " #string of liked recipes separated by a space
	c.execute("UPDATE user_info SET liked_recipes=? WHERE username=?", [current+t.replace(" ","_"), session['username'][0]]) #adds liked recipe to table, replace spaces with _

	c.execute("SELECT dish_name from foods")
	foodarray = c.fetchall()
	# print("foods:")
	# print(foodarray)
	if len(foodarray) > 0: # checks if there is anything in food table 
		for foodtuple in foodarray:
			if t in foodtuple: #dish is already liked
				if t not in liked:
					c.execute("SELECT likes from foods where dish_name = ?", [t])
					likes = c.fetchall()[0]
					print(likes)
					c.execute("UPDATE foods set likes = ? where dish_name = ?",[likes[0]+1, t] )
					db.commit()
					return redirect("/leaderboard") #breaks loop so recipes aren't added multiple times
				else:
					return redirect("/leaderboard")
			else: # new entry
				c.execute("INSERT into foods values (?, ?)", [t, 1])
				db.commit()
				return redirect("/leaderboard")

	else:
		c.execute("INSERT into foods values (?, ?)", [t, 1])

	c.execute("SELECT * from foods")
	print(c.fetchall())
	#c.execute("CREATE TABLE IF NOT EXISTS foods(dish_name TEXT, likes INTEGER);")

	#c.execute("CREATE TABLE IF NOT EXISTS foods(dish_name TEXT, likes INTEGER, comments TEXT);")
	#give me the number of likes this dish has
	# c.execute('SELECT likes FROM foods WHERE dish_name=?', t)
	# likes = c.fetchall()[0]
	# print("LIKES HERE aiosudhaodihqwodiqhweoriqwheio/n" + likes)
	#update the number of likes this dish has to be (previous + 1)
	# c.execute('UPDATE foods SET liked=? WHERE dish_name=?', t)

	
	#c.execute('SELECT liked_recipes FROM user_info')
	#test = c.fetchall()
	db.commit()
	return redirect("/leaderboard")

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

# print(makeFriends)
@app.route('/logout') 
def logout(): 
	session.pop("username", None)
	#session.pop("password")
	return redirect("/login")

if __name__ == '__main__':
	app.debug = True
	app.run()