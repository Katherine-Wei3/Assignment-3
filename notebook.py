# ICS 32
# Assignment #1: Diary
#
# Author: Aaron Imani
#
# v0.1.0

# You should review this code to identify what features you need to support
# in your program for assignment 1.
#
# YOU DO NOT NEED TO READ OR UNDERSTAND THE JSON SERIALIZATION ASPECTS OF THIS CODE
# RIGHT NOW, though can you certainly take a look at it if you are curious since we
# already covered a bit of the JSON format in class.

"""Notebook and Diary classes for ICS 32 Assignment.
Handles diary entries, contacts, chats, and file operations for user notebooks.
"""

import json
import time as time_module
from pathlib import Path


class NotebookFileError(Exception):
    """
    Raised when attempting to load or save Notebook objects to the file system.
    """
    # pass


class IncorrectNotebookError(Exception):
    """
    Raised when attempting to deserialize a notebook file to a Notebook object.
    """
    # pass


class Diary(dict):
    """
    The Diary class is responsible for working with individual user diaries.
    Supports a timestamp property and an entry property.
    """

    def __init__(self, entry: str = None, timestamp: float = 0):
        """Initialize a Diary object."""
        self._timestamp = timestamp
        self.set_entry(entry)
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry):
        """Set the diary entry and update the dictionary."""
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)
        if self._timestamp == 0:
            self._timestamp = time_module.time()

    def get_entry(self):
        """Get the diary entry."""
        return self._entry

    def set_time(self, timestamp: float):
        """Set the diary timestamp."""
        self._timestamp = timestamp
        dict.__setitem__(self, 'timestamp', timestamp)

    def get_time(self):
        """Get the diary timestamp."""
        return self._timestamp

    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Notebook:
    """Notebook is a class that can be used to manage a diary notebook."""

    def __init__(self, username: str, password: str, bio: str):
        """Creates a new Notebook object."""
        self.username = username
        self.password = password
        self.bio = bio
        self._diaries = []
        self.contacts = []
        self.chats = {}

    def add_diary(self, diary: Diary) -> None:
        """Append a Diary object to the diary list."""
        self._diaries.append(diary)

    def del_diary(self, index: int) -> bool:
        """
        Removes a Diary at a given index and returns `True` if successful and `False` if an index is invalid.
        """
        try:
            del self._diaries[index]
            return True
        except IndexError:
            return False

    def get_diaries(self) -> list[Diary]:
        """Returns the list object containing all diaries that 
        have been added to the Notebook object."""
        return self._diaries

    def save(self, path: str) -> None:
        """
        Save the current instance of Notebook to the file system.
        Raises NotebookFileError, IncorrectNotebookError.
        """
        file_path = Path(path)
        if file_path.suffix == '.json':
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(self.__dict__, file, indent=4)
            except Exception as ex:
                raise NotebookFileError(
                    "Error while attempting to process the notebook file.", ex
                ) from ex
        else:
            raise NotebookFileError("Invalid notebook file path or type")

    def load(self, path: str) -> None:
        """
        Populate the current instance of Notebook with data stored in a notebook file.
        Raises NotebookFileError, IncorrectNotebookError.
        """
        file_path = Path(path)
        if file_path.exists() and file_path.suffix == '.json':
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    obj = json.load(file)
                    self.username = obj['username']
                    self.password = obj['password']
                    self.bio = obj['bio']
                    for diary_obj in obj['_diaries']:
                        diary = Diary(diary_obj['entry'], diary_obj['timestamp'])
                        self._diaries.append(diary)
                    self.contacts = obj.get('contacts', [])
                    self.chats = obj.get('chats', {})
            except Exception as ex:
                raise IncorrectNotebookError(ex) from ex
        else:
            raise NotebookFileError()
        self.chats = obj.get('chats', {})

    def add_contact_and_message(
            self,
            path: str,
            contact: str,
            message: str = None) -> None:
        """
        Add a message to the chat history with a contact.
        Args:
            contact (str): The contact's username.
            message (str): The message text.
        """
        if contact and contact not in self.contacts:
            self.contacts.append(contact)
        if contact and contact not in self.chats:
            self.chats[contact] = []
        if contact and message:
            self.chats[contact].append(message)
        self.save(path)

    def load_local_contacts_and_chats(self, username, password) -> dict:
        """
        Get all chat history for the given username and password.
        Returns:
            dict: A dictionary containing all chat histories.
        Raises:
            PermissionError: If username or password is incorrect.
        """
        if username == self.username and password == self.password:
            return self.chats
        raise PermissionError("Incorrect username or password for local notebook.")
    