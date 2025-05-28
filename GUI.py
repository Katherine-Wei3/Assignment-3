import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Text
import ds_messenger
from pathlib import Path
import json
from notebook import Notebook

class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
        """Initialize the Body frame with a treeview for contacts and text editors."""
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()
        # self.body.entry_editor.delete('1.0', tk.END)

    def node_select(self, event):
        """Handle selection of a contact in the treeview."""
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        """Insert a contact into the contact list and treeview."""
        # print(self._contacts) debug 
        if contact not in self._contacts:
            self._contacts.append(contact)
            id = len(self._contacts) - 1
            self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        """Insert a contact into the treeview."""
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message:str):
        """Insert a user message into the entry editor."""
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message:str):
        """Insert a contact message into the entry editor."""
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        """Get the text from the message editor."""
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
        """Set the text in the message editor."""

        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        """Draw the main body of the application with contacts and message editors."""
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)
        
        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """Footer frame for the Direct Messenger GUI, containing buttons and status labels."""
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        """Handle the click event for the send button."""
        if self._send_callback is not None:
            self._send_callback()

    def _add_contact_callback(self):
        """Handle the click event for the add contact button."""
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        """Draw the footer with buttons and status labels."""
        save_button = tk.Button(master=self, text="Send", width=20, command=self.send_click)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        # self.add_contact_button = tk.Button(self, text="Add Contact", width=20, command=self._add_contact_callback)
        # self.add_contact_button.pack(fill=tk.X, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root: tk.Tk, title: str = None, user: str = None, pwd: str = None, server: str = None):
        """Initialize the dialog for configuring the Direct Messenger server and user credentials."""
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame: tk.Frame):
        """Create the body of the dialog with entry fields for server, username, and password."""
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        # You need to implement also the region for the user to enter
        # the Password. The code is similar to the Username you see above
        # but you will want to add self.password_entry['show'] = '*'
        # such that when the user types, the only thing that appears are
        # * symbols.
        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry['show'] = '*'
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

    def apply(self):
        """Apply the changes made in the dialog."""
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    """Main application frame for the direct messenger GUI."""
    def __init__(self, root):
        """Initialize the main application, configure server, and set up GUI widgets."""
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = ''
        self.password = ''
        self.server = ''
        self.recipient = ''
        # You must implement this! You must configure and
        # instantiate your DirectMessenger instance after this line.
        self.direct_messenger = ds_messenger.DirectMessenger(self.server, self.username, self.password)

        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        self.configure_server()
        self.root.after(2000, self.check_new)

    def send_message(self):
        """Send a message to the recipient."""
        # You must implement this!
        msg = self.body.get_text_entry()
        try:
            self.direct_messenger.send(msg, self.recipient)
        except ConnectionError as e:
            messagebox.showerror("Connection Error", str(e))

    def add_contact(self):
        """Add a new contact to the contact list."""
        # You must implement this!
        # Hint: check how to use tk.simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list
        new_contact = tk.simpledialog.askstring("Add Contact", "Enter contact name:")
        if new_contact:
            self.body.insert_contact(new_contact)
            self.recipient = new_contact
        self.direct_messenger.nb.add_contact_and_message(self.direct_messenger.notebook_path, new_contact)

    def recipient_selected(self, recipient: str):
        """Set the current recipient when a contact is selected.

        Args:
            recipient (str): The selected contact's username.
        """
        self.recipient = recipient
        # FIXME
        self.body.entry_editor.delete('1.0', tk.END)
        # Get messages for this contact from the notebook
        messages = self.direct_messenger.nb.chats.get(recipient, [])
        for msg in messages:
            self.body.insert_contact_message(msg)

    def configure_server(self):
        """Configure the Direct Messenger server, username, password."""
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        # You must implement this!
        # You must configure and instantiate your
        # DirectMessenger instance after this line.
        self.direct_messenger = ds_messenger.DirectMessenger(self.server, self.username, self.password)
        print(self.direct_messenger.nb.contacts)
        for contact in self.direct_messenger.nb.contacts:
            self.body.insert_contact(contact)

    def _publish(self, msg: list):
        """Publish a new message to the contact list and entry editor.
        Args:
            msg (list): A list of DirectMessage objects to be published.
        """
        # You must implement this!
        sender = getattr(msg, 'from_name', None)
        # print(f'sender: {sender}') DEBUG
        if sender and sender not in self.body._contacts:
            self.body.insert_contact(sender)
            if self.recipient == sender:
                self.body.insert_contact_message(msg)
        for m in msg:
            self.body.insert_contact_message(m.message)
        self.direct_messenger.nb.add_contact_and_message(self.direct_messenger.notebook_path, self.recipient, m.message)

    def check_new(self):
        """Check for new messages from the server and publish them."""
        # You must implement this!
        try:
            new_msg = self.direct_messenger.retrieve_new()
            for msg in new_msg:
                if msg.from_name not in self.body._contacts:
                    self.body.insert_contact(msg.from_name)
                    self.direct_messenger.nb.add_contact_and_message(self.direct_messenger.notebook_path, msg.from_name, msg.message)
            if new_msg:
                self._publish(new_msg)
            self.root.after(2000, self.check_new)
        except ConnectionError as e:
            messagebox.showerror("Connection Error", str(e))

    def _draw(self):
        """Draw the main application GUI components."""
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New')
        menu_file.add_command(label='Open...')
        menu_file.add_command(label='Close')

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

