import os 
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

class MalwareURL(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)

    def __init__(self, url, status):
        self.url = url
        self.status = status

    def __repr__(self):
        return '{}'.format(self.status)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/v1/urlinfo/all")
def view_all():
    malware_status = MalwareURL.query.all()
    return render_template("all.html", malware_status=malware_status)

@app.route("/v1/urlinfo/<url>")
def lookup(url): 
    result = MalwareURL.query.filter_by(url=url).all()
    if(len(result) == 0):
        result = ["URL NOT FOUND IN DATABASE!!! Please contact Admin"]
    if(len(result) > 1):
        result = ["INCONSISTENCIES IN DATABASE!!! Please contact Admin"]
    return render_template("lookup.html", url=url, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
