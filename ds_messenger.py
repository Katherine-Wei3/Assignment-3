# ds_messenger.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Katherine Wei
# yininw17@uci.edu
# 14645993

from ds_protocol import extract_json, auth_request, direct_message_request, fetch
import socket

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
    self._connect()
  
  def _connect(self, host: int, port: int) -> None:
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.host = host
    self.port = port
    self.sock.connect((self.host, self.port))
    self.send = self.sock.makefile('w')
    self.recv = self.sock.makefile('r')
    	
    join_msg = auth_request(self.username, self.password)
    self.send.write(join_msg)
    self.send.flush()
    self.response = self.receive()
    if self.response.type ==
  
  def send(self, message:str, recipient:str) -> bool:
    # must return true if message successfully sent, false if send failed.
    try:
      
      return True
    except:
      return False
      
  def retrieve_new(self) -> list:
    # must return a list of DirectMessage objects containing all new messages
    pass
 
  def retrieve_all(self) -> list:
    # must return a list of DirectMessage objects containing all messages
    pass