from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import cv2
import numpy as np
from pipeline import DroneAnalysisPipeline
import base64

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Initialize pipeline
pipeline = DroneAnalysisPipeline()

UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save uploaded file
    img_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(img_path)

    # Run analysis
    result_filename = f"result_{file.filename}"
    result_path = os.path.join(RESULTS_FOLDER, result_filename)
    
    # Updated to return both counts
    img_result, counts = pipeline.analyze_image(img_path, output_path=result_path)
    human_count = counts['human']
    car_count = counts['car']

    # Convert result image to base64 for easy display
    with open(result_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    return jsonify({
        'human_count': human_count,
        'car_count': car_count,
        'image': encoded_string
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
