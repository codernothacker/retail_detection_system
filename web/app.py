from flask import Flask, request, render_template, jsonify, redirect, url_for
import os
import requests
import uuid
from PIL import Image
import logging
from config import Config
from utils import setup_logger, allowed_file
from utils.error_handlers import handle_errors

app = Flask(__name__)
app.config.from_object(Config)
logger = setup_logger(__name__)
logging.basicConfig(level=logging.DEBUG)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
DETECTION_SERVICE_URL = os.getenv('DETECTION_SERVICE_URL', 'http://detector:5001')
GROUPING_SERVICE_URL = os.getenv('GROUPING_SERVICE_URL', 'http://grouping:5002')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
@handle_errors
def upload_file():
    try:
        app.logger.info("Starting file upload process")
        if 'image' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
            filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            app.logger.info(f"File saved to: {filepath}")
            container_filepath = os.path.join('/app/images', filename)
            
            try:
                detection_response = requests.post(
                    f'{DETECTION_SERVICE_URL}/detect',
                    json={'image_path': container_filepath},
                    timeout=30
                )
                detection_response.raise_for_status()
                detections = detection_response.json().get('detections', [])
                grouping_response = requests.post(
                    f'{GROUPING_SERVICE_URL}/group',
                    json={
                        'detections': detections,
                        'image_path': container_filepath
                    },
                    timeout=30
                )
                grouping_response.raise_for_status()

                result = {
                    'message': 'Processing completed successfully',
                    'original_image': f'/static/uploads/{filename}',
                    'detected_image': f'/static/uploads/detected_{filename}',
                    'detections': grouping_response.json().get('grouped_detections', [])
                }
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify(result)
                return render_template('result.html', result=result)
                
            except requests.exceptions.RequestException as e:
                app.logger.error(f"Service error: {str(e)}")
                return jsonify({'error': f'Service error: {str(e)}'}), 500
        
        return jsonify({'error': 'Invalid file type'}), 400
        
    except Exception as e:
        app.logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
