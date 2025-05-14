
from flask import Flask, request, jsonify
from deepface import DeepFace
import os
import uuid
app = Flask(__name__)

@app.route('/')
def home():
    return "🧠 DeepFace Emotion API is running!"

@app.route('/analyze_emotion', methods=['POST'])
def analyze_emotion():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files['image']
    unique_filename = f"temp_{uuid.uuid4().hex}.jpg"
    image_path = os.path.join(unique_filename)
    image_file.save(image_path)

    try:
        result = DeepFace.analyze(img_path=image_path, actions=['emotion'])

        # Handle both dict and list output from DeepFace
        if isinstance(result, list):
            emotions = result[0]['emotion']
            dominant = result[0]['dominant_emotion']
        else:
            emotions = result['emotion']
            dominant = result['dominant_emotion']

        return jsonify({
            "emotions": emotions,
            "dominant_emotion": dominant
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(image_path):
            os.remove(image_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
