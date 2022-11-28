import os, json, datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy 
import jwt 
from functools import wraps                 # Python standard package 


# Defining the root directory for the rest of execution 
basedir = os.path.abspath(os.path.dirname(__file__))

# Creating Flask application object 
app = Flask(__name__)

# Setting configuration flags for SQLAlchemy 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SECRET_KEY'] = 'qwerty12345'        # Arbitrary value set 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Creating SQLAlchemy database object
db = SQLAlchemy(app)


# Defining the structure of the database table for Malware URLs
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
        token = None
        if ('api-access-token' in request.headers):
            token = request.headers['api-access-token']
        if (not token):
            return jsonify({"message": "Authentication token missing!!"})
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
        if (data["password"] != "admin"):       # Arbitrary value maintained (refer below)
            return jsonify({"message": "Invalid token provided!!"})
        return f(*args, **kwargs)
    return wrap


# Basic API entry endpoint 
@app.route("/")
def welcome():
    return jsonify({"message" : "Welcome!"})


# Handling the authorization 
@app.route("/login", methods=['POST']) 
def login(): 
    message = None
    if (request.method == 'POST'):
        data = request.json
        if ((data['username'] != 'admin') or (data['password'] != 'admin')):                    # Arbitrarily set credentials (refer README)
            return jsonify({"message" : "Incorrect Username and/or Password. Try again!"}) 
        else:
            # Setting authentication token with a 60 minute expiry 
            token = jwt.encode({"password" : "admin", "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
            return jsonify({"message" : "Logged in successfully!", "NOTE: api-access-token" : token})


# Handling GET request for all available malware URL database data 
@app.route("/v1/urlinfo/all")
@login_required
def view_all():
    data = MalwareURL.query.all()
    result = []   
    for ele in data:   
        ele_data = {}   
        ele_data['url'] = ele.url 
        ele_data['status'] = ele.status
        result.append(ele_data)   
    return jsonify({"available_data": result})


# Handling GET request for a specific URL's malware status 
@app.route("/v1/urlinfo/<url>")
@login_required
def lookup(url): 
    data = MalwareURL.query.filter_by(url=url).all()
    if(len(data) == 0):
        return json.loads('{"error" : "URL NOT FOUND IN DATABASE!!! Please contact Admin"}')
    if(len(data) > 1):
        return json.loads('{"error" : "INCONSISTENCIES IN DATABASE!!! Please contact Admin"}')
    result = []   
    for ele in data:   
        ele_data = {}   
        ele_data['url'] = ele.url 
        ele_data['status'] = ele.status
        result.append(ele_data)   
    return jsonify({"result": result})


# Defining and starting the server for the service 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
