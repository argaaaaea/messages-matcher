#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime

from flask import Flask, jsonify, request

os.environ["PYTHONIOENCODING"] = "utf-8"

app = Flask(__name__)

TARGET_MESSAGE = "Mine"


@app.route("/matcher", methods=["POST"])
@app.route("/webhook", methods=["POST"])
def receive_message():
    payload = request.get_json(silent=True) or {}
    message = payload.get("message")
    destination = payload.get("destination")

    if not message:
        return jsonify({"error": "message is required"}), 400

    if not destination:
        return jsonify({"error": "destination is required"}), 400

    if message == TARGET_MESSAGE:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] matched payload: message={message}, destination={destination}")
        sys.stdout.flush()
        return jsonify({"message": "is processed", "destination": destination}), 200

    return jsonify({"message": "not processed"}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print("Simple webhook server starting...")
    print(f"Listening on http://0.0.0.0:{port}/matcher")
    sys.stdout.flush()
    app.run(host="0.0.0.0", port=port, debug=False)
