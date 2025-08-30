import os
import cv2
import random

SOURCE_DIR = "dataset"
DEST_DIR = "augmented_dataset"
IMAGE_SIZE = (100, 100)  # fixed size after crop

def crop_center(image):
    """Crop image to center square and resize"""
    h, w = image.shape[:2]
    crop_size = int(min(w, h) * 0.8)
    left = (w - crop_size) // 2
    top = (h - crop_size) // 2
    right = left + crop_size
    bottom = top + crop_size
    cropped = image[top:bottom, left:right]
    return cv2.resize(cropped, IMAGE_SIZE)

def augment(image, save_dir, base_name):
    """Generate and save augmented images"""
    # Save original cropped
    cropped = crop_center(image)
    cv2.imwrite(os.path.join(save_dir, f"{base_name}_original.jpg"), cropped)

    # Flipped (horizontal mirror)
    flipped = cv2.flip(cropped, 1)
    cv2.imwrite(os.path.join(save_dir, f"{base_name}_flipped.jpg"), flipped)

    # Rotated (+/- 10 degrees)
    angle = random.choice([-10, 10])
    h, w = cropped.shape[:2]
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    rotated = cv2.warpAffine(cropped, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
    cv2.imwrite(os.path.join(save_dir, f"{base_name}_rotated.jpg"), rotated)

def run_augmentation():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    for person in os.listdir(SOURCE_DIR):
        person_path = os.path.join(SOURCE_DIR, person)
        if not os.path.isdir(person_path):
            continue

        dest_person = os.path.join(DEST_DIR, person)
        os.makedirs(dest_person, exist_ok=True)

        for idx, file in enumerate(os.listdir(person_path)):
            if file.lower().endswith((".jpg", ".png", ".jpeg")):
                img_path = os.path.join(person_path, file)
                image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # load as grayscale
                if image is None:
                    print(f"⚠️ Could not read {img_path}, skipping.")
                    continue
                base = f"{person}_{idx}"
                augment(image, dest_person, base)

    print("✅ Cropping & Augmentation Done.")

if __name__ == "__main__":
    run_augmentation()
