import os
from flask import Flask, render_template

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    print(f"Server started in port {port}")
    app.run(host='0.0.0.0', port=port)
