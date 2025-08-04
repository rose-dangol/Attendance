import os
import numpy as np
from PIL import Image
import cv2
from sklearn.metrics.pairwise import euclidean_distances

# === Constants ===
DATASET_DIR = "augmented_dataset"
IMAGE_SIZE = (100, 100)  # LBP input size

# === LBP Function ===
def compute_lbp(image_array):
    height, width = image_array.shape
    lbp = np.zeros((height - 2, width - 2), dtype=np.uint8)

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            center = image_array[i, j]
            binary = ''
            binary += '1' if image_array[i - 1, j - 1] >= center else '0'
            binary += '1' if image_array[i - 1, j] >= center else '0'
            binary += '1' if image_array[i - 1, j + 1] >= center else '0'
            binary += '1' if image_array[i, j + 1] >= center else '0'
            binary += '1' if image_array[i + 1, j + 1] >= center else '0'
            binary += '1' if image_array[i + 1, j] >= center else '0'
            binary += '1' if image_array[i + 1, j - 1] >= center else '0'
            binary += '1' if image_array[i, j - 1] >= center else '0'

            lbp[i - 1, j - 1] = int(binary, 2)
    return lbp

# === Histogram Function ===
def extract_histogram(lbp_img):
    hist, _ = np.histogram(lbp_img.ravel(), bins=256, range=(0, 256))
    hist = hist.astype("float")
    hist /= (hist.sum() + 1e-7)
    return hist

# === Load Training Data ===
def load_dataset():
    features = []
    labels = []

    for label in os.listdir(DATASET_DIR):
        person_path = os.path.join(DATASET_DIR, label)
        if not os.path.isdir(person_path):
            continue

        for file in os.listdir(person_path):
            img_path = os.path.join(person_path, file)
            img = Image.open(img_path).convert("L").resize(IMAGE_SIZE)
            img_array = np.array(img)

            lbp = compute_lbp(img_array)
            hist = extract_histogram(lbp)

            features.append(hist)
            labels.append(label)

    return features, labels

# === Predict Function ===
def predict_frame(gray_frame, train_features, train_labels):
    resized = cv2.resize(gray_frame, IMAGE_SIZE)
    lbp = compute_lbp(resized)
    hist = extract_histogram(lbp)

    distances = euclidean_distances([hist], train_features)[0]
    idx = np.argmin(distances)
    return train_labels[idx], distances[idx]

# === Main Real-Time Loop ===
def live_recognition():
    print(" Loading training data...")
    features, labels = load_dataset()
    print(f" Loaded {len(labels)} training images.\n")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print(" Cannot access webcam.")
        return

    print(" Starting real-time face recognition...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Predict label
        name, distance = predict_frame(gray, features, labels)

        # Display name on frame
        label = f"{name} ({distance:.2f})"
        cv2.putText(frame, label, (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2)

        # Show the frame
        cv2.imshow("LBPH Real-Time Recognition", frame)

        key = cv2.waitKey(1)
        if key == 27:  # ESC to quit
            break

    cap.release()
    cv2.destroyAllWindows()

# === Run It ===
if __name__ == "__main__":
    live_recognition()
