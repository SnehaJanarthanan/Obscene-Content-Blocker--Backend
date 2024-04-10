import boto3
import os
import shutil

#uses AWS rekognition

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
            
    print(result_array)
    
    return result_array


#enter the key 1 and key 2 from the AWS rekognition
result = detect_obscene_images_AWS("input_images", "output_folder", KEY_1, KEY_2, region_name='ap-south-1')