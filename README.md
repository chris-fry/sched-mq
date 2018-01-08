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

## Build Guide and Examples (tested on Ubuntu 16.04) (*detail to be completed*):
1. Install pre-requisites:
  * Python3 (see: [https://docs.python.org/3/using/index.html])
  * Python-Eve (see: [http://python-eve.org/install.html])
  * MongoDB (see: [https://docs.mongodb.com/manual/installation/])
  * RabbitMQ (see: [https://www.rabbitmq.com/download.html])
  * Python Pika (see: [http://pika.readthedocs.io/en/0.11.2/index.html#installing-pika])
2. Ensure MongoDB and RabbitMQ are running
3. Start the test message consumer (run `python3 testing_monitor_queue.py`) to create the example queue and start listening.
4. Start API (run `python3 api.py`)
5. Start Daemon (run `python3 daemon.py`)
6. Create test message in past, should be sent and received immediately
  * *To Complete...*
7. Create test message in near future, should be sent and received when time arrives
  * *To Complete...*
8. Create test message in distant future, shouldn't be sent (before date specified)
  * *To Complete...*
9. List all messages pending
  * *To Complete...*
10. Edit test message in distant future
  * *To Complete...*
11. Delete test message in distant future
  * *To Complete...*

## API specification:
The API schema is defined as an Eve settings file in `api_settings.py`. This is a reasonably lean python script that should be fairly simple to understand for anyone used to working with API's.
