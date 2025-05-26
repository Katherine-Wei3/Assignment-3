# ds_messenger.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Katherine Wei
# yininw17@uci.edu
# 14645993

from ds_protocol import extract_json, auth_request, direct_message_request, fetch
import socket
import time
import json
from pathlib import Path

MSG_PATH = "."
MSG_FILE = "local_messages.json"
p = Path(MSG_PATH)/MSG_FILE
if not p.exists():
  p.touch()

def load_local_messages() -> list:
  if p.exists() and p.stat().st_size > 0:
    with open(p, 'r') as f:
      return json.load(f)
  return []

def save_local_messages(messages):
  with open(p, 'w') as f:
    json.dump(messages, f)

class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.sender = None
    self.timestamp = None

class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
    self.token = None
	  # more code should go in here
    self.sock = None
    self.server = dsuserver
    self.username = username
    self.password = password

    #load local message file
    self.local_messages = load_local_messages()

    self._connect(self.server, 3001)

  def _connect(self, host: str, port: int) -> None:
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.host = host
    self.port = port
    self.client.connect((self.host, self.port))

    self.send_file = self.client.makefile('w')
    self.recv = self.client.makefile('r')

    join_msg = auth_request(self.username, self.password)
    self.send_file.write(join_msg + '\r\n')
    self.send_file.flush()
    resp = self.recv.readline()
    self.response = extract_json(resp)

    try:
      if self.response and self.response.type  == 'ok':
       self.token = self.response.token
    except:
       print('Authentication Failed')

  def send(self, message:str, recipient:str) -> bool: 
    msg = direct_message_request(self.token, recipient, message, str(time.time()))
    self.send_file.write(msg + '\r\n')
    self.send_file.flush()
    resp = self.recv.readline() 
    self.response = extract_json(resp)
    if self.response and self.response.type == 'ok':
        return True
    else:
      return False

  def retrieve_new(self) -> list:
    # must return a list of DirectMessage objects containing all new messages
    self.send_file.write(fetch(self.token, 'unread') + '\r\n')
    self.send_file.flush()
    resp = self.recv.readline()
    self.response = extract_json(resp)
    
    # FIXME!!!
    if self.response:
      if self.response.message not in self.local_messages:
        self.local_messages.extend(self.response.message)
      save_local_messages(self.local_messages)
      return self.response.message
    else:
      return []
  
  def retrieve_all(self) -> list:
    # must return a list of DirectMessage objects containing all messages
    self.send_file.write(fetch(self.token, 'all') + '\r\n')
    self.send_file.flush()
    resp = self.recv.readline()
    self.response = extract_json(resp)

    if self.response:
      # FIXME!!!
      if self.response.message not in self.local_messages:
        self.local_messages.append(self.response.message)
        save_local_messages(self.local_messages)
      return self.response.message
    else:
      return []

  def close(self):
    if self.send_file:
        self.send_file.close()
    if self.recv:
        self.recv.close()
    if self.client:
        self.client.close()

  def save(self, filename: str, data: dict) -> None:
    with open(filename, 'w') as file:
        json.dump(data, file)

