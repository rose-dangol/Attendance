import os
import numpy as np
import time
from PIL import Image
import cv2  # ✅ OpenCV for webcam
from sklearn.metrics.pairwise import euclidean_distances

# === Constants ===
DATASET_DIR = "augmented_dataset"
IMAGE_SIZE = (100, 100)  # Resize all images to fixed size

# === Step 1: Local Binary Pattern ===
def compute_lbp(image_array):
    """Apply Local Binary Pattern to an image array"""
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

# === Step 2: LBP Histogram ===
def extract_histogram(lbp_img):
    """Generate normalized histogram from LBP image"""
    hist, _ = np.histogram(lbp_img.ravel(), bins=256, range=(0, 256))
    hist = hist.astype("float")
    hist /= (hist.sum() + 1e-7)  # Avoid divide by zero
    return hist

# === Step 3: Load Training Images ===
def load_dataset():
    """Load dataset and extract LBP histograms and labels"""
    features = []
    labels = []

    for label in os.listdir(DATASET_DIR):
        person_path = os.path.join(DATASET_DIR, label)
        if not os.path.isdir(person_path):
            continue  # skip files

        for file in os.listdir(person_path):
            img_path = os.path.join(person_path, file)
            img = Image.open(img_path).convert("L").resize(IMAGE_SIZE)
            img_array = np.array(img)

            lbp = compute_lbp(img_array)
            hist = extract_histogram(lbp)

            features.append(hist)
            labels.append(label)

    return features, labels

# === Step 4: Webcam Capture using OpenCV ===
def capture_image(path="test.jpg"):
    """Capture a face image from webcam and save it"""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Cannot access webcam.")
        return None

    print("📸 Webcam open. Press SPACE to capture, ESC to cancel.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to read frame.")
            break

        cv2.imshow("Live - Press SPACE to Capture", frame)

        key = cv2.waitKey(1)
        if key % 256 == 27:  # ESC key
            print("❌ Capture cancelled.")
            break
        elif key % 256 == 32:  # SPACE key
            # Convert to grayscale and resize
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, IMAGE_SIZE)
            cv2.imwrite(path, resized)
            print(f"✅ Image captured and saved to {path}")
            break

    cap.release()
    cv2.destroyAllWindows()
    return path

# === Step 5: Predict Test Image ===
def predict_image(image_path, train_features, train_labels):
    """Compare input image with training set using LBP + Histogram"""
    img = Image.open(image_path).convert("L").resize(IMAGE_SIZE)
    img_array = np.array(img)

    lbp = compute_lbp(img_array)
    hist = extract_histogram(lbp)

    distances = euclidean_distances([hist], train_features)[0]
    idx = np.argmin(distances)
    return train_labels[idx]

# === Main Program ===
if __name__ == "__main__":
    print("🔧 Loading training dataset...")
    train_features, train_labels = load_dataset()
    print(f"✅ Loaded {len(train_labels)} training images.")

    test_path = capture_image()

    if test_path:
        prediction = predict_image(test_path, train_features, train_labels)
        print(f"\n🧠 Predicted Person: {prediction}")
