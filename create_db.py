import app 
from app import * 

with app.app_context():
    # create the database and the db table
    db.create_all()

    # insert data
    db.session.add(MalwareURL("cisco.com", "GOOD"))
    db.session.add(MalwareURL("evil.com", "BAD"))
    db.session.add(MalwareURL("google.com", "GOOD"))
    db.session.add(MalwareURL("criminal.com", "BAD"))
    db.session.add(MalwareURL("nikhil.accept", "GOOD"))
    db.session.add(MalwareURL("nikhil.reject", "BAD"))

    # commit the changes
    db.session.commit()
