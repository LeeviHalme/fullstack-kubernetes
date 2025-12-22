from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/get-log")
def get_status():
    try:
        with open("files/output.txt", "r") as file:
            log_content = file.read()

        with open("files/pong.txt", "r") as file:
            pong_content = file.read()

        return jsonify({"log": log_content, "pong": pong_content}), 200

    except FileNotFoundError:
        return jsonify({"error": "Log file was not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
