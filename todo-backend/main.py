import os
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

    if todo_name:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("INSERT INTO todos (name, done) VALUES (%s, %s);", (todo_name, False))

        conn.commit()
        cur.close()
        conn.close()

        # Redirect back to the frontend home page
        return redirect('/')

    return {'error': 'No todo provided'}, 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT'))
    print(f"Server started in port {port}")
    app.run(host='0.0.0.0', port=port)
