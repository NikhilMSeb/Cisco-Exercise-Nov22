# JSON Implementation

This directory contains the exercise solution implemented such that the outputs are JSON-based. 

## Design Choices & Overview  

1. Lookup Service API 

An industry standard for building APIs is the REST architecture, and of the many frameworks for building REST APIs with Python this service uses **Flask**. 
Flask provides all the key requirements for this service out-of-the-box without needing too much overhead infrastructure. 
Flask is also easy to deploy to production, and has comprehensive documentation and support due to its existing wide usage. 

In the current implementation, I have built all API endpoints to be accessed, handled and provide outputs in JSON and through direct API requests, hence allowing this to be directly integrated with a service that wants to perform a lookup as a single part of a larger workflow. 

2. Database of Malware URLs 

This implementation will leverage **SQLAlchemy** and its in-built features instead of a larger setup for the sake of simplicity. 
SQLAlchemy provides a fully featured SQL abstraction toolkit so that this solution is still scalable, and its object-relational mapper (ORM) allows the model itself and the database schema to be cleanly decoupled. 
So we can simulate our database requirements without needing the intensive set-up of a complete SQL-based database. 

In the current implementation, I have provided some arbitrary URLs and statuses for looking up. They can be edited as described below. 

*Note on Authorization implementation:*

The current implementation of authorization and authentication in this service uses just "admin" as both the username and password as an arbitrary choice - a more complex and production-scale version of this would be to also add a table in the database for registered users and allow for an access-restricted sign up process. This would enable personalized and more secure access credentials. 

This would allow for more complex password hashing (as provided by the "werkzeug.security" package for example). We can also then eliminate the need for manual authorization tokens as is in the current implementation (as you will see below), and instead store the latest available token for access on a per-user basis in the database itself. 

## Setup Instructions 

1. Clone this Github repository locally if not already done (the command below can be used)

> git clone https://github.com/NikhilMSeb/Cisco-Exercise-Nov22.git

2. Technical Prerequisites 

