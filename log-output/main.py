import os
from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.get("/get-log")
def get_status():
    """
    Get log content, pong count, information content, and environment message.
    """
    try:
        information_file_path = os.getenv("INFORMATION_FILE_PATH")
        output_file_path = os.getenv("OUTPUT_FILE_PATH")
        pong_api_endpoint = os.getenv("PONG_API_ENDPOINT")

        # get environment variable MESSAGE
        message_content = os.getenv("MESSAGE", None)

        with open(output_file_path, "r") as file:
            log_content = file.read()

        with open(information_file_path, "r") as file:
            information_content = file.read()

        # get pong count from pong-app HTTP endpoint
        response = requests.get(pong_api_endpoint, timeout=5)
        if response.status_code != 200:
            return jsonify({"error": "Failed to retrieve pong count"}), 500

        pong_content = response.json().get("pings", "N/A")

        return jsonify({
            "log": log_content, 
            "pong": pong_content, 
            "information": information_content, 
            "env": message_content
        }), 200

    except FileNotFoundError:
        return jsonify({"error": "Log file was not found"}), 404

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host='0.0.0.0', port=port)
