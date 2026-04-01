#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import json
from datetime import datetime
import sys
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'

app = Flask(__name__)

@app.route('/webhook/whatsapp', methods=['POST', 'GET'])
def whatsapp_webhook():
    """Receive WhatsApp DLR and message callbacks from Infobip"""
    try:
        data = request.get_json() if request.is_json else request.args.to_dict()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{'='*80}")
        print(f"[{timestamp}] WEBHOOK RECEIVED")
        print(f"{'='*80}")
        print(json.dumps(data, indent=2))
        print(f"{'='*80}\n")
        sys.stdout.flush()

        return jsonify({"status": "received"}), 200
    except Exception as e:
        print(f"Error processing webhook: {e}")
        sys.stdout.flush()
        return jsonify({"error": str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()}), 200

if __name__ == '__main__':
    print("\nWhatsApp Webhook Server Starting...")
    print("Listening on http://localhost:9091/webhook/whatsapp")
    print("Press Ctrl+C to stop\n")
    sys.stdout.flush()
    app.run(host='0.0.0.0', port=9091, debug=False)
