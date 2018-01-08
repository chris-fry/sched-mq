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
  * Tests are performed in Ubuntu 16.04 LTS, using a Bash shell and the cURL URL data transfer command line tool ([https://curl.haxx.se/])
2. Ensure MongoDB and RabbitMQ are running
3. Start the test message consumer (run `python3 testing_monitor_queue.py`) to create the example queue and start listening.
4. Start API (run `python3 api.py`)
5. Start Daemon (run `python3 daemon.py`)

### Testing:

These tests demonstrate how to create, receive and manage messages.

They assume a local API, messaging queue and database running on default ports with no high-availability, authentication or encryption. These settings are probably not production appropriate for your needs. In particular, it's a good idea to ensure your test machine does not allow external network access to these ports using an appropriate host based firewall. In Ubuntu, this can be achieved by installing and enabling Uncomplicated Firewall (`sudo apt-get install ufw`, for more info, see: [https://wiki.ubuntu.com/UncomplicatedFirewall])

*To Do: add production-appropriate reference architecture diagram and explanation to project documentation*

The following command, used throughout these examples returns the current date/time as seconds past the epoch:

``` date "+%s" ```

Create test message to be delivered now, should be sent and received within about 1 second:

``` let now=`date "+%s"` ```

*To be completed...*

Create test message in past (100 seconds ago), should be sent and received within about 1 second:

``` let past=`date "+%s"`-100 ```

*To be completed...*

Create test message in near future, should be sent and received when time arrives:

``` let near_future=`date "+%s"`+10 ```

*To be completed...*

Create test message to be sent in about 1 year (365.25 days), shouldn't be sent until that date:

```let one_year_in_future=`date "+%s"`+31557600 ```

*To be completed...*

List all messages pending (should be just the message created for next year):

*To be completed...*

Edit test message in distant future:

*To be completed...*

Delete test message in distant future:

*To be completed...*

## API specification:
The API schema is defined as an Eve settings file in `api_settings.py`. This is a reasonably lean python script that should be fairly simple to understand for anyone used to working with API's.
