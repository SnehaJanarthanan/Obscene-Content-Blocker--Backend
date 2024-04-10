import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS  
import os
import urllib.request
import shutil
import boto3

app = Flask(__name__)
CORS(app, origins="*")

def download_images(image_paths, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for i, image_path in enumerate(image_paths):
        if image_path.startswith('http'):
            try:
                file_name = os.path.join(output_dir, f'image_{i}.jpg')
                urllib.request.urlretrieve(image_path, file_name)
                print(f"Downloaded {image_path} to {file_name}")
            except Exception as e:
                print(f"Failed to download {image_path}: {e}")
        else:
            print(f"Skipping non-HTTP image: {image_path}")

# Explicit image detection AWS
def detect_obscene_images_AWS(input_folder, output_folder, access_key_id, secret_access_key, region_name='ap-south-1'):
    client = boto3.client('rekognition', region_name=region_name, aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    obscene_labels = ['Explicit Nudity', 'Graphic Violence', 'Illegal Drugs', 'Weapons', 'Terrorism', 'Hate Symbols', 'Sexual Activity']
    result_array = []
    
    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            with open(image_path, 'rb') as image_file:
                image_bytes = image_file.read()
            response = client.detect_moderation_labels(Image={'Bytes': image_bytes}, MinConfidence=40)
            moderation_labels = response.get('ModerationLabels', [])
            if any(label['Name'] in obscene_labels for label in moderation_labels):
                result_array.append(1)  # Obscene image
                output_image_path = os.path.join(output_folder, filename)
                shutil.copy(image_path, output_image_path)
            else:
                result_array.append(0)  # Not obscene image
    
    return result_array

# EXPLICIT IMAGES

@app.route('/images', methods=['POST'])
def receive_images():
    try:
        data = request.get_json()
        images = data.get('images')
        print("Received images:", images)
        
        download_images(images, 'downloaded_images')
        
        output_folder = "output_folder"
        result = detect_obscene_images_AWS("input_images", output_folder, "KEY_1", "KEY_2", region_name='ap-south-1')
        print(result)
        
        return jsonify({'message': 'Images received and downloaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
