# ds_protocol.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Katherine Wei
# yininw17@uci.edu
# 14645993

# TODO: ERROR HANDLING, FORMING REQUESTS, AND PARSING RESPONSES
import json
from collections import namedtuple

# Create a namedtuple to hold the values we expect to retrieve from json messages.
ServerResponse = namedtuple('ServerResponse', ['type','message', 'token'])
Message = namedtuple('Message', ['message', 'direction', 'name', 'timestamp'])

class DSPError(Exception):
    '''
    An exception to be used when received commands do not follow protocol specifications
    '''
    pass

def extract_json(json_msg:str) -> ServerResponse:
  '''
  Call the json.loads function on a json response and convert it to a DataTuple object
  '''
  try:
    json_obj = json.loads(json_msg) 
    if 'response' in json_obj:
      type = json_obj['response']['type']
      if 'message' in json_obj['response']:
        message = json_obj['response']['message']
      elif 'messages' in json_obj['response']:
        message = _extract_messages(json_obj)
      token = json_obj['response'].get('token') # some replies may not have a token
      return ServerResponse(type, message, token)
  except json.JSONDecodeError:
    print("Json cannot be decoded.")
  except Exception:
    raise DSPError

def auth_request(username: str, password: str) -> str:
  '''
  This function takes a username and password and returns a json string sent to the server
  '''
  auth = {
    "authenticate":{
      "username": username,
      "password": password
    }
  }
  return json.dumps(auth)

def direct_message_request(token: str, recipient: str, message: str, timestamp: float) -> str:
  '''
  This function takes a token, recipient, and message and returns a json string sent to the server 
  '''
  direct_message = {
    "token": token,
    "directmessage": {
      "entry": message,
      "recipient": recipient,
      "timestamp": timestamp
    }
  }
  return json.dumps(direct_message)

def fetch(token: str, what: str) -> str:
  '''
  This function takes a token and fetch (all / unread) and returns a json string sent to the server
  '''
  fetch = {
    "token": token,
    "fetch": what
    }
  return json.dumps(fetch)

def _extract_messages(json_obj: dict) -> list[Message]:
  '''
  This function takes json messages and returns a list of Message objects
  '''
  messages = []
  try:
    messages_data = json_obj['response']['messages']
    for msg in messages_data:
      message = msg['message']
      timestamp = msg['timestamp']
      if 'from' in msg:
        direction = 'received'
        name = msg['from']
      elif 'recipient' in msg:
        direction = 'sent'
        name = msg['recipient']
      messages.append(Message(message, direction, name, timestamp))
    return messages
  except json.JSONDecodeError:
    print("Json cannot be decoded.")
  except Exception:
    raise DSPError
  


