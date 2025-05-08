from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    image_dir = "static/images"
    images = [f"/{image_dir}/{img}" for img in os.listdir(image_dir) if img.endswith(('.png', '.jpg', '.jpeg'))]
    return render_template('index.html', images=images)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=60002, debug=False)
