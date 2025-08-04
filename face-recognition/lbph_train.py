import os
import numpy as np
from PIL import Image
from collections import defaultdict
from sklearn.metrics.pairwise import euclidean_distances

DATASET_DIR = "augmented_dataset"
IMAGE_SIZE = (100, 100)  # Standardized image size

def compute_lbp(image_array):
    """Apply LBP to image array (2D grayscale)"""
    height, width = image_array.shape
    lbp = np.zeros((height-2, width-2), dtype=np.uint8)

    # Loop over image except edges
    for i in range(1, height-1):
        for j in range(1, width-1):
            center = image_array[i, j]
            binary = ''
            # Clockwise comparison with 8 neighbors
            binary += '1' if image_array[i-1, j-1] >= center else '0'
            binary += '1' if image_array[i-1, j] >= center else '0'
            binary += '1' if image_array[i-1, j+1] >= center else '0'
            binary += '1' if image_array[i, j+1] >= center else '0'
            binary += '1' if image_array[i+1, j+1] >= center else '0'
            binary += '1' if image_array[i+1, j] >= center else '0'
            binary += '1' if image_array[i+1, j-1] >= center else '0'
            binary += '1' if image_array[i, j-1] >= center else '0'
            
            lbp[i-1, j-1] = int(binary, 2)
    return lbp

def extract_histogram(lbp_img):
    """Compute normalized histogram from LBP image"""
    hist, _ = np.histogram(lbp_img.ravel(), bins=256, range=(0, 256))
    hist = hist.astype("float")
    hist /= (hist.sum() + 1e-7)  # Normalize
    return hist

def load_dataset():
    """Read dataset, compute LBP histograms"""
    features = []
    labels = []
    
    for label in os.listdir(DATASET_DIR):
        person_path = os.path.join(DATASET_DIR, label)
        for file in os.listdir(person_path):
            path = os.path.join(person_path, file)
            img = Image.open(path).resize(IMAGE_SIZE)
            img_array = np.array(img)

            lbp_img = compute_lbp(img_array)
            hist = extract_histogram(lbp_img)

            features.append(hist)
            labels.append(label)
    return features, labels

def predict(test_path, train_features, train_labels):
    """Predict person from test image"""
    img = Image.open(test_path).convert("L").resize(IMAGE_SIZE)
    test_array = np.array(img)
    test_lbp = compute_lbp(test_array)
    test_hist = extract_histogram(test_lbp)

    dists = euclidean_distances([test_hist], train_features)[0]
    index = np.argmin(dists)
    return train_labels[index]

if __name__ == "__main__":
    # STEP 1: Load training data
    print("📦 Training LBPH model...")
    features, labels = load_dataset()
    print(f"✅ Training complete. Total images: {len(labels)}")

    # STEP 2: Predict from test image
    test_img = input("🧪 Enter test image path (e.g., test.jpg): ")
    prediction = predict(test_img, features, labels)
    print(f"🧠 Predicted Person: {prediction}")
