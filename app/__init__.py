from flask import Flask  # facilitate flask webserving
from flask import render_template  # facilitate jinja templating
from flask import request, redirect, url_for  # facilitate form submission
from flask import session
#LOGIN FUNCTIONALITY#
#====================================================================================#
app = Flask(__name__)  # create Flask object
app.secret_key = b'bigproer'

#temporary dictionary to represent pulling from SQLITE
users = {"owen" : "123", "etan" : "435"}

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


#=====================================================================================#

if __name__ == "__main__":  # false if this file imported as module
    app.debug = True  # enable PSOD, auto-server-restart on code chg
    app.run()
