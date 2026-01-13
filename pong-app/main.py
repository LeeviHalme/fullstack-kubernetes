import os
from flask import Flask

app = Flask(__name__)

COUNTER = 0

@app.get("/pingpong")
def get_status():
    """Return 'pong' with an incrementing counter each time it's called."""
    # pylint: disable=global-statement
    global COUNTER
    COUNTER += 1

    return f"pong {COUNTER}"

@app.get("/pings")
def get_pings():
    """Return the number of pings received so far."""
    return { "pings": COUNTER }

if __name__ == "__main__":
    port = int(os.environ.get("PORT"))
    app.run(host='0.0.0.0', port=port)
