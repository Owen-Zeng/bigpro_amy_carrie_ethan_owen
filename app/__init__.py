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
c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT NOT NULL);")
c.execute(f"INSERT OR REPLACE INTO users VALUES('owen', '123');")
c.execute(f"INSERT OR REPLACE INTO users VALUES('Ethan', 'salad');")

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
    elif (request.method == "GET"):
        return redirect(url_for('register'))
    else:
        return loginpage(valid=True)

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


#IMPORTANT PLEASE READ TO SAVE YOURSELF TIME THIS REGISTER DOES NOT CHECK WHETHER THE INPUTS ARE REPEATED, WHICH WILL PROB CAUSE ERRORS
@app.route("/register", methods=['POST'])
def register():
    # isRegistering = request.args["register"]
    if request.method=='POST':
        username=request.form.get('id')
        password=request.form.get('pass')
        return registerpage(username,password)
    return registerpage()
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
def registerpage(username="",password="",valid= True):
     if(valid==True):
        return render_template('register.html')
     else:
        return render_template('register.html', invalid="Your username or password was incorrect")

#=====================================================================================#

if __name__ == "__main__":  # false if this file imported as module
    app.debug = True  # enable PSOD, auto-server-restart on code chg
    app.run()
