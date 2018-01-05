MONGO_HOST = 'localhost'
MONGO_DBNAME = 'sched-mq'
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']
messages_schema = {
  # UTC Date/Time to send the message as seconds after Epoch
  'datetime': {
    'type': 'float',
    'required': True
  },
  # AMQP hostname
  'host': {
    'type': 'string',
    'required': True
  },
  # AMQP port
  'port': {
    'type': 'integer',
    'required': True
  },
  # AMQP exchange
  'exchange': {
    'type': 'string',
    'required': True
  },
  # AMQP queue
  'queue': {
    'type': 'string',
    'required': True
  },
  # AMQP Message Topics string
  'topics': {
    'type': 'string'
  },
  # Message as string
  'message': {
    'type': 'string',
    'required': True
  }
}
messages = {
  'schema': messages_schema
}
DOMAIN = {
  'messages': messages
}
