import sqlite3

DB_FILE="data.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()

c.execute("create table users_info(username text, password text, friends text, liked_recipies text, outgoing_friend_requests text, incoming_friend_requests text);")
c.execute("create table foods(dish_name text, likes integer);")