# HTML Implementation

This directory contains the exercise solution implemented such that the outputs are HTML-based. 


## Design Choices & Overview  

1. Lookup Web Service API 

An industry standard for building APIs is the REST architecture, and of the many frameworks for building REST APIs with Python this service uses **Flask**. 
Flask provides all the key requirements for this service out-of-the-box without needing too much overhead infrastructure. 
Flask is also easy to deploy to production, and has comprehensive documentation and support due to its existing wide usage. 

In the current implementation, I have constructed HTML webpages to explicitly demonstrate the outputs. 
This service can easily be adapted to instead provide outputs to be used internally by JSON serializing the responses of the GET requests. 

2. Database of Malware URLs 

This implementation will leverage **SQLAlchemy** and its in-built features instead of a larger setup for the sake of simplicity. 
SQLAlchemy provides a fully featured SQL abstraction toolkit so that this solution is still scalable, and its object-relational mapper (ORM) allows the model itself and the database schema to be cleanly decoupled. 
So we can simulate our database requirements without needing the intensive set-up of a complete SQL-based database. 

In the current implementation, I have provided some arbitrary URLs and statuses for looking up. They can be edited as described below. 

## Setup Instructions 

1. Clone this Github repository locally (the command below can be used)

> git clone https://github.com/NikhilMSeb/Cisco-Exercise-Nov22.git

2. Technical Prerequisites 

Assuming that both Python (3.x) and Pip are installed in your system (if not refer [this](https://www.python.org/downloads/) for installing both, or [this](https://pip.pypa.io/en/stable/installation/) for pip):

There are 2 pre-requisite libraries for running this service - Flask and FLask-SQLAlchemy - both of which can be installed using the following terminal command: 

*You can also add these prerequisites in a virtual environment by following the instructions [here](https://virtualenv.pypa.io/en/latest/installation.html)*

> pip install Flask Flask-SQLAlchemy

3. Setting up the test Database

Executing the **create_db.py** script will create the required database (with dummy data) in the root repository folder: 

> python create_db.py

The values in this database can be adjusted if needed by directly editing the file [here](https://github.com/NikhilMSeb/Cisco-Exercise-Nov22/blob/main/create_db.py) 

## Testing Demo 

The 2 key functionalities of this service can be tested using the folllowing steps:

1. Start running the service using the following command: 

> python app.py

2. Visit the landing endpoint of the API below in your broswer and confirm it is running with no issues: 

> http://localhost:8000

ADD new photo 

ADD
Follow the instructions to log in (feel free to try accessing other without)

ADD
After logging in, can follow list (same as below)

3. Visit the following endpoint in your browser to see a list of all stored URLs and their statuses from the database: 

> http://localhost:8000/v1/urlinfo/all

ADD new photo 

4. Visit the following endpoint in your browser (with your own input) to obtain the status of a specific URL in the database: 

> http://localhost:8000/v1/urlinfo/{url}

*[Available URLs in dummy data: cisco.com, evil.com, google.com, criminal.com, nikhil.accept, nikhil.reject]*

ADD new photo 

ADD logging out try - play around as you like! 

## Additional Development 

1. The size of the URL list could grow infinitely, how might you scale this beyond the memory capacity of the system? 

Answer: 

2. The number of requests may exceed the capacity of this system, how might you solve that? 

Answer: 

3. What are some strategies you might use to update the service with new URLs? Updates may be as many as 5000 URLs a day with updates arriving every 10 minutes.

Answer: While this implementation is at a small scale for the exercise, we can easily scale this up to thousands of URLs using a cloud computing platform - for the sake of discussion, say AWS. 

Raw URL data can be stored in S3 buckets in the form of CSV files. Updates to the CSV files 

Cloud computing 

## Resources Used 

* https://realpython.com/api-integration-in-python/
* https://www.tutorialspoint.com/flask/index.htm
* https://hackersandslackers.com/database-queries-sqlalchemy-orm/
* https://realpython.com/token-based-authentication-with-flask/
