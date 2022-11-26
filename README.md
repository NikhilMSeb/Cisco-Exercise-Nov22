# Cisco-Exercise-Nov22

Git repo to track and share the project built as part of the "Malware URL Lookup" exercise for Cisco Cloud Security recruiting 


## Design Overview 

1. Lookup Web Service API 

An industry standard for building APIs is the REST architecture, and of the many frameworks for building REST APIs with Python this service uses Flask. 
Flask provides all the key requirements for this service out-of-the-box without needing too much overhead infrastructure. 
Flask is also easy to deploy to production, and has comprehensive documentation and support due to its existing wide usage. 

2. Database of Malware URLs 

This implementation will be using SQLite to replicate the "databases of malware URLs" because we will have relatively-low traffic and be read-heavy. 
This will simulate our database requirements for testing and demos, without needing the intensive set-up of a complete SQL-based database. 


## Setup Instructions 

TBD


## Additional Development 

1. The size of the URL list could grow infinitely, how might you scale this beyond the memory capacity of the system? 

2. The number of requests may exceed the capacity of this system, how might you solve that? 

3. What are some strategies you might use to update the service with new URLs? Updates may be as many as 5000 URLs a day with updates arriving every 10 minutes.


## Resourced Used 

TBD
