# ds_protocol.py

# Starter code for assignment 2 in ICS 32 Programming with Software
# Libraries in Python

# Replace the following placeholders with your information.

# Katherine Wei
# yininw17@uci.edu
# 14645993

"""Protocol utilities for Direct Messenger.
Defines protocol message formats, parsing, and helpers for server communication.
"""

import json
from collections import namedtuple

# Create a namedtuple to hold the values we expect to retrieve from json messages.
ServerResponse = namedtuple('ServerResponse', ['type', 'message', 'token'])
MessageReceived = namedtuple(
    'MessageReceived', [
        'message', 'from_name', 'timestamp', 'status'])
MessageSent = namedtuple(
    'MessageSent', [
        'message', 'recipient', 'timestamp', 'status'])


class DSPError(Exception):
    '''
    An exception to be used when received commands do not follow protocol specifications
    '''
    # pass


def extract_json(json_msg: str) -> ServerResponse:
    '''
    Call the json.loads function on a json response and convert it to a DataTuple object
    '''
    try:
        json_obj = json.loads(json_msg)
        if 'response' in json_obj:
            resp_type = json_obj['response']['type']
            if 'message' in json_obj['response']:
                message = json_obj['response']['message']
            elif 'messages' in json_obj['response']:
                message = json_obj['response']['messages']
                received = _extract_messages_received(json_obj)
                sent = _extract_messages_sent(json_obj)
                # print(f"Received: {received}, Sent: {sent}")
                message = received + sent
            else:
                message = None
            # some replies may not have a token
            token = json_obj['response'].get('token')
            return ServerResponse(resp_type, message, token)
        return None
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return None
    except Exception as exc:
        raise DSPError from exc


def auth_request(username: str, password: str) -> str:
    '''
    This function takes a username and password and returns a json string sent to the server
    '''
    auth = {
        "authenticate": {
            "username": username,
            "password": password
        }
    }
    return json.dumps(auth)


def direct_message_request(
        token: str,
        recipient: str,
        message: str,
        timestamp: float) -> str:
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


def fetch_request(token: str, what: str) -> str:
    '''
    This function takes a token and fetch (all / unread) and returns a json string to the server
    '''
    fetch_obj = {
        "token": token,
        "fetch": what
    }
    return json.dumps(fetch_obj)


def _extract_messages_received(json_obj: dict) -> list[MessageReceived]:
    '''
    This function takes json messages and returns a list of MessageReceived objects
    '''
    messages = []
    messages_data = json_obj['response']['messages']
    for msg in messages_data:
        if 'from' in msg:
            messages.append(
                MessageReceived(
                    msg['message'],
                    msg['from'],
                    msg['timestamp'],
                    msg.get('status')
                )
            )
    return messages


def _extract_messages_sent(json_obj: dict) -> list[MessageSent]:
    '''
    This function takes json messages and returns a list of MessageSent objects
    '''
    messages = []
    messages_data = json_obj['response']['messages']
    for msg in messages_data:
        if 'recipient' in msg:
            messages.append(
                MessageSent(
                    msg['message'],
                    msg['recipient'],
                    msg['timestamp'],
                    msg.get('status')
                )
            )
    return messages
