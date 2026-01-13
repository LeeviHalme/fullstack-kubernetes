import os
import psycopg2
from flask import Flask

app = Flask(__name__)

COUNTER = 0
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    return psycopg2.connect(DATABASE_URL)

def init_db():
    """Initialize the database and create the counter table if it doesn't exist."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS counter (id INT PRIMARY KEY, count INT);")
    cur.execute("INSERT INTO counter (id, count) VALUES (1, 0) ON CONFLICT (id) DO NOTHING;")

    conn.commit()
    cur.close()
    conn.close()

@app.get("/pingpong")
def get_status():
    """Return 'pong' with an incrementing counter each time it's called."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("UPDATE counter SET count = count + 1 WHERE id = 1 RETURNING count;")
    new_count = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return f"pong {new_count}"

@app.get("/pings")
def get_pings():
    """Return the number of pings received so far."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT count FROM counter WHERE id = 1;")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return { "pings": count }

# Initialize the database when the application starts
init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT"))
    app.run(host='0.0.0.0', port=port)
