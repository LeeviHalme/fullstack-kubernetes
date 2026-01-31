import os
from flask import Flask, jsonify
import requests

app = Flask(__name__)

pong_api_endpoint = os.getenv("PONG_API_ENDPOINT")
greeter_api_endpoint = os.getenv("GREETER_API_ENDPOINT")

# this is a comment to trigger the gh workflow

@app.get("/log/healthz")
def health_check():
    """Health check endpoint to verify pong-app connectivity."""
    try:
        # Try to reach the Ping-pong service internally
        response = requests.get(pong_api_endpoint, timeout=2)
        if response.status_code == 200:
            return "OK", 200

        return "pong-app not ready", 500
    except Exception: # pylint: disable=broad-except
        return "pong-app unreachable", 500

@app.get("/get-log")
def get_status():
    """
    Get log content, pong count, information content, and environment message.
    """
    try:
        information_file_path = os.getenv("INFORMATION_FILE_PATH")
        output_file_path = os.getenv("OUTPUT_FILE_PATH")

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

        greeter_response = requests.get(greeter_api_endpoint, timeout=5)
        if greeter_response.status_code != 200:
            return jsonify({"error": "Failed to retrieve greeter message"}), 500
        
        greeter_message = greeter_response.text.strip()

        return jsonify({
            "log": log_content, 
            "pong": pong_content, 
            "information": information_content,
            "greeter": greeter_message,
            "env": message_content
        }), 200

    except FileNotFoundError:
        return jsonify({"error": "Log file was not found"}), 404

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host='0.0.0.0', port=port)
