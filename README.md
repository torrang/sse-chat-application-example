# SSE(Server-Sent Events) Chat Application Example

## 

### 1. What is this project?

This project is a simple chat application example of how to use SSE with Flask.

Rooms are stored in memory but chat logs aren't stored on anywhere.

### 2. How to run this project?

1. Clone this repository
2. Install the dependencies
3. Run the server with `python app.py`
4. Open the browser and navigate to `http://localhost:5000/`

### 3. How it works?

1. When you join the chat, the server will send a message to the client.
2. When you send a message, the server will broadcast the message to all connected clients.
3. When you leave the chat, the server will remove the client from the list of connected clients.
