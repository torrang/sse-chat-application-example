import time
import json
import queue
import logging
from typing import Dict

import flask
from flask import request, Response, jsonify, render_template

from chat_models import Room, User

app = flask.Flask(__name__)
logger = logging.getLogger(__name__)

# Global variables
rooms: Dict[int, Room] = {}
chat_stream_queue: queue.Queue = queue.Queue(maxsize=100)


def stream_queue():
    with app.app_context():
        while True:
            try:
                chat = chat_stream_queue.get(timeout=1)
            except queue.Empty:
                yield f""
                time.sleep(1)
            else:
                yield f"data: {json.dumps(chat)}\n\n"


# Chat application main page
@app.route('/')
def web_index():
    return render_template('chat/index.html')


@app.route('/api/v1/stream', methods=['GET'])
def api_chat_stream():
    return Response(stream_queue(), content_type="text/event-stream")


@app.route('/api/v1/message', methods=['POST'])
def api_send_chat():
    logger.info(f"user sent message, message={request.json}")

    chat_stream_queue.put(request.json)

    return jsonify({"result": True})


if __name__ == '__main__':
    app.run(debug=True)

