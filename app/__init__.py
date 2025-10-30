from flask import Flask  # facilitate flask webserving
from flask import render_template  # facilitate jinja templating
from flask import request, redirect, url_for  # facilitate form submission
from flask import session
import sqlite3   #enable control of an sqlite database


#FLASK declaration
#====================================================================================#
app = Flask(__name__)  # create Flask object
app.secret_key = b'bigproer'


#SQLITE3 Databases
#====================================================================================#
DB_FILE="webstory.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()
# profile table
c.execute("CREATE TABLE IF NOT EXISTS user_profile(username TEXT PRIMARY KEY NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL);")

# story pages table
c.execute("CREATE TABLE IF NOT EXISTS stories(storyTitle TEXT PRIMARY KEY NOT NULL, content TEXT, previousEdit TEXT, storyLink TEXT);")

# author name table with story title
c.execute("CREATE TABLE IF NOT EXISTS authors(username TEXT, storyTitle TEXT);")


#REGISTER FUNCTIONALITY
#====================================================================================#
@app.route("/register", methods=['GET', 'POST'])
def register():
    # if username exists in database, redirect to home
    if loggedin():
        return redirect(url_for('home'))
    else:
        if request.method == 'POST':
            # open sqlite3 db as db
            with sqlite3.connect(DB_FILE) as db:
                c = db.cursor()
                # keeps session alive even if page closes
                session.permanent = True
                # stores username and pass as id and pass, respectively
                t = ""
                if(request.form['id'] == "" or request.form['pass'] == "" or request.form['email'] == ""):
                    t = "Please enter a valid "
                    if(request.form['id'] == ""):
                        t = t + "username "
                    if(request.form['email'] == ""):
                        t = t + "email "
                    if(request.form['pass'] == ""):
                        t = t + "password "
                    return registerpage(False, t)
                # insert db values for each form
                for row in c.execute(f"SELECT * FROM user_profile WHERE username = '{request.form['id']}'"):
                    if(row[0] != ''):
                        return registerpage(False, "Username taken")
                command = (f"INSERT INTO user_profile VALUES ('{request.form['id']}', '{request.form['pass']}', '{request.form['email']}');")
                session['username'] = request.form['id']
                session['password'] = request.form['pass']
                c.execute(command)
                return redirect(url_for('home'))
    # if not logged in, show register page
    return registerpage()


#LOGIN FUNCTIONALITY#
#====================================================================================#
# dict of usernames:password
users={}

for row in c.execute("SELECT * FROM user_profile;"):
    users.update({row[0]:row[1]})

print(users)

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
        with sqlite3.connect(DB_FILE) as db:
                c = db.cursor()
                for row in c.execute(f"SELECT * FROM user_profile WHERE username LIKE '{request.form['id']}';"):
                    if(row[1] == request.form['pass']):
                        session['username'] = request.form['id']
                        session['password'] = request.form['pass']
                        return redirect(url_for('home'))
                    else:
            #session.pop('username')
            #session.pop('password')
                        return loginpage(valid=False)
        return loginpage(valid = False)
    else:
        return loginpage(valid=True)

@app.route("/home", methods=['GET', 'POST'])
def home():
    if loggedin():
        return homepage(session['username'])
    else:
        return redirect(url_for('register'))

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    # if logged in, remove username key from dict
    if loggedin():
        session.pop('username', None)
        return logoutpage()
    return redirect(url_for('login'))
'''
@app.route("/stories", methods=['GET', 'POST'])
def stories():
    if loggedin():
        return stories()
    return loginpage()

@app.route("/stories/<name>", methods=['GET', 'POST'])
def stories(name):
    return
'''
#WEBPAGE ROUTING#
#====================================================================================#
# returns the home page html template
def homepage(user):
    return render_template('home.html',username=user,)

# if the username is valid, return the login page html template
# else, return the same page but with the incorrect username/password text
def loginpage(user="",valid=True):
    if(valid==True):
        return render_template('login.html',username=user)
    else:
        return render_template('login.html',invalid="Your username or password was incorrect")

# returns the logout page html template
def logoutpage():
    return render_template('logout.html')

# returns the register page html template
def registerpage(valid = True, error=""):
    if(valid == True):
        return render_template('register.html')
    else:
        return render_template('register.html', invalid = error)
    
# returns the stories page 
def storiespage():
    return render_template("stories.html")

def singleStory():
    return render_template("singlestory.html")

#=====================================================================================#
if __name__ == "__main__":  # false if this file imported as module
    app.debug = True  # enable PSOD, auto-server-restart on code chg
    app.run(port=8000)
