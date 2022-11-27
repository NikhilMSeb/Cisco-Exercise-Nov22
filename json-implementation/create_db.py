# Importing all database and table definitions from primary "app.py" 
import app 
from app import * 

with app.app_context():
    # Create the database and the database table
    db.create_all()

    # Insert the data
    db.session.add(MalwareURL("cisco.com", "GOOD"))
    db.session.add(MalwareURL("evil.com", "BAD"))
    db.session.add(MalwareURL("google.com", "GOOD"))
    db.session.add(MalwareURL("criminal.com", "BAD"))
    db.session.add(MalwareURL("nikhil.accept", "GOOD"))
    db.session.add(MalwareURL("nikhil.reject", "BAD"))
    # Format to add further data points: db.session.add(MalwareURL("url", "status"))

    # Commit the changes
    db.session.commit()
