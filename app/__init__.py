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
c.execute("CREATE TABLE IF NOT EXISTS stories(storyTitle TEXT PRIMARY KEY NOT NULL, content TEXT, previousEdit TEXT, storyLink TEXT, author TEXT);")

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
# dict of all stories
storyDict={}

for row in c.execute(f"SELECT storyTitle, content FROM stories;"):
    storyDict.update({row[0]:row[1]})

print(storyDict)

# dict of usernames:password
users={}

for row in c.execute("SELECT * FROM user_profile;"):
    users.update({row[0]:row[1]})

print(users)

#dict of editors and authors
editors={}
authors={}
for row in c.execute("SELECT * FROM authors;"):
    editors.update({row[0]:row[1]})
for row in c.execute("SELECT storyTitle, author FROM stories;"):
    authors.update({row[0]:row[1]})

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
    edittedStories = {}
    for key, value in editors.items():
        if (value == session['username']):
            edittedStories.update({key, value})

    if loggedin():
        return homepage(session['username'], edittedStories)
    else:
        return redirect(url_for('register'))

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    # if logged in, remove username key from dict
    if loggedin():
        session.pop('username', None)
        return logoutpage()
    return redirect(url_for('login'))

#Stories
#==========================================================================#

@app.route("/stories")
def stories(name=""):
    if loggedin():
        return storiespage()
    else:
        return redirect(url_for('login'))

@app.route("/singlestory", methods=['GET', 'POST'])
def singlestory():
    if loggedin():
        if request.method == 'POST':
            givenTitle = request.form['title']

            with sqlite3.connect(DB_FILE) as db:
                c = db.cursor()
                if(givenTitle == "" or request.form['content'] == ""):
                    return singlestorypage("", False, "Enter valid content/title")
                if(givenTitle in storyDict):
                    return singlestorypage("", False, "That title is taken")
                else:
                    c.execute(f"INSERT OR REPLACE INTO stories VALUES ('{givenTitle}', '{request.form['content']}', '{request.form['content']}', '/singlestory/{givenTitle}', '{session['username']}');")
                    c.execute(f"INSERT OR REPLACE INTO authors VALUES ('{session['username']}', '{givenTitle}')")
                    storyDict[givenTitle] = request.form['content']
                    editors.update({session['username']:givenTitle})
                    authors.update({givenTitle:session['username']})
            session.permanent = True
            return redirect(url_for('createdstory', link=givenTitle))
        return singlestorypage()
    return redirect(url_for('login'))

@app.route("/singlestory/<link>", methods=['GET', 'POST'])
def createdstory(link):
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
       
        hasEdit="hidden"
        if(session['username'] not in editors):
            hasEdit="text"
            if(session['username']!=authors[link]):
                if request.method == 'POST':
                    recentEdit=request.form['edit']
                    updatedStory=storyDict[link] + "\n" + recentEdit
                    c.execute(f"UPDATE stories SET content = '{updatedStory}' WHERE storyTitle = '{link}';")
                    c.execute(f"UPDATE stories SET previousEdit = '{recentEdit}' WHERE storyTitle = '{link}';")
                    c.execute(f"INSERT OR REPLACE INTO authors VALUES ('{session['username']}', '{link}');")
                    hasEdit="hidden"
        c.execute(f"SELECT storyTitle, content FROM stories WHERE storyTitle = '{link}'")
        storyRow = c.fetchone()
        c.execute(f"SELECT username FROM authors WHERE storyTitle = '{link}'")
        authorRow = c.fetchone()
        if (storyRow is None):
            return "Story doesn't exist"
        storyDict[storyRow[0]] = storyRow[1]
        print(storyDict)
        
    session.permanent = True
    return createdstorypage(storyRow[0], storyRow[1], True, hasEdit) # we dont have to redirect here

def author(storyName):
    return authors.get(storyName)

#WEBPAGE ROUTING#
#====================================================================================#
# returns the home page html template
def homepage(user, edits):
    return render_template('home.html',username=user, edited_stories = edits )

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

    return render_template("stories.html", stories=authors)

def singlestorypage(name="", valid = True, error=""):

    return render_template("singlestory.html", storyName=name, invalid = error)

def createdstorypage(title="", content="", valid = True,hasEdit=""):
    return render_template("createdstory.html", storyTitle=title, storyContent = content,edit=hasEdit)

#Navbar below:
#=====================================================================================#

#=====================================================================================#
if __name__ == "__main__":  # false if this file imported as module
    app.debug = True  # enable PSOD, auto-server-restart on code chg
    app.run()
