import cv2
import os
import numpy as np

DATASET_DIR = "dataset"  # your dataset folder
TRAINER_FILE = "trainer.yml"
LABELS_FILE = "labels.txt"

# Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Prepare training data
faces = []
labels = []
label_dict = {}  # name -> id
current_id = 0

print("[INFO] Preparing dataset...")

for person_name in os.listdir(DATASET_DIR):
    person_path = os.path.join(DATASET_DIR, person_name)
    if not os.path.isdir(person_path):
        continue

    # assign numeric id to each person
    if person_name not in label_dict:
        label_dict[person_name] = current_id
        current_id += 1

    person_id = label_dict[person_name]

    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)

        # read image
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue

        # detect face in the image
        faces_rects = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)
        for (x, y, w, h) in faces_rects:
            roi = img[y:y+h, x:x+w]
            roi_resized = cv2.resize(roi, (200, 200))
            faces.append(roi_resized)
            labels.append(person_id)

print(f"[INFO] Total faces: {len(faces)}")
print(f"[INFO] Total labels: {len(labels)}")

# Train LBPH recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces, np.array(labels))
recognizer.save(TRAINER_FILE)

# Save labels mapping (id -> name)
with open(LABELS_FILE, "w") as f:
    for name, id_ in label_dict.items():
        f.write(f"{id_},{name}\n")

print("[INFO] Training complete. Model saved as trainer.yml and labels.txt")
