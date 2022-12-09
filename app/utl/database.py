import sqlite3
DB_FILE="data.db"

#open or CREATE file 
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()

def createSession(): 
    # set up tables - 1) user info and 2) food info 
    c.execute("create table if not exists users_info(username text, password text, friends text, liked_recipies text, outgoing_friend_requests text, incoming_friend_requests text);")
    c.execute("create table if not exists foods(dish_name text, likes integer);")
    db.commit() 
    db.close() 

# VERY ROUGH OUTLINE THAT DOESNT FULLY WORK ATM BUT ITS SOMETHING

# def register(username, password):
#     c.execute('select exists(username) from users_info where username = ?', username)
#     [exists] = c.fetchone()
#     if exists: 
#         print("username is already taken, try again")
#         db.commit() 
#         db.close() 
#     else: 
#         newUser = (username, password)
#         c.execute(f'insert into users_info values(?, ?)',newUser)

# def login(username, password): 
#     successStatus = False 
#     username = (username,)
#     c.execute(f'select password from users_info where username = ?', username)
#     passwordFetch = c.fetchone() 
#     if(): 
#         passwordFetch = passwordFetch[0] 
#         # if the password is found 
#         if(passwordFetch == password): 
#             db.commit()
#             db.close() 
#             successStatus = True
#     return successStatus