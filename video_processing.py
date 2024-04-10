import os
import boto3
from flask import Flask, request, jsonify
from flask_cors import CORS  
import time

app = Flask(__name__)
CORS(app, origins="*") 

def detect_obscene_image_AWS(image_path, access_key_id, secret_access_key, region_name='ap-south-1'):
    client = boto3.client('rekognition', region_name=region_name, aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    
    obscene_labels = ['Explicit Nudity', 'Graphic Violence', 'Illegal Drugs', 'Weapons', 'Terrorism', 'Hate Symbols', 'Sexual Activity']
    
    try:
        time.sleep(15)
        img_data = image_path
        with open(img_data, 'rb') as file:
            img_data = file.read()
        response = client.detect_moderation_labels(Image={'Bytes': img_data}, MinConfidence=40)
        moderation_labels = response.get('ModerationLabels', [])
        
        # Check if any of the detected labels are obscene
        if any(label['Name'] in obscene_labels for label in moderation_labels):
            print("Obscene image detected.")
            return True  
        else:
            print("No obscene content detected.")
            return False  
    
    except Exception as e:
        print(f"Failed to process image: {e}")
        return False 

@app.route('/',methods=['GET'])
# def hello():
#     return "Hello World!"

@app.route('/videos', methods=['POST'])
def check_obscene_image():
    try:
        print("Check")
        image_data = request.get_json()
        print(image_data)
        image_path = image_data.get('image_path')
        print(image_path)
        is_obscene = detect_obscene_image_AWS(image_path, "KEY1", "KEY2", region_name='ap-south-1')
        print("Is image obscene?", is_obscene)
     

        return jsonify({'obscene':  is_obscene}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
