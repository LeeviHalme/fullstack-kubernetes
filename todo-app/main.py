import os
import time
import requests
from flask import Flask, render_template

app = Flask(__name__, static_folder="static")

def refetch_image():
    """
    Fetches a new image from Picsum and saves it to the static folder.
    """
    img_url = 'https://picsum.photos/1200'
    response = requests.get(img_url, timeout=10)

    if response.status_code == 200:
        img_path = os.path.join(app.static_folder, 'hourly_image.png')
        with open(img_path, 'wb') as f:
            f.write(response.content)

@app.get('/')
def index():
    """
    Fetch todos from the backend and render them in the template.
    """
    response = requests.get('http://todo-backend-svc:8000/api/todos', timeout=5)
    todos = response.json().get('todos', [])

    return render_template('index.html', todos=todos)

@app.get('/get-img')
def get_img():
    """
    Serves an image that is refreshed every 10 minutes.
    """
    # Get local file from static folder and check when it was last modified
    img_path = os.path.join(app.static_folder, 'hourly_image.png')

    if not os.path.exists(img_path):
        refetch_image()

    # Check if the image is older than 10 minutes (600 seconds)
    last_modified_time = os.path.getmtime(img_path)
    current_time = time.time()
    if current_time - last_modified_time > 600:
        refetch_image()

    return app.send_static_file('hourly_image.png')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    print(f"Server started in port {port}")
    app.run(host='0.0.0.0', port=port)
