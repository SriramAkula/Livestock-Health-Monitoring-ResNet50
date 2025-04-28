from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)

# Load trained model
model = load_model("C:\\Users\\micro\\OneDrive\\Desktop\\PROJECTS\\ComputerVision\\Camera_Included\\ResNet50_FineTuned_Best.h5")

# Class labels
class_labels = ['Healthy', 'Sick']

IMG_HEIGHT = 224
IMG_WIDTH = 224

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded.'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected.'})

    if file:
        upload_folder = 'static/uploads'
        os.makedirs(upload_folder, exist_ok=True)

        filepath = os.path.join(upload_folder, file.filename)
        file.save(filepath)

        img = image.load_img(filepath, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        prediction = model.predict(img_array)[0][0]
        predicted_class = int(prediction > 0.5)
        result = class_labels[predicted_class]
        confidence = float(prediction) if predicted_class == 1 else 1 - float(prediction)

        print("🔍 Raw output:", prediction)
        print("✅ Predicted class:", result)
        print("📊 Confidence:", confidence)

        return jsonify({
            'prediction': result,
            'confidence': round(confidence * 100, 2)
        })

    return jsonify({'error': 'Prediction failed'})


if __name__ == '__main__':
    app.run(debug=True)
