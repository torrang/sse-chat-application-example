import json
import logging
from typing import Optional
from datetime import datetime
from logging.config import dictConfig

import redis
import redis.exceptions
import flask
from flask import request, Response, jsonify, render_template

from model import Message

# Global variables
redis_channel = "sse-chat"
redis_client: Optional[redis.Redis] = None
app = flask.Flask(__name__)
logger = logging.getLogger()


def configure_logger():
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'DEBUG',
            'handlers': ['wsgi']
        }
    })


def stream_queue():
    with app.app_context():
        pubsub = redis_client.pubsub()
        pubsub.subscribe(redis_channel)
        
        for data in pubsub.listen():
            if data.get('data') == 1:
                continue

            logger.debug(f"channel data={data['data']}")
            message = Message(**json.loads(data['data']))

            # Event handler
            if message.message_type == "join":
                yield f"event: new_user\n"
                yield f"data: {data['data'].decode('utf8')}\n\n"
            elif message.message_type == "chat":
                yield f"event: new_chat\n"
                yield f"data: {data['data'].decode('utf8')}\n\n"
            else:
                yield f"data: {data['data'].decode('utf8')}\n\n"


# Chat application main page
@app.route('/')
def web_index():
    return render_template('chat/index.html')


@app.route('/api/v1/stream', methods=['GET'])
def api_chat_stream():
    # Send new user event
    message = Message(
        sender="server",
        message=f"{request.remote_addr} joined the server.",
        message_type="join",
        timestamp=datetime.now().timestamp()
    )

    redis_client.publish(redis_channel, json.dumps(message.to_dict()))

    return Response(stream_queue(), content_type="text/event-stream")


@app.route('/api/v1/message', methods=['POST'])
def api_send_chat():
    response = {}
    data = request.json
    data['message_type'] = "chat"
    data['timestamp'] = datetime.now().timestamp()
    message = Message(**data)

    logger.info(f"user sent message, message={message}")

    try:
        redis_client.publish(redis_channel, json.dumps(message.to_dict()))
    except redis.exceptions.ConnectionError as e:
        response = {"result": False, "message": "server is busy"}

    response = {"result": True, "message": None}

    return jsonify(response)


if __name__ == '__main__':
    # Set logger
    configure_logger()

    # Connect to redis
    redis_client = redis.Redis()

    # Run chat server
    app.run(host='0.0.0.0', debug=True)

