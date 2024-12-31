import os
import hashlib
from typing import Dict

import flask
from flask import render_template

from models import Room, User

app = flask.Flask(__name__)

# Global variables
rooms: Dict[int, Room] = {}

# Chat application main page
@app.route('/')
def web_index():
    return render_template('index.html')

# Chat application chat page
@app.route('/')
def web_chat_page():
    return "Hello, World!"

# Get the list of members in the chat
@app.route('/api/v1/chat/members', methods=['GET'])
def api_chat_members():
    pass

# Join the chat
@app.route('/api/v1/chat/join', methods=['POST'])
def api_chat_join():
    pass

# Leave the chat
@app.route('/api/v1/chat/leave', methods=['POST'])
def api_chat_leave():
    pass

# Send a message to the chat
@app.route('/api/v1/chat/message', methods=['POST'])
def api_chat_message():
    pass

if __name__ == '__main__':
    app.run(debug=True)

