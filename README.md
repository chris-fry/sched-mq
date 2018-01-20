# sched-mq
## Scheduled Messaging Queue

This is a program that stores AMQP messages and sends them at a specific time or as soon as possible after that time.

All scripts referenced in this document are contained in the src directory.

## Requirements:

* Python 3.* (runs the API for message management and the daemon that sends messages)
* Python Eve (provides the API for message management)
* MongoDB (stores messages to be sent)
* Python Pika (sends and receives AMQP messages)
* At least one AMQP queue (to receive messages)

## How it works:

* A user or system creates a message using the API, which has a simple schema including a send date/time
* The message is stored in MongoDB
* The Daemon polls MongoDB, checking for messages due to be sent
* When a message send time is reached or passed, the Daemon sends it to the specified queue, then deletes it
* The Daemon continues to check for messages
* The source code includes a testing script that can be used to monitor a queue

## Build Guide and Examples (tested on Ubuntu 16.04 LTS) (*detail to be completed*):
1. Install pre-requisites:
  * Python3 (see: [https://docs.python.org/3/using/index.html])
  * Python-Eve (see: [http://python-eve.org/install.html])
  * MongoDB (see: [https://docs.mongodb.com/manual/installation/])
  * RabbitMQ (see: [https://www.rabbitmq.com/download.html])
  * Python Pika (see: [http://pika.readthedocs.io/en/0.11.2/index.html#installing-pika])
  * Examples are performed in Ubuntu 16.04 LTS, using a Bash shell and the cURL URL data transfer command line tool ([https://curl.haxx.se/])
2. Ensure MongoDB and RabbitMQ are running
3. Start the test message consumer (run `python3 testing_monitor_queue.py`) to create the example queue and start listening.
4. Start API (run `python3 api.py`)
5. Start Daemon (run `python3 daemon.py`)

### Examples:

These examples demonstrate how to create, receive and manage messages.

They assume a local API, messaging queue and database running on default ports with no high-availability, authentication or encryption. These settings are probably not production appropriate for your needs. In particular, it's a good idea to ensure your test machine does not allow external network access to these ports using an appropriate host based firewall. In Ubuntu, this can be achieved by installing and enabling Uncomplicated Firewall (`sudo apt-get install ufw`, for more info, see: [https://wiki.ubuntu.com/UncomplicatedFirewall])

*To Do: add production-appropriate reference architecture diagram and explanation to project documentation*

The date/time parameter must be provided as seconds past the UNIX Epoch, (midnight UTC, 1 January 1970).
The following command, used throughout these examples returns this value for the current date/time:

``` date "+%s" ```

Create example message to be delivered now, should be sent and received within about 1 second:

```
$ let now=`date "+%s"`
$ curl -i -H "Content-Type: application/json" --request POST --data '{
  "datetime" : "'$now'",
  "host" :
  "localhost",
  "port" : 5672,
  "exchange" :
  "",
  "topics" :
  "hello.world",
  "queue" :
  "hello",
  "message" : {
  "hello" : "world" }}' \
  http://localhost:5000/messages

HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 282
Location: http://localhost:5000/messages/5a5df7cbbce3ac0bc8cb0682
Server: Eve/0.7.4 Werkzeug/0.11.15 Python/3.5.2
Date: Tue, 16 Jan 2018 13:02:03 GMT

{"_links": {"self": {"title": "Message", "href": "messages/5a5df7cbbce3ac0bc8cb0682"}}, "_updated": "Tue, 16 Jan 2018 13:02:03 GMT", "_status": "OK", "_etag": "d45f71e8de43fde9d64c2984841c58176f7ebda4", "_created": "Tue, 16 Jan 2018 13:02:03 GMT", "_id": "5a5df7cbbce3ac0bc8cb0682"}
```

Create example message in past (100 seconds ago), should be sent and received within about 1 second:

```
$ let past=`date "+%s"`-100
$ curl -i -H "Content-Type: application/json" --request POST --data '{
  "datetime" : "'$past'",
  "host" :
  "localhost",
  "port" : 5672,
  "exchange" :
  "",
  "topics" :
  "hello.world",
  "queue" :
  "hello",
  "message" : {
  "hello" : "world" }}' \
  http://localhost:5000/messages

HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 282
Location: http://localhost:5000/messages/5a5dfc2bbce3ac0bc8cb0684
Server: Eve/0.7.4 Werkzeug/0.11.15 Python/3.5.2
Date: Tue, 16 Jan 2018 13:20:43 GMT

{"_links": {"self": {"title": "Message", "href": "messages/5a5dfc2bbce3ac0bc8cb0684"}}, "_updated": "Tue, 16 Jan 2018 13:20:43 GMT", "_status": "OK", "_etag": "e3225eb1b5fbdad8f914e6d35c1bf438535a1ecf", "_created": "Tue, 16 Jan 2018 13:20:43 GMT", "_id": "5a5dfc2bbce3ac0bc8cb0684"}
```

Create example message scheduled to be sent in 10 seconds, should be sent and received when time arrives:

```
$ let near_future=`date "+%s"`+10
$ curl -i -H "Content-Type: application/json" --request POST --data '{
  "datetime" : "'$near_future'",
  "host" :
  "localhost",
  "port" : 5672,
  "exchange" :
  "",
  "topics" :
  "hello.world",
  "queue" :
  "hello",
  "message" : {
  "hello" : "world" }}' \
  http://localhost:5000/messages

HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 282
Location: http://localhost:5000/messages/5a5dfcaebce3ac0bc8cb0687
Server: Eve/0.7.4 Werkzeug/0.11.15 Python/3.5.2
Date: Tue, 16 Jan 2018 13:22:54 GMT

{"_links": {"self": {"title": "Message", "href": "messages/5a5dfcaebce3ac0bc8cb0687"}}, "_updated": "Tue, 16 Jan 2018 13:22:54 GMT", "_status": "OK", "_etag": "c1698343d62afece7dc561250e1ba26371c2d09b", "_created": "Tue, 16 Jan 2018 13:22:54 GMT", "_id": "5a5dfcaebce3ac0bc8cb0687"}
```

Create example message to be sent in 1 year (365.25 days), shouldn't be sent until that date:

```
$ let one_year_in_future=`date "+%s"`+31557600
$ curl -i -H "Content-Type: application/json" --request POST --data '{
  "datetime" : "'$one_year_in_future'",
  "host" :
  "localhost",
  "port" : 5672,
  "exchange" :
  "",
  "topics" :
  "hello.world",
  "queue" :
  "hello",
  "message" : {
  "hello" : "world" }}' \
  http://localhost:5000/messages

HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 282
Location: http://localhost:5000/messages/5a634d89bce3ac0bc8cb068a
Server: Eve/0.7.4 Werkzeug/0.11.15 Python/3.5.2
Date: Sat, 20 Jan 2018 14:09:13 GMT

{"_links": {"self": {"title": "Message", "href": "messages/5a634d89bce3ac0bc8cb068a"}}, "_updated": "Sat, 20 Jan 2018 14:09:13 GMT", "_status": "OK", "_etag": "e7f0db7fee58174166cc946ae81e7597c20c5317", "_created": "Sat, 20 Jan 2018 14:09:13 GMT", "_id": "5a634d89bce3ac0bc8cb068a"}
```

List all messages pending (should be just the message created for next year):
```
$ curl -i -H "Content-Type: application/json" --request GET http://localhost:5000/messages

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 588
X-Total-Count: 1
Last-Modified: Sat, 20 Jan 2018 14:09:13 GMT
Server: Eve/0.7.4 Werkzeug/0.11.15 Python/3.5.2
Date: Sat, 20 Jan 2018 14:09:53 GMT

{"_links": {"self": {"title": "messages", "href": "messages"}, "parent": {"title": "home", "href": "/"}}, "_meta": {"max_results": 25, "total": 1, "page": 1}, "_items": [{"datetime": 1548014839.0, "_links": {"self": {"title": "Message", "href": "messages/5a634d89bce3ac0bc8cb068a"}}, "_created": "Sat, 20 Jan 2018 14:09:13 GMT", "exchange": "", "_id": "5a634d89bce3ac0bc8cb068a", "message": {"hello": "world"}, "host": "localhost", "_updated": "Sat, 20 Jan 2018 14:09:13 GMT", "topics": "hello.world", "port": 5672, "queue": "hello", "_etag": "e7f0db7fee58174166cc946ae81e7597c20c5317"}]}
```

Edit example message scheduled to be sent next year (note, the etag must be included in an If-Match header for updates and deletes):
```
$ curl -i -H "Content-Type: application/json" -H "If-Match: e7f0db7fee58174166cc946ae81e7597c20c5317" --request PATCH --data '{
  "datetime" : "'$one_year_in_future'",
  "host" :
  "localhost",
  "port" : 5672,
  "exchange" :
  "",
  "topics" :
  "hello.earth",
  "queue" :
  "hello",
  "message" : {
  "hello" : "earth" }}' \
  http://localhost:5000/messages/5a634d89bce3ac0bc8cb068a

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 282
ETag: "66df41282a1c50dbb9a56c9bdd22c1ee8f758237"
Server: Eve/0.7.4 Werkzeug/0.11.15 Python/3.5.2
Date: Sat, 20 Jan 2018 14:10:48 GMT

{"_links": {"self": {"title": "Message", "href": "messages/5a634d89bce3ac0bc8cb068a"}}, "_updated": "Sat, 20 Jan 2018 14:10:48 GMT", "_status": "OK", "_etag": "66df41282a1c50dbb9a56c9bdd22c1ee8f758237", "_created": "Sat, 20 Jan 2018 14:09:13 GMT", "_id": "5a634d89bce3ac0bc8cb068a"}
```

Delete example message scheduled to be sent next year (the message will never be sent. Note, the etag must be included in an If-Match header for updates and deletes):
```
$ curl -i -H "Content-Type: application/json" -H "If-Match: 66df41282a1c50dbb9a56c9bdd22c1ee8f758237" --request DELETE http://localhost:5000/messages/5a634d89bce3ac0bc8cb068a

HTTP/1.0 204 NO CONTENT
Content-Type: application/json
Content-Length: 0
Server: Eve/0.7.4 Werkzeug/0.11.15 Python/3.5.2
Date: Sat, 20 Jan 2018 14:14:24 GMT
```

## API specification:
The API schema is defined as an Eve settings file in `api_settings.py`. This is a reasonably lean Python script that should be fairly easy to understand for anyone used to working with API's.
