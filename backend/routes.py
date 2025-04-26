from flask import request, jsonify
from PIL import Image
import numpy as np
import torch
from fastai.vision.all import *
from agent import bot_run

# Load ML models
print("Loading ML models...")
pneumonia_model = load_learner("model.pkl")
tuberculosis_model = load_learner("modeltb.pkl")
brain_tumor_model = load_learner("modelbt.pkl")
print("ML models loaded successfully")

def process_image(image_tensor, model):
    """Process an image using the specified model"""
    try:
        predictions = model.predict(image_tensor, with_input=True)
        return f"{predictions[1]}: {int(predictions[3][predictions[3].argmax()] * 100)}%"
    except Exception as e:
        print(f"Error processing image: {e}")
        return "Error processing image"

def register_routes(app):
    @app.route('/chat', methods=['POST'])
    def chat():
        """Handle chat requests"""
        try:
            data = request.json
            user_message = data.get('message', '')
            
            response = bot_run(user_message)
            
            return jsonify({"response": response})
        except Exception as e:
            print(f"Error in chat endpoint: {e}")
            return jsonify({"error": str(e)}), 500

    @app.route('/analyze-image', methods=['POST'])
    def analyze_image():
        """Handle medical image analysis requests"""
        try:
            if 'image' not in request.files:
                return jsonify({"error": "No image provided"}), 400
            
            image_file = request.files['image']
            image_type = request.form.get("type")
            
            if image_file.filename == '':
                return jsonify({"error": "No selected file"}), 400
                
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'dicom'}
            if not '.' in image_file.filename or \
               image_file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                return jsonify({"error": f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"}), 400
            
            try:
                img = Image.open(image_file.stream)
                
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                    
                max_size = (1024, 1024)
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.LANCZOS)
                
                image_tensor = torch.tensor(np.array(img))
                
                if image_type == 'pneumonia':
                    result = process_image(image_tensor, pneumonia_model)
                    model_name = "Pneumonia"
                elif image_type == 'tuberculosis':
                    result = process_image(image_tensor, tuberculosis_model)
                    model_name = "Tuberculosis"
                elif image_type == 'brain_tumor':
                    result = process_image(image_tensor, brain_tumor_model)
                    model_name = "Brain Tumor"
                else:
                    return jsonify({"error": f"Invalid image type: {image_type}. Valid types are: pneumonia, tuberculosis, brain_tumor"}), 400
                
                return jsonify({
                    "analysis": result,
                    "model": model_name
                })
            except Exception as e:
                print(f"Error processing image: {e}")
                return jsonify({"error": f"Error processing image: {str(e)}"}), 500
                
        except Exception as e:
            print(f"Error in analyze-image endpoint: {e}")
            return jsonify({"error": str(e)}), 500 