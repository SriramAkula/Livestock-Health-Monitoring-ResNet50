import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
import os

# Load trained model
model = load_model("C:\\Users\\micro\\OneDrive\\Desktop\\PROJECTS\\ComputerVision\\Camera_Included\\ResNet50_FineTuned_Best.h5")
print("✅ Model Loaded Successfully!")

# Class labels
class_labels = ['Healthy', 'Sick']
IMG_HEIGHT, IMG_WIDTH = 224, 224
min_prob_val = 0.65

# Preprocess function
def preprocess(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Mediapipe Hands Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# OpenCV Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # width
cap.set(4, 480)  # height

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Failed to capture frame.")
        break

    # Prediction
    processed_frame = preprocess(frame)
    prediction = model.predict(processed_frame)[0][0]
    predicted_class = int(prediction > 0.5)
    confidence = float(prediction) if predicted_class == 1 else 1 - float(prediction)

    if confidence > min_prob_val:
        label = f"{class_labels[predicted_class]}: {confidence:.2f}"
        cv2.putText(frame, label, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
    else:
        cv2.putText(frame, "Detecting...", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

    # Hand Gesture Detection
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            thumb_tip = hand_landmarks.landmark[4]
            thumb_ip = hand_landmarks.landmark[3]
            index_tip = hand_landmarks.landmark[8]
            index_ip = hand_landmarks.landmark[6]

            # Thumbs Up Gesture Detection
            if thumb_tip.y < thumb_ip.y and index_tip.y > index_ip.y:
                cv2.putText(frame, '👍 Thumbs Up Detected! Closing Camera...',
                            (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.imshow('Livestock Health Detection', frame)
                cv2.waitKey(2000)
                cap.release()
                cv2.destroyAllWindows()
                print("👋 Camera Closed with Thumbs Up Gesture!")
                exit()

    cv2.imshow('Livestock Health Detection', frame)

    # ESC key to quit
    if cv2.waitKey(1) & 0xFF == 27:
        print("👋 Camera Closed with ESC Key!")
        break

cap.release()
cv2.destroyAllWindows()
