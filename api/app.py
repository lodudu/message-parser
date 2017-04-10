import logging

from flask import Flask
from flask import jsonify
from flask import request

from message import Message

app = Flask(__name__)

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


@app.route("/parsed_message")
def hello():
    message = request.args.get('message', '')
    msg = Message(message)

    result = {}
    mentions = msg.mentions
    emoticons = msg.emoticons
    links = msg.links
    if mentions is not None and len(mentions) > 0:
        result['mentions'] = mentions
    if emoticons is not None and len(emoticons) > 0:
        result['emoticons'] = emoticons
    if links is not None and len(links) > 0:
        result['links'] = links

    return jsonify(result), 200


if __name__ == "__main__":
    app.run()
