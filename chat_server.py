import sys
import json
import logging
from typing import Optional
from logging.config import dictConfig

import redis
import flask
from flask import request, Response, jsonify, render_template

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
        
        for message in pubsub.listen():
            if message.get('data') == 1:
                continue

            logger.debug(f"channel message={message['data']}")
            yield f"data: {message['data'].decode('utf8')}\n\n"


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

    redis_client.publish(redis_channel, json.dumps(request.json))

    return jsonify({"result": True})


if __name__ == '__main__':
    # Set logger
    configure_logger()

    # Connect to redis
    redis_client = redis.Redis()

    # Run chat server
    app.run(host='0.0.0.0', debug=True)

