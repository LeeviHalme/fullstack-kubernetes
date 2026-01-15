import os
import sys
import psycopg2
from flask import Flask, request, redirect

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    return psycopg2.connect(DATABASE_URL)

def init_db():
    """Initialize the database and create the todo table if it doesn't exist."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS todos ( \
                  id SERIAL PRIMARY KEY, \
                  name TEXT NOT NULL, \
                  done BOOLEAN NOT NULL DEFAULT FALSE \
                );")

    conn.commit()
    cur.close()
    conn.close()

# Initialize DB at the top level for Gunicorn
init_db()

@app.before_request
def log_request_info():
    """Log incoming requests."""
    print(f"--> {request.method} {request.path}", file=sys.stderr)

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT 1;") # Simple query to test connection

        cur.close()
        conn.close()

        return {"status": "OK"}, 200
    except Exception: # pylint: disable=broad-except
        return {"error": "Database not reachable"}, 500

@app.get('/api/todos')
def get_todos():
    """
    Gets the list of todos from db.
    """

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name, done FROM todos;")
    todos = [{"id": row[0], "name": row[1], "done": row[2]} for row in cur.fetchall()]

    cur.close()
    conn.close()

    return { "todos": todos }, 200

@app.post('/api/todos')
def add_todo():
    """
    Adds a new todo from a standard HTML form.
    """
    # Use request.form to get data from HTML <input name="name" />
    todo_name = request.form.get('name')

    if not todo_name:
        print("ERROR: No todo provided", file=sys.stderr)
        return {'error': 'No todo provided'}, 400

    if len(todo_name) > 140:
        print(f"ERROR: Todo is too long: {todo_name}", file=sys.stderr)
        return {'error': 'Todo is too long'}, 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO todos (name, done) VALUES (%s, %s);", (todo_name, False))

    conn.commit()
    cur.close()
    conn.close()

    print(f"Added todo: {todo_name}", file=sys.stderr)

    # Redirect back to the frontend home page
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT'))
    print(f"Server started in port {port}")
    app.run(host='0.0.0.0', port=port)
