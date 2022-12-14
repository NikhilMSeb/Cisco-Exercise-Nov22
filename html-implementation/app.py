import os 
from flask import Flask, render_template, request, session, redirect, url_for, flash 
from flask_sqlalchemy import SQLAlchemy 
from functools import wraps                 # Python standard package 


# Defining the root directory for the rest of execution 
basedir = os.path.abspath(os.path.dirname(__file__))

# Creating Flask application object 
app = Flask(__name__)

# Setting arbitrary secret key for authentication & authorization 
app.secret_key = 'qwerty12345'

# Setting configuration flag for storing the SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

# Creating SQLAlchemy database object
db = SQLAlchemy(app)


# Defining the structure of the table 
class MalwareURL(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)

    def __init__(self, url, status):
        self.url = url
        self.status = status

    def __repr__(self):
        return '{}'.format(self.status)         # Returning only the status of a given URL


# Defining the enforcing of logging in for access 
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if ('logged_in' in session):
            return f(*args, **kwargs)
        else:
            flash('LOG IN REQUIRED TO ACCESS ATTEMPTED PAGE')
            return redirect(url_for('login'))
    return wrap


# Pre log in landing page 
@app.route("/")
def welcome():
    return render_template('welcome.html') 


# Post log in landing page
@app.route("/home")
@login_required
def home():
    return render_template("home.html")


# Handling the authentication and authorization (logging in and logging out)
@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if (request.method == 'POST'):
        if ((request.form['username'] != 'admin') or (request.form['password'] != 'admin')):        # Arbitrarily set credentials (refer README)
            error = 'Incorrect Username and/or Password. Try again!'
        else:
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route("/logout")
@login_required
def logout():
    session.pop('logged_in', None)
    return render_template('logout.html')


# Handling GET request for all available malware URL database data 
@app.route("/v1/urlinfo/all")
@login_required
def view_all():
    malware_status = MalwareURL.query.all()
    return render_template("all.html", malware_status=malware_status)


# Handling GET request for a specific URL's malware status 
@app.route("/v1/urlinfo/<url>")
@login_required
def lookup(url): 
    result = MalwareURL.query.filter_by(url=url).all()
    if(len(result) == 0):
        result = ["URL NOT FOUND IN DATABASE!!! Please contact Admin"]
    if(len(result) > 1):
        result = ["INCONSISTENCIES IN DATABASE!!! Please contact Admin"]
    return render_template("lookup.html", url=url, result=result)


# Defining and starting the server for the service 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
