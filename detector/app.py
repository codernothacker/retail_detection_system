from flask import Flask, request, jsonify
from detection import ProductDetector
import os
import traceback
from config import DetectorConfig
from utils import prepare_image, convert_detections
from utils.error_handlers import handle_errors

app = Flask(__name__)
detector = None

@app.before_first_request
def initialize():
    global detector
    detector = ProductDetector()

@app.route('/detect', methods=['POST'])
@handle_errors
def detect():
    try:
        if 'image_path' not in request.json:
            return jsonify({'error': 'No image path provided'}), 400
            
        image_path = request.json['image_path']
        if not os.path.exists(image_path):
            return jsonify({'error': f'Image not found at path: {image_path}'}), 404
            
        global detector
        if detector is None:
            detector = ProductDetector()
            
        detections = detector.detect(image_path)
        
        return jsonify({
            'status': 'success',
            'detections': detections,
            'count': len(detections)
        })
        
    except Exception as e:
        print(f"Error in detect endpoint: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)