Assuming that both Python (3.x) and Pip are installed in your system (if not refer [this](https://www.python.org/downloads/) for installing both, or [this](https://pip.pypa.io/en/stable/installation/) for pip):

There are 3 pre-requisite libraries for running this service - Flask, FLask-SQLAlchemy and PyJWT - all of which can be installed using the following terminal command: 

*You can also add these prerequisites in a virtual environment by following the instructions [here](https://virtualenv.pypa.io/en/latest/installation.html)*

> pip install -U Flask Flask-SQLAlchemy pyjwt

3. Setting up the test Database

Executing the **create_db.py** script will create the required database (with dummy data) in the root repository folder: 

> python create_db.py

The values in this database can be adjusted if needed by directly editing the file [here](https://github.com/NikhilMSeb/Cisco-Exercise-Nov22/blob/main/create_db.py) 

*[Note: Running the database creation script multiple times can cause data duplication]*

## Testing Demo 

The testing of this requires usage of the **Postman** platform - it can be downloaded [here](https://www.postman.com/downloads/), and you can sign up for a free account!

Following that, the 2 key functionalities of this service can be tested using the folllowing steps:

1. Start running the service using the following command in this directory: 

> python app.py

2. Visit the landing endpoint of the API below through a Postman GET request (refer picture), and confirm it is running with no issues: 

> http://127.0.0.1:8000/

Request:
![image](https://user-images.githubusercontent.com/46250395/204472445-7ec3eeb2-0684-43fc-a031-71a42f73d711.png)

Response: 
![image](https://user-images.githubusercontent.com/46250395/204472543-88bd8616-0966-40e0-aeb7-a1506c865c3c.png) 

3. Authenticate through login via the endpoint below through a Postman POST request (refer picture) using username and password both as "admin":

> http://127.0.0.1:8000/login

Request:
![image](https://user-images.githubusercontent.com/46250395/204473169-a82918a8-05b2-4ebc-8c44-8fadfe96d9b9.png)

Alternatively you can also attempt to access any of the further endpoints below, but you will be met with a log in requirement!

Make note of the 'api-access-token' in the response as that will be your **authorization token** moving forward. 

Response:
![image](https://user-images.githubusercontent.com/46250395/204473638-7b691650-5b90-4d02-a6eb-22b365eca0b8.png)

4. Visit the following endpoint through a Postman GET request (refer picture) to see a list of all stored URLs and their statuses from the database: 

> http://127.0.0.1:8000/v1/urlinfo/all

**Note:** You need to first add the authorization token to the header of your request to gain access 

Request:
![image](https://user-images.githubusercontent.com/46250395/204474248-5a6abdb9-f3a2-494e-a5ea-7352c687173b.png)

Response:
![image](https://user-images.githubusercontent.com/46250395/204474513-b3f83851-c189-4473-a49b-ec8c889acde0.png)

5. Visit the following endpoint through a Postman GET request (refer picture) with your own input to obtain the status of a specific URL in the database: 

**Note:** Continue to add the authorization token to the header of your request to gain access 

> http://127.0.0.1:8000/v1/urlinfo/{url}

*[Available URLs in dummy data: cisco.com, evil.com, google.com, criminal.com, nikhil.accept, nikhil.reject]*

Request:
![image](https://user-images.githubusercontent.com/46250395/204474898-561ca78c-71fc-484f-b8c0-64c13570bebc.png)

Response:
![image](https://user-images.githubusercontent.com/46250395/204474756-761d1f7a-9450-4be1-8e33-9eb598c348b4.png)

6. Play around as you like!

Try different API requests as you choose, but keeping in mind that your authorization token expires in 1 hour. 

7. Outside of manual testing, you can run the unit tests for this service by executing the following command in this directory: 

> python .\test.py -v

## Additional Development 

1. The size of the URL list could grow infinitely, how might you scale this beyond the memory capacity of the system? 

Answer: The option I would suggest for this is remote "unlimited" databases. This is of course not implemented for this coding exercise, but is an option if we are considering this service at a production level. 

Unlimited storage databases, or "bottomless" databases, are kept on remote object storage. The use of remote storage separates where data is stored and where the data is processed. Because unlimited storage databases are stored remotely, their size is not limited by the size of local cluster storage, but rather only by available external object storage. On public cloud object stores, this is for all practical purposes unlimited. Popular vendor options for this approach include Sync, Dropbox and Box. 

2. The number of requests may exceed the capacity of this system, how might you solve that? 

Answer: There are 2 approaches that tackle the issue of request overload in a straightforward manner - queueing requests and caching requests. Neither of these have been implemented for this coding exercise. 

Queueing requests allows for storing multiple incoming requests, and even to sort these in order of priority and return responses after processing. A very straightforward approach to implementing this might be to use a Redis task queue along with the Flask API - we would just need to set up a worker to listen for queued tasks, a Redis connection to enqueue incoming requests, and handle them as wanted. 

Caching requests works by storing frequently accessed data along the request-response path to readily provide as compared to processing it in real-time. This is actually supported by the RESTful architecture as well. To implement this, we could use existing packages like Flask-Cache and leverage their underlying functionality, along with a connection service (potentially Redis again) to faciliate this. 

3. What are some strategies you might use to update the service with new URLs? Updates may be as many as 5000 URLs a day with updates arriving every 10 minutes.

Answer: While this implementation is at a small scale for the exercise, we can easily scale this up to millions of URLs using a cloud computing platform - for the sake of discussion, say AWS. 

Raw URL data can be stored in S3 buckets in the form of CSV files. Updates to the CSV files can be done manually or through a parallel data pipeline. This raw data can then be parsed through something like Glue service to maintain a table in a cloud database (or multiple tables/databases as needed). This final database of data can then be accessed programatically, while we can also leverage access management and other features of the cloud service itself. 

Cloud computing over here would allow for scaling up without worrying about the architectural overhead, higher performance and availability, as well as overall cost reduction in the long term. 

## Resources Used 

* https://realpython.com/api-integration-in-python/
* https://www.tutorialspoint.com/flask/index.htm
* https://hackersandslackers.com/database-queries-sqlalchemy-orm/
* https://pyjwt.readthedocs.io/en/stable/
* https://docs.python.org/3/library/unittest.html 
