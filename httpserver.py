from flask import Flask, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploaded_frames"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload/<username>/<cam_index>', methods=['POST'])
def upload_frame(username, cam_index):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Ensure the directory exists
    user_dir = os.path.join(app.config['UPLOAD_FOLDER'], username, cam_index)
    os.makedirs(user_dir, exist_ok=True)

    # Save the uploaded file
    file_path = os.path.join(user_dir, 'latest.jpg')
    file.save(file_path)
    return jsonify({"message": "Frame uploaded successfully!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)