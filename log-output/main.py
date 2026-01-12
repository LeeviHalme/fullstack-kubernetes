from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.get("/get-log")
def get_status():
    try:
        with open("files/output.txt", "r") as file:
            log_content = file.read()

        # get pong count from pong-app HTTP endpoint
        response = requests.get("http://pong-app-svc:5500/pings", timeout=5)
        if response.status_code != 200:
            return jsonify({"error": "Failed to retrieve pong count"}), 500

        pong_content = response.json().get("pings", "N/A")

        return jsonify({"log": log_content, "pong": pong_content}), 200

    except FileNotFoundError:
        return jsonify({"error": "Log file was not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
