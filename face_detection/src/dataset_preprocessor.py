# read raw images → resize → augment → convert to grayscale → compute integral image → save as .npy files

import os         # works with file path and folders
import numpy as np  # handle array
from matplotlib import image as mpimg # read image as numpy arrays 
from image_data import ImageData # reuse from our old class
import time   # to measure time taken

start_time = time.time()
# create class DatasetPreprocesor 
class DatasetPreprocesor:
  # constructor (__init__): runs auto when obj created
  def __init__(self, input_dir, output_dir, size=(24,24)):  
    '''
    self : 
    input_dir : folder to store raw img
    output_dir: folder to store processed img
    size=(24,24): 
    '''
    self.input_dir = input_dir
    self.output_dir = output_dir
    self.size = size
    os.makedirs(self.output_dir, exist_ok = True)

  # load >1 images
  def load_images(self):
    # get all images
    files = [f for f in os.listdir(self.input_dir)
              if f.lower().endswith(('.jpg','.png','.jpeg'))]
    return [os.path.join(self.input_dir, f) for f in files]
  
  def rgb_to_grayscale(self):
    # luminance formula
    return (self.rgb[:,:,0] * 0.299  + self.rgb[:,:,1] * 0.587 + self.rgb[:,:,2] * 0.114)

  # mannual resize (using nearest neighbour interpolation)
  def resize_image(self, img_array):
    target_h, target_w = self.size
    src_h, src_w = img_array.shape[:2]

    resized = np.zeros((target_h, target_w,3))
    for i in range(target_h):
      for j in range(target_w):
        y = int(i * src_h/target_h)
        x = int(j * src_w/target_w)
        resized[i,j] = img_array[y,x]

    return resized

  # augment
  def augment_image(self, img_array):
    # 4 version of image:
    # 1. original img
    augumented = [img_array]   

    # 2. flip horizontally
    augumented.append(np.fliplr(img_array))

    # Darker and brightness
    augumented.append(np.clip(img_array * 0.8, 0, 255)) # 3. dark
    augumented.append(np.clip(img_array * 1.2, 0, 255)) # 4. bright

    return augumented
  

  #preprocess and save
  def preprocess_save(self):
    files =self.load_images()
    count = 0

    for file in files:
      rgb = mpimg.imread(file)

      # Resize
      resized = self.resize_image(rgb)

      # Augment
      augmented_imgs = self.augment_image(resized)

      for img in augmented_imgs:
        # using ImageData from image_data
        temp = ImageData.__new__(ImageData) # creates new instance
        temp.rgb = img
        temp.gray = temp.rgb_to_grayscale()
        temp.integral = temp.compute_integral_image()

        # save as .npy
        save_path = os.path.join(
          self.output_dir, f"img_{count:4d}.npy")
        
        np.save(save_path, {
          "gray": temp.gray,
          "integral": temp.integral
        })
        
        count += 1

    print((f"Processed and saved: {count} imges to {self.output_dir}")) 
  end_time = time.time()
  elapsed_time = end_time - start_time

  print(f"{elapsed_time} secs for completion")


# from dataset_preprocessor import DatasetPreprocesor

# process faces
faces_pre = DatasetPreprocesor("dataset/faces", "procesed_dataset/faces")
faces_pre.preprocess_save()

# process no faces
no_faces_pre = DatasetPreprocesor("dataset/no_faces", "procesed_dataset/no_faces")
no_faces_pre.preprocess_save()




