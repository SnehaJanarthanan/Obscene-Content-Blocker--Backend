import boto3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/age_identification', methods=['POST'])
def send_url():
    data = request.json  # Assuming JSON data is sent
    received_url = data.get('url', '')  # Extracting the URL from JSON
    # Do something with the URL, for example, print it
    print("Received URL:", received_url)
    return jsonify({'message': 'URL received successfully'})

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app




# Initialize AWS Rekognition client
client = boto3.client('rekognition', region_name='ap-south-1', aws_access_key_id='KEY1', aws_secret_access_key='KEY2')

# Function to detect age range in an image
def detect_age(image_path):
    try:
        # Read image data
        with open(image_path, 'rb') as file:
            image_data = file.read()

        # Perform face detection
        response = client.detect_faces(
            Image={'Bytes': image_data},
            Attributes=['ALL']  
        )

        # Extract age range from the response
        face_details = response['FaceDetails']
        if len(face_details) > 0:
            age_range = face_details[0]['AgeRange']
            return age_range
        else:
            return None  # No face detected

    except Exception as e:
        print(f"Failed to process image: {e}")
        return None

# Example usage
age_range = detect_age(image_path)
if age_range:
    print(f"Detected age range: {age_range}")
else:
    print("No face detected in the image.")
