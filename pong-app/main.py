from flask import Flask

app = Flask(__name__)

COUNTER = 0

@app.get("/pingpong")
def get_status():
    global COUNTER
    COUNTER += 1

    return f"pong {COUNTER}"

@app.get("/pings")
def get_pings():
    return { "pings": COUNTER }

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5500)
