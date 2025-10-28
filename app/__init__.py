from flask import Flask  # facilitate flask webserving
from flask import render_template  # facilitate jinja templating
from flask import request, redirect, url_for  # facilitate form submission
from flask import session
import sqlite3   #enable control of an sqlite database
#SQLITE3 Databases
#====================================================================================#
DB_FILE="webstory.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()
c.execute("CREATE TABLE IF NOT EXISTS user_profile(username TEXT PRIMARY KEY NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL);")
c.execute("CREATE TABLE IF NOT EXISTS stories(storyTitle TEXT PRIMARY KEY NOT NULL, content TEXT, previousEdit TEXT, storyLink TEXT);")
c.execute("CREATE TABLE IF NOT EXISTS authors(username TEXT, storyTitle TEXT);")


#REGISTER FUNCTIONALITY
#====================================================================================#

def register():
    if loggedin():
        return "Logged In"
    else:
        return 1

#LOGIN FUNCTIONALITY#
#====================================================================================#
app = Flask(__name__)  # create Flask object
app.secret_key = b'bigproer'

users={}

c.execute("SELECT * FROM users username;")
username_roster=c.fetchall()
for i in range(len(username_roster)):
    users.update({username_roster[i][0]:username_roster[i][1]})


db.commit() #save changes
db.close()  #close database
#temporary dictionary to represent pulling from SQLITE


def loggedin():
    if 'username' in session:
        return True
    return False

@app.route("/", methods=['GET', 'POST'])
def response():
    if loggedin():
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if loggedin():
        return redirect(url_for('home'))
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
    if loggedin():
        session.pop('username', None)
        return logoutpage()
    return redirect(url_for('login'))

#WEBPAGE ROUTING#
#====================================================================================#
def homepage(soul,a="Thetha"):
    return render_template('home.html',user=soul,)
def loginpage(soul="",valid= True):
    if(valid==True):
        return render_template('login.html',user=soul)
    else:
        return render_template('login.html',invalid="Your username or password was incorrect")
def logoutpage():
    return render_template('logout.html')
def registerpage():
    return render_template('register.html')

#=====================================================================================#

if __name__ == "__main__":  # false if this file imported as module
    app.debug = True  # enable PSOD, auto-server-restart on code chg
    app.run()
