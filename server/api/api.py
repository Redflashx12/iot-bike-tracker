import json
import os
from datetime import datetime

from bson import json_util
from flask import Flask, request, jsonify, make_response
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

    @app.route('/devices/<device_id>/')
    @auth.login_required
    def get_messages_json(device_id):
        try:
            page_num = int(request.args.get('page', 1))
            if page_num < 1:
                raise ValueError("Page number must be a positive integer")
        except ValueError:
            return jsonify({"error": "Invalid page number"}), 400
        from_dt = request.args.get('from', datetime.min.isoformat())
        to_dt = request.args.get('to', datetime.max.isoformat())
        page_size = 20
        
        messages, total_messages = db_client.get_messages_of_device(device_id, page_num, page_size,
                                                                    from_dt, to_dt)
        total_pages = (total_messages + page_size - 1) // page_size
        if page_num > total_pages:
            return jsonify({"error": "Page not found"}), 404

        response = make_response(json.loads(json_util.dumps(messages)))
        response.headers['X-Page'] = page_num
        response.headers['X-Total-Pages'] = total_pages
        response.headers['X-Total-Messages'] = total_messages
        return response

    return app
