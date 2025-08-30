import cv2

TRAINER_FILE = "trainer.yml"
LABELS_FILE = "labels.txt"

# Load trained model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(TRAINER_FILE)

# Load labels
labels = {}
with open(LABELS_FILE, "r") as f:
    for line in f.readlines():
        id_, name = line.strip().split(",")
        labels[int(id_)] = name

# Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (200, 200))

        id_, confidence = recognizer.predict(roi_gray)

        if confidence < 70:  # lower = more confident
            name = labels.get(id_, "Unknown")
        else:
            name = "Unknown"

        # Draw rectangle + name
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, f"{name} ({int(confidence)})", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Live Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
