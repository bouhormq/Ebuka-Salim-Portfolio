import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import logging

load_dotenv()
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))


@app.route('/upload', methods=['POST'])
def upload_file():
    app.logger.info("Upload endpoint was hit")
    if 'profile_picture' not in request.files:
        app.logger.error("No 'profile_picture' in request.files")
        return jsonify({'error': 'No file part'}), 400
    file = request.files['profile_picture']
    if file.filename == '':
        app.logger.error("Filename is empty")
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = 'logo.jpg'
        upload_folder = os.path.join(app.static_folder, 'img')
        save_path = os.path.join(upload_folder, filename)
        app.logger.info(f"Attempting to save file to: {save_path}")
        try:
            file.save(save_path)
            app.logger.info(f"Successfully saved file to: {save_path}")
            response = jsonify({'success': 'File uploaded successfully'})
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response, 200
        except Exception as e:
            app.logger.error(f"Failed to save file: {e}")
            return jsonify({'error': str(e)}), 500
