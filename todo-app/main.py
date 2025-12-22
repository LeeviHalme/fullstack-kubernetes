import os
import requests
import time
from flask import Flask, render_template

app = Flask(__name__, static_folder="static")

def refetch_image():
    # Get image from Picsum and save it to static folder as hourly_image.png
    img_url = 'https://picsum.photos/1200'
    response = requests.get(img_url)

    if response.status_code == 200:
        img_path = os.path.join(app.static_folder, 'hourly_image.png')
        with open(img_path, 'wb') as f:
            f.write(response.content)

@app.get('/')
def index():
    hardcoded_todos = ["Learn Kubernetes", "Learn Flask", "Build awesome apps"]
    return render_template('index.html', todos=hardcoded_todos)

@app.get('/get-img')
def get_img():
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
