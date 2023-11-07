import json
import os

from bson import json_util
from flask import Flask, request
from flask_httpauth import HTTPTokenAuth


def create_app(db_client):
    app = Flask(__name__)
    auth = HTTPTokenAuth(header="X-API-Key")

    tokens = {
        os.environ.get("TRACKER_MAIN_API_KEY"): "main",
    }

    @auth.verify_token
    def verify_token(token):
        if token in tokens:
            return tokens[token]

    @app.route('/devices/')
    @auth.login_required
    def display_device_ids():
        device_ids = db_client.get_all_device_ids()
        return device_ids

    # Route for retrieving messages in JSON format for a specific device
    @app.route('/devices/<device_id>/')
    @auth.login_required
    def get_messages_json(device_id):
        page_num = int(request.args.get('page', 1))
        page_size = 10
        messages = db_client.get_messages(device_id, page_num, page_size)
        return json.loads(json_util.dumps(messages))

    return app
