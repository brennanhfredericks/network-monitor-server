# network-monitor-server
consumer of data generate by network-monitor-client

# Flask API

## WSGI application
- [x] uWSGI (HTTP) listening on port 5050 and passing request to Flask (WSGI) application

## Database
- [x] configured low privilege Mysql user for the application
- [x] address table name issue for `i_pv4`, `i_pv6`,`AF__packet` 
## Endpoints
- [x] `/packets`
  - endpoint used to submit captured packet data
- [x] `/packets/tables`
  - endpoint to retrieve a list of protocols available
- [x] `/packets/tables/<protocol>`
  - endpoint to retrieve the number of entries available
- [] `/packets/tables/view?ProtocolName=af_packet;Limit=100;`
- [x] `/packets/tables/all`
  - endpoint to retrieve the number of entries avaialale for all protocols


# Nginx
## Reverse proxy
- HTTP
  - listening on port 5050
  - locations
    - [] /
      - nothing implemented yet
    - [x] `/packets` 
      - forwarding request to flask_api uwsgi


# Mysql

## Users
- [x] low privilege account for the flask_api user. not allowed drop tables/databases or create users  

## Databases
- [x] database for the packets received by the flask_api.
  - [x] all protocols have their own table. one to many relationship

# TODO
- [] Decomple api from database. Currently the client waits for a response from the api, while the api insert data in the database.
  - Options
    - Redis Publish/Subcribe:
      - flask api side
      - create new thread at api startup and only stop thread when api shutdown
      - use a queue to pass data from the endpoints (that need to be store in database) to thread. Once the enpoint has added the data recieved from the client to the queue in can response to the client with 200 or failure. 
      - in the thread create a asynchronous redis client that publishes data to different channels depending on the endpoint that added the data to the queue

      - mysql side
      - create a asynchronous redis client that subcribes to predetermined channels. once data is received the data should be added to the database.

# Issue:
- At some point database stops inserting new data, don't know the reason. need to investigate database logs

- 