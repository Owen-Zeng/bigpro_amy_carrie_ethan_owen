from flask import Flask  # facilitate flask webserving
from flask import render_template  # facilitate jinja templating
from flask import request, redirect, url_for  # facilitate form submission
from flask import session
import sqlite3   #enable control of an sqlite database
<<<<<<< HEAD
=======


#FLASK declaration
#====================================================================================#
app = Flask(__name__)  # create Flask object
app.secret_key = b'bigproer'


>>>>>>> 98b7b36106a6c91cb29e7bd89da7be35ac775c60
#SQLITE3 Databases
#====================================================================================#
DB_FILE="webstory.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()
<<<<<<< HEAD
c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT NOT NULL);")
c.execute(f"INSERT OR REPLACE INTO users VALUES('owen', '123');")
c.execute(f"INSERT OR REPLACE INTO users VALUES('Ethan', 'salad');")

#REGISTER FUNCTIONALITY
#====================================================================================#

=======
# profile table
c.execute("CREATE TABLE IF NOT EXISTS user_profile(username TEXT PRIMARY KEY NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL);")

# story pages table
c.execute("CREATE TABLE IF NOT EXISTS stories(storyTitle TEXT PRIMARY KEY NOT NULL, content TEXT, previousEdit TEXT, storyLink TEXT);")

# author name table with story title
c.execute("CREATE TABLE IF NOT EXISTS authors(username TEXT, storyTitle TEXT);")


#REGISTER FUNCTIONALITY
#====================================================================================#
@app.route("/register", methods=['GET', 'POST'])
>>>>>>> 98b7b36106a6c91cb29e7bd89da7be35ac775c60
def register():
    # if username exists in database, redirect to home
    if loggedin():
        return "Logged In"
    else:
<<<<<<< HEAD
        return 1

=======
        if request.method == 'POST':
            # open sqlite3 db as db
            with sqlite3.connect(DB_FILE) as db:
                c = db.cursor()
                # insert db values for each form
                command = (f"INSERT INTO user_profile VALUES ('{request.form['id']}', '{request.form['email']}', '{request.form['pass']}');")
                c.execute(command)
                # keeps session alive even if page closes
                session.permanent = True
                # stores username and pass as id and pass, respectively
                session['username'] = request.form['id']
                session['password'] = request.form['pass']
                return redirect(url_for('home'))
    # if not logged in, show register page
    return registerpage()
>>>>>>> 98b7b36106a6c91cb29e7bd89da7be35ac775c60


#LOGIN FUNCTIONALITY#
#====================================================================================#
<<<<<<< HEAD
app = Flask(__name__)  # create Flask object
app.secret_key = b'bigproer'

users={}

c.execute("SELECT * FROM users username;")
username_roster=c.fetchall()
for i in range(len(username_roster)):
    users.update({username_roster[i][0]:username_roster[i][1]})
=======
# dict of usernames:password
users={}

for row in c.execute("SELECT * FROM user_profile;"):
    users.update({row[0]:row[2]})
>>>>>>> 98b7b36106a6c91cb29e7bd89da7be35ac775c60


db.commit() #save changes
db.close()  #close database
#temporary dictionary to represent pulling from SQLITE

# if the username exists in database, return True
# else return False
def loggedin():
    if 'username' in session:
        return True
    return False

# redirect page to home or login
@app.route("/", methods=['GET', 'POST'])
def response():
    if loggedin():
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    # redirect to login page if logged in
    if loggedin():
        return redirect(url_for('home'))
    # if requested, save session username and password
    # and login, makes sure to remove invalid login credentials
    if request.method == 'POST':
        session.permanent = True
        session['username'] = request.form['id']
        session['password'] = request.form['pass']
        if users.get(session['username'])==session['password']:
            return redirect(url_for('home'))
        else:
            session.pop('username')
            return loginpage(valid=False)
    else:
        return loginpage(valid=False)

@app.route("/home", methods=['GET', 'POST'])
def home():
    if loggedin():
        return homepage(session['username'])
    else:
        return redirect(url_for('login'))

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    # if logged in, remove username key from dict
    if loggedin():
        session.pop('username', None)
        return logoutpage()
    return redirect(url_for('login'))


#WEBPAGE ROUTING#
#====================================================================================#
<<<<<<< HEAD
def homepage(soul,a="Thetha"):
    return render_template('home.html',user=soul,)
def loginpage(soul="",valid= True):
=======
# returns the home page html template
def homepage(user):
    return render_template('home.html',username=user,)

# if the username is valid, return the login page html template
# else, return the same page but with the incorrect username/password text
def loginpage(user="",valid = True):
>>>>>>> 98b7b36106a6c91cb29e7bd89da7be35ac775c60
    if(valid==True):
        return render_template('login.html',user=soul)
    else:
        return render_template('login.html',invalid="Your username or password was incorrect")

# returns the logout page html template
def logoutpage():
    return render_template('logout.html')

# returns the register page html template
def registerpage():
    return render_template('register.html')


#=====================================================================================#
if __name__ == "__main__":  # false if this file imported as module
    #app.debug = True  # enable PSOD, auto-server-restart on code chg
    app.run()
