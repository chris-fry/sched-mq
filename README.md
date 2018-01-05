# sched-mq
## Scheduled Messaging Queue

This is a program that stores AMQP messages and sends them at a specific time or as soon as possible after that time.

## Requirements:
* Python 3.* (runs the API for message management and the daemon that sends messages)
* Python Eve (supports the API for message management)
* MongoDB (stores messages to be sent)
* At least one AMQP queue (to receive messages)

## How it works:
* A user or system creates a message using the API, which has a simple schema including a send date/time
* The message is stored in MongoDB
* The Daemon watches polls MongoDB, checking for messages due to be sent (messages created with a past date/time are sent immediately)
* When a message send time is reached, the Daemon sends it to the specified queue, then deletes it
* The Daemon continues to check for messages
* The source code includes a testing script that can be used to monitor a queue

## Example:

### Create a message:
*To be completed*

### Message received using test script:
*To be completed*

## Building a PoC (Tested on Ubuntu 16.04) (*detail to be completed*):
1. Install pre-requisites:
  * Python3
  * Python-Eve
  * RabbitMQ
2. Create test queue
3. Start API
4. Start Daemon
5. Start test message consumer
6. Create test message in past, should be sent and received immediately
7. Create test message in near future, should be sent and received when time arrives
8. Create test message in distant future, shouldn't be sent (before date specified)
9. List all messages pending
10. Edit test message in distant future
11. Delete test message in distant future
