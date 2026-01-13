import os
from flask import Flask, request, redirect

app = Flask(__name__)

todo_list = []

@app.get('/api/todos')
def get_todos():
    """
    Gets the list of todos from memory.
    """

    return {'todos': todo_list}

@app.post('/api/todos')
def add_todo():
    """
    Adds a new todo from a standard HTML form.
    """
    # Use request.form to get data from HTML <input name="name" />
    todo_name = request.form.get('name')

    if todo_name:
        # Creating the object structure
        new_todo = {
            "name": todo_name,
            "done": False
        }
        todo_list.append(new_todo)

        # Redirect back to the frontend home page
        return redirect('/')

    return {'error': 'No todo provided'}, 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT'))
    print(f"Server started in port {port}")
    app.run(host='0.0.0.0', port=port)
