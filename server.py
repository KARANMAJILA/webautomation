from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image
import io
import base64
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import requests
import time

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# Load face cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

HAIRSTYLE_PROMPTS = {
    # Male Short
    "crew cut": "man with crew cut hairstyle, professional photo, high quality",
    "buzz fade": "man with buzz fade hairstyle, professional photo, high quality",
    "caesar": "man with caesar cut hairstyle, professional photo, high quality",
    "french crop": "man with french crop hairstyle, professional photo, high quality",
    "ivy league": "man with ivy league hairstyle, professional photo, high quality",
    "flat top": "man with flat top hairstyle, professional photo, high quality",
    "high fade": "man with high fade hairstyle, professional photo, high quality",
    "textured crop": "man with textured crop hairstyle, professional photo, high quality",
    "undercut": "man with undercut hairstyle, professional photo, high quality",
    "slicked back short": "man with slicked back short hairstyle, professional photo, high quality",
    "messy crop": "man with messy crop hairstyle, professional photo, high quality",
    "skin fade": "man with skin fade hairstyle, professional photo, high quality",
    
    # Male Medium
    "quiff": "man with quiff hairstyle, professional photo, high quality",
    "slicked back": "man with slicked back hairstyle, professional photo, high quality",
    "modern shag": "man with modern shag hairstyle, professional photo, high quality",
    "pompadour": "man with pompadour hairstyle, professional photo, high quality",
    "bro flow": "man with bro flow hairstyle, professional photo, high quality",
    "medium waves": "man with medium waves hairstyle, professional photo, high quality",
    "textured top": "man with textured top hairstyle, professional photo, high quality",
    "side part": "man with side part hairstyle, professional photo, high quality",
    "taper fade": "man with taper fade hairstyle, professional photo, high quality",
    "swept back": "man with swept back hairstyle, professional photo, high quality",
    "faux hawk": "man with faux hawk hairstyle, professional photo, high quality",
    "beach waves": "man with beach waves hairstyle, professional photo, high quality",
    
    # Male Long
    "long & wavy": "man with long wavy hairstyle, professional photo, high quality",
    "man bun": "man with man bun hairstyle, professional photo, high quality",
    "shoulder length": "man with shoulder length hairstyle, professional photo, high quality",
    "surfer style": "man with surfer style hairstyle, professional photo, high quality",
    "samurai bun": "man with samurai bun hairstyle, professional photo, high quality",
    "long layers": "man with long layers hairstyle, professional photo, high quality",
    "dreadlocks": "man with dreadlocks hairstyle, professional photo, high quality",
    "locs": "man with locs hairstyle, professional photo, high quality",
    "long curls": "man with long curls hairstyle, professional photo, high quality",
    "viking braids": "man with viking braids hairstyle, professional photo, high quality",
    "half bun": "man with half bun hairstyle, professional photo, high quality",
    "mullet modern": "man with modern mullet hairstyle, professional photo, high quality",
    
    # Female Short
    "pixie cut": "woman with pixie cut hairstyle, professional photo, high quality",
    "bob": "woman with bob hairstyle, professional photo, high quality",
    "shaggy bob": "woman with shaggy bob hairstyle, professional photo, high quality",
    "blunt cut": "woman with blunt cut hairstyle, professional photo, high quality",
    "curly crop": "woman with curly crop hairstyle, professional photo, high quality",
    "french pixie": "woman with french pixie hairstyle, professional photo, high quality",
    "asymmetrical bob": "woman with asymmetrical bob hairstyle, professional photo, high quality",
    "short layers": "woman with short layers hairstyle, professional photo, high quality",
    "modern pixie": "woman with modern pixie hairstyle, professional photo, high quality",
    "choppy layers": "woman with choppy layers hairstyle, professional photo, high quality",
    "textured crop": "woman with textured crop hairstyle, professional photo, high quality",
    
    # Female Medium
    "layered": "woman with layered hairstyle, professional photo, high quality",
    "balayage": "woman with balayage highlights hairstyle, professional photo, high quality",
    "wolf cut": "woman with wolf cut hairstyle, professional photo, high quality",
    "lob": "woman with lob hairstyle, professional photo, high quality",
    "curtain bangs": "woman with curtain bangs hairstyle, professional photo, high quality",
    "feathered": "woman with feathered hairstyle, professional photo, high quality",
    "textured waves": "woman with textured waves hairstyle, professional photo, high quality",
    "face-framing layers": "woman with face-framing layers hairstyle, professional photo, high quality",
    "shag cut": "woman with shag cut hairstyle, professional photo, high quality",
    "piece-y layers": "woman with piece-y layers hairstyle, professional photo, high quality",
    "side swept": "woman with side swept hairstyle, professional photo, high quality",
    "shoulder length waves": "woman with shoulder length waves hairstyle, professional photo, high quality",
    
    # Female Long
    "wavy": "woman with wavy long hairstyle, professional photo, high quality",
    "braided": "woman with braided hairstyle, professional photo, high quality",
    "straight & long": "woman with straight long hairstyle, professional photo, high quality",
    "loose curls": "woman with loose curls hairstyle, professional photo, high quality",
    "layered lengths": "woman with layered lengths hairstyle, professional photo, high quality",
    "fishtail braid": "woman with fishtail braid hairstyle, professional photo, high quality",
    "beach waves": "woman with beach waves hairstyle, professional photo, high quality",
    "beachy blonde": "woman with beachy blonde waves hairstyle, professional photo, high quality",
    "mermaid waves": "woman with mermaid waves hairstyle, professional photo, high quality",
    "silk press": "woman with silk press hairstyle, professional photo, high quality",
    "long layers": "woman with long layers hairstyle, professional photo, high quality",
    "flowing curls": "woman with flowing curls hairstyle, professional photo, high quality",
}

