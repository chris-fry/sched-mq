import pika, daemon_settings
from json import dumps
from pymongo import ASCENDING, MongoClient
from time import sleep, strftime, time

messages_collection = "messages"

message_count = 0

# Connect to database
db = MongoClient(
  daemon_settings.mongo_host,
  daemon_settings.mongo_port
)[daemon_settings.db_name]

# Polls the message database and sends any messages when due
def run_daemon():
  print(" [*] Daemon started. To stop, press CTRL+C or kill process.")
  while True:
    message = get_next_message()
    if message is None or message['datetime'] > time():
      sleep(daemon_settings.polling_freq)
    else:
      publish(message)

# Get's next message ordered by date
def get_next_message():
  message = db[messages_collection].find_one(
    filter={},
    sort=[('datetime', ASCENDING), ('_id', ASCENDING)]
  )
  return(message)

def publish(message):
  try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(
      host=message['host'],
      port=message['port']
    ))
    channel = connection.channel()
    channel.basic_publish(
      exchange=message['exchange'],
      routing_key=message['queue'],
      body=dumps(message['message'])
    )
    print("{} - sent: {}".format(globals()['message_count'] + 1, message['message']))
    connection.close()
    # Remove message from database
    deleted = db[messages_collection].delete_one({'_id': message['_id']})
    if not deleted.raw_result['ok']:
      time_str = strftime('%Y-%m-%d %H:%M:%S', gmtime(time()))
      print("{}: Error removing message {}".format(time_str, message['_id']))
      sleep(5)
    globals()["message_count"] += 1
  except pika.exceptions.ConnectionClosed:
    print("Error for message _id: {}: Could not connect to host {}, port {}".format(
      message['_id'], message['host'], message['port']
    ))
    sleep(5)

run_daemon()
