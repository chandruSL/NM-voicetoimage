from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from transformers import CLIPProcessor, CLIPModel
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64
import torch

app = Flask(__name__)
CORS(app)

# Initialize CLIP processor and model outside of route handler
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.get_json()
    text_prompt = data.get('text')

    def generate_image_from_text(text_prompt):
        # Create a new image with the specified background color
        image = Image.new("RGB", (400, 200), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        # Load a font and calculate text size and position
        font = ImageFont.load_default()
        text_width, text_height = draw.textsize(text_prompt, font=font)
        text_x = (400 - text_width) // 2
        text_y = (200 - text_height) // 2

        # Draw the text on the image
        draw.text((text_x, text_y), text_prompt, fill=(0, 0, 0), font=font)

        return image

    if text_prompt:
        try:
            image = generate_image_from_text(text_prompt)
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            return jsonify({'success': True, 'image_base64': image_base64})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    else:
        return jsonify({'success': False, 'error': 'No text provided'})

if __name__ == '__main__':
    app.run(debug=True)