def generate_image_with_ai(hairstyle_name, gender="female"):
    """Generate image using free AI API (Pollinations)"""
    try:
        prompt = HAIRSTYLE_PROMPTS.get(hairstyle_name.lower(), f"person with {hairstyle_name} hairstyle")
        
        # Using free Pollinations API - no authentication needed
        url = f"https://image.pollinations.ai/prompt/{prompt}?width=512&height=512&seed={int(time.time() * 1000)}"
        
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            return base64.b64encode(response.content).decode()
        else:
            print(f"API Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return None

def overlay_hairstyle(original_img_base64, ai_img_base64):
    """Blend AI-generated hairstyle onto original photo"""
    try:
        # Decode images
        original_img = Image.open(io.BytesIO(base64.b64decode(original_img_base64)))
        ai_img = Image.open(io.BytesIO(base64.b64decode(ai_img_base64)))
        
        # Resize AI image to match original
        original_img = original_img.convert('RGB')
        ai_img = ai_img.convert('RGB')
        ai_img = ai_img.resize(original_img.size, Image.Resampling.LANCZOS)
        
        # Blend images (70% AI hairstyle, 30% original)
        blended = Image.blend(original_img, ai_img, 0.4)
        
        # Convert back to base64
        buffer = io.BytesIO()
        blended.save(buffer, format="JPEG", quality=95)
        return base64.b64encode(buffer.getvalue()).decode()
        
    except Exception as e:
        print(f"Error blending images: {str(e)}")
        return ai_img_base64

def get_recommendations(hairstyle):
    """Generate recommendations for hairstyle"""
    recommendations = {
        "crew cut": "Timeless and professional. Great for business settings.",
        "bob": "Classic and versatile. Suits most face shapes.",
        "pixie cut": "Bold and low-maintenance. Frames the face beautifully.",
        "undercut": "Modern and edgy. Makes a strong statement.",
        "long wavy": "Romantic and elegant. Adds softness to features.",
        "braided": "Protective and stylish. Works with many occasions.",
    }
    return recommendations.get(hairstyle.lower(), f"The {hairstyle} is a great choice!")

@app.route('/')
def index():
    return "🚀 Hairstyle AI Server Running"

@app.route('/api/generate-hairstyle', methods=['POST'])
def generate_hairstyle():
    try:
        if 'photo' not in request.files:
            return jsonify({"success": False, "error": "Photo required"}), 400
        
        file = request.files['photo']
        hairstyle = request.form.get('selectedHairstyle')
        
        if not file or not hairstyle:
            return jsonify({"success": False, "error": "Missing data"}), 400
        
        # Read original photo
        original_img = Image.open(file.stream).convert('RGB')
        
        # Convert to base64
        buffer = io.BytesIO()
        original_img.save(buffer, format="JPEG", quality=95)
        original_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        print(f"🎨 Generating {hairstyle} hairstyle...")
        
        # Generate AI hairstyle image
        ai_img_base64 = generate_image_with_ai(hairstyle)
        
        if not ai_img_base64:
            return jsonify({"success": False, "error": "Failed to generate hairstyle"}), 500
        
        # Blend images
        print("🎭 Blending hairstyle with your photo...")
        result_base64 = overlay_hairstyle(original_base64, ai_img_base64)
        
        recommendation = get_recommendations(hairstyle)
        
        return jsonify({
            "success": True,
            "generatedImage": f"data:image/jpeg;base64,{result_base64}",
            "recommendation": f"✨ {recommendation}",
            "hairstyle": hairstyle,
            "time": datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({
        "status": "ok",
        "service": "Hairstyle AI Generator",
        "method": "AI Image Generation + Blending"
    })

if __name__ == '__main__':
    print("🚀 Hairstyle AI Server Running on http://localhost:5000")
    print("📷 Upload photos and transform hairstyles with AI!")
    app.run(debug=False, host='0.0.0.0', port=5000)