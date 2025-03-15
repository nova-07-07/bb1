from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
TEXT_FOLDER = "txts"  # Folder containing text files
IMAGE_FOLDER = "I:/bible/static"  # Folder containing images

@app.route('/')
def list_files():
    files = [f for f in os.listdir(TEXT_FOLDER) if f.endswith(".txt")]
    return jsonify(files)

@app.route('/view')
def view_file():
    filename = request.args.get("file")
    if not filename or not filename.endswith(".txt"):
        return jsonify({"error": "Invalid file"}), 400
    file_path = os.path.join(TEXT_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return jsonify({"filename": filename, "content": content})

@app.route('/image/<filename>')
def get_image(filename):
    if not filename.lower().endswith((".png", ".jpeg")):
        return jsonify({"error": "Invalid file type"}), 400
    return send_from_directory(IMAGE_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
