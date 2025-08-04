import os
from PIL import Image, ImageOps
import random

SOURCE_DIR = "dataset"
DEST_DIR = "augmented_dataset"

def crop_center(image):
    """Crop image to center square"""
    width, height = image.size
    crop_size = int(min(width, height) * 0.8)
    left = (width - crop_size) // 2
    top = (height - crop_size) // 2
    right = left + crop_size
    bottom = top + crop_size
    return image.crop((left, top, right, bottom)).resize((100, 100))  # Resized to fixed size

def augment(image, save_dir, base_name):
    """Generate and save augmented images"""
    # Save original cropped
    cropped = crop_center(image)
    cropped.save(os.path.join(save_dir, f"{base_name}_original.jpg"))

    # Flipped
    flipped = ImageOps.mirror(cropped)
    flipped.save(os.path.join(save_dir, f"{base_name}_flipped.jpg"))

    # Rotated
    angle = random.choice([-10, 10])
    rotated = cropped.rotate(angle)
    rotated.save(os.path.join(save_dir, f"{base_name}_rotated.jpg"))

def run_augmentation():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    for person in os.listdir(SOURCE_DIR):
        person_path = os.path.join(SOURCE_DIR, person)
        dest_person = os.path.join(DEST_DIR, person)
        os.makedirs(dest_person, exist_ok=True)

        for idx, file in enumerate(os.listdir(person_path)):
            if file.endswith(".jpg") or file.endswith(".png"):
                img_path = os.path.join(person_path, file)
                image = Image.open(img_path).convert("L")  # Convert to grayscale
                base = f"{person}_{idx}"
                augment(image, dest_person, base)

    print("✅ Cropping & Augmentation Done.")

if __name__ == "__main__":
    run_augmentation()
