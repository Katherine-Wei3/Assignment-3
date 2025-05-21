# ds_messenger.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Katherine Wei
# yininw17@uci.edu
# 14645993

from ds_protocol import extract_json, auth_request, direct_message_request, fetch
import socket
import time

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
    self._connect(dsuserver, 3001)
  
  def _connect(self, host: str, port: int) -> None:
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.host = host
    self.port = port
    self.sock.connect((self.host, self.port))
    self.sock.settimeout(3)
    self.send_file = self.sock.makefile('w')
    self.recv = self.sock.makefile('r')
    	
    join_msg = auth_request(self.username, self.password)
    self.send_file.write(join_msg + '\r\n')
    self.send_file.flush()
    self.response = extract_json(self.recv.readline())
    try:
      if self.response.type == 'ok':
       self.token = self.response.token
    except:
       print('Authentication Failed')

  def send(self, message:str, recipient:str) -> bool: 
    try:
        msg = direct_message_request(self.token, recipient, message, str(time.time()))
        self.send_file.write(msg + '\r\n')
        self.send_file.flush()
        return True 
    except Exception as e:
        print("Failed to send:", e)
        return False

  def retrieve_new(self) -> list:
    # must return a list of DirectMessage objects containing all new messages
    self.send_file.write(fetch(self.token, 'unread') + '\r\n')
    self.send_file.flush()
    self.response = extract_json(self.recv.readline())
    return self.response.message
  
  def retrieve_all(self) -> list:
    # must return a list of DirectMessage objects containing all messages
    self.send_file.write(fetch(self.token, 'unread') + '\r\n')
    self.send_file.flush()
    self.response = extract_json(self.recv.readline())
    return self.response.message
  
  def close(self):
    if self.send_file:
        self.send_file.close()
    if self.recv:
        self.recv.close()
    if self.sock:
        self.sock.close()