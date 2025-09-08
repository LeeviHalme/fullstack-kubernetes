import time
import random
import string
import threading
from datetime import datetime
from flask import Flask, jsonify

app = Flask(__name__)

RANDOM_STRING = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
LATEST_LOG_ENTRY = None

@app.get("/status")
def get_status():
    return jsonify({"latest_log_entry": LATEST_LOG_ENTRY})

def log_loop():
    """
    This function will run in a separate thread and continuously
    update the global log entry.
    """
    global LATEST_LOG_ENTRY
    while True:
        timestamp = datetime.isoformat(datetime.now())
        LATEST_LOG_ENTRY = f"{timestamp}: {RANDOM_STRING}"
        print(LATEST_LOG_ENTRY)
        time.sleep(5)

def start_log_loop():
    """
    Start the logging loop in a background thread.
    daemon=True ensures the thread exits when the main program does.
    """
    logging_thread = threading.Thread(target=log_loop, daemon=True)
    logging_thread.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
