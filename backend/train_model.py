import os
import cv2
import numpy as np
from lbp.lbp import compute_lbp
from lbp.histogram import lbph_features

def train_faces(dataset_path="data/train"):
    database = []

    for label in os.listdir(dataset_path):
        person_dir = os.path.join(dataset_path, label)
        if not os.path.isdir(person_dir): continue

        for img_name in os.listdir(person_dir):
            path = os.path.join(person_dir, img_name)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

            if img is None:
                print(f"⚠️ Skipped unreadable image: {path}")
                continue

            img = cv2.resize(img, (64, 64))
            lbp_img = compute_lbp(img)
            feature_vector = lbph_features(lbp_img)
            database.append((label, feature_vector))
            print(f"✅ Processed: {path} → Label: {label}")

    os.makedirs("models", exist_ok=True)
    np.save("models/lbph_database.npy", np.array(database, dtype=object))
    print("✅ Training complete! Database saved to models/lbph_database.npy.")

if __name__ == "__main__":
    train_faces()
