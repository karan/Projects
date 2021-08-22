# API Endpoint for Proverbs project
Simple project written in C for fetching some data from MongoDB and presenting it on an API endpoint listening on port 4040

Dependencies:
* libmongoc
* libjansson
* libmicrohttpd

TODO:

* At the moment only 10 entries are returned from DB, need to find out how to send data in chunks ( maybe while loop? ).
* Need to make this run on multi threading
