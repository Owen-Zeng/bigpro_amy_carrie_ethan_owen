from flask import Flask  # facilitate flask webserving
from flask import render_template  # facilitate jinja templating
from flask import request, redirect, url_for  # facilitate form submission
from flask import session

app = Flask(__name__)  # create Flask object
app.secret_key = b'bigproer'
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
            return render_template('login.html', invalid="Your username or password was incorrect")
    else:
        return render_template('login.html')


@app.route("/home", methods=['GET', 'POST'])
def home():
    if loggedin():
        return render_template('response.html', user=session['username'])
    else:
        return redirect(url_for('login'))


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    if loggedin():
        session.pop('username', None)
        return render_template('logout.html')
    return redirect(url_for('login'))


if __name__ == "__main__":  # false if this file imported as module
    app.debug = True  # enable PSOD, auto-server-restart on code chg
    app.run()
