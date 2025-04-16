# from django.test import TestCase

# # Create your tests here.
# import cv2

# # Load the pre-trained face detection model (Haar Cascade)
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# # Read image
# image = cv2.imread('C:/Users/DKC/Desktop/617495.jpg')  # Replace with your image path
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Detect faces
# faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

# # Draw rectangles around faces
# for (x, y, w, h) in faces:
#     cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

# # Show the result
# cv2.imshow('Face Detection', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
import cv2
import os

# Load pre-trained Haar Cascade model for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open webcam
cap = cv2.VideoCapture(0)

# Create folder to save face images
save_dir = "faces"
os.makedirs(save_dir, exist_ok=True)
face_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces (x, y, width, height)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Draw rectangles & save data
    for (x, y, w, h) in faces:
        # Draw rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Crop and save face image
        face_img = frame[y:y+h, x:x+w]
        face_filename = os.path.join(save_dir, f"face_{face_count}.jpg")
        cv2.imwrite(face_filename, face_img)
        print(f"Saved: {face_filename}")
        face_count += 1

    # Display the frame
    cv2.imshow('Face Detector - Press Q to quit', frame)

    # Exit on Q key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
