from flask import Flask, request, jsonify
import speech_recognition as sr
from transformers import CLIPProcessor, CLIPModel
import base64
import torch

app = Flask(__name__)

@app.route('/generate-image', methods=['POST'])
def generate_image():
    # Function to convert speech to text
    def speech_to_text():
        recognizer = sr.Recognizer()
        with sr.AudioFile(request.files['audio']):
            audio = recognizer.record(request.files['audio'])
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None

    # Function to generate image based on text prompt using CLIP
    def generate_image_from_text(text_prompt):
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16")
        inputs = processor(text=text_prompt, return_tensors="pt", padding=True)
        outputs = model(**inputs)
        image_features = outputs['pixel_values']
        image = Image.fromarray(image_features[0].numpy().astype("uint8"))
        return image

    # Get speech input and generate image
    speech_file = request.files['audio']
    text_prompt = speech_to_text()
    if text_prompt:
        image = generate_image_from_text(text_prompt)
        # Convert image to base64 for sending to frontend
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return jsonify({'success': True, 'image_base64': image_base64})
    else:
        return jsonify({'success': False})

if __name__ == '__main__':
    app.run(debug=True)
