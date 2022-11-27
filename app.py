import os 
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 


# Defining the root directory for the rest of execution 
basedir = os.path.abspath(os.path.dirname(__file__))


# Creating Flask application object 
app = Flask(__name__)


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


# Base entry point for the API
@app.route("/")
def home():
    return render_template("home.html")


# Handling GET request for all available malware URL database data 
@app.route("/v1/urlinfo/all")
def view_all():
    malware_status = MalwareURL.query.all()
    return render_template("all.html", malware_status=malware_status)


# Handling GET request for a specific URL's malware status 
@app.route("/v1/urlinfo/<url>")
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
