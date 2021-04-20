# network-monitor-server
consumer of data generate by network-monitor-client

# Flask API

## WSGI application
- [x] uWSGI (HTTP) listening on port 5050 and passing request to Flask (WSGI) application

## Database
- [x] configured low privilege Mysql user for the application
- [] address table name issue for `i_pv4`, `i_pv6`,`AF__packet` 
## Endpoints
- [x] packets/
  - endpoint used to submit captured packet data

- [] packets_stats/
  - endpoint used to report on the number of packets in the database (and tables)

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