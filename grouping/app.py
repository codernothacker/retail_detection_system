from flask import Flask, request, jsonify
from grouping import ProductGrouper
import cv2
import os
import traceback
import logging
from utils.error_handlers import handle_errors
from config import GroupingConfig
from utils import setup_logger, extract_roi_features, draw_group_visualization

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
grouper = ProductGrouper()

@app.route('/group', methods=['POST'])
@handle_errors
def group():
    try:
        logger.info("Received grouping request")
        
        if 'detections' not in request.json or 'image_path' not in request.json:
            logger.error("Missing required data in request")
            return jsonify({'error': 'Missing required data'}), 400
            
        detections = request.json['detections']
        image_path = request.json['image_path']
        
        logger.info(f"Processing image: {image_path}")
        logger.debug(f"Number of detections: {len(detections)}")
        
        if not os.path.exists(image_path):
            logger.error(f"Image not found: {image_path}")
            return jsonify({'error': f'Image not found at path: {image_path}'}), 404
            
        image = cv2.imread(image_path)
        logger.info(f"Image shape: {image.shape}")
        
        grouped_detections = grouper.group_products(image, detections)
        logger.info(f"Grouped {len(grouped_detections)} detections")
        
        output_path = os.path.join(
            os.path.dirname(image_path),
            f'detected_{os.path.basename(image_path)}'
        )
        
        grouper.visualize_groups(image, grouped_detections, output_path)
        logger.info("Visualization completed")
        
        return jsonify({
            'status': 'success',
            'grouped_detections': grouped_detections
        })
        
    except Exception as e:
        logger.error(f"Error in group endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)