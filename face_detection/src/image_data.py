import numpy as np
from matplotlib import image as mpimg    # to read image as numpy array
# import time


class ImageData:

  def __init__(self, image_path):
    self.image_path = image_path
    self.rgb = self.load_image()
    self.gray = self.rgb_to_grayscale()
    self.integral = self.compute_integral_image()

  def load_image(self):
    return mpimg.imread(self.image_path)
  
  def rgb_to_grayscale(self):
    # luminance formula
    return (self.rgb[:,:,0] * 0.299  + self.rgb[:,:,1] * 0.587 + self.rgb[:,:,2] * 0.114)
    
  # '''
  def compute_integral_image(self):
    h,w = self.gray.shape
    integImage = np.zeros((h+1,w+1)) # extra padding

    for i in range(1, h+1):
      for j in range(1, w+1):
        # calculating the integral image using the recursive sum
        integImage[i,j] =  (integImage[i,j-1]+ integImage[i-1,j] - integImage[i-1,j-1] + self.gray[i-1,j-1])  # self.gray & ogImage same thing but something bachako?
        # also why is it inside () : just for grouping doesnt do anything

    return integImage
  # '''
  # calculating with nested for loops take long time so 
  # using NumPy built-in to compute cumulative sums 
  # def compute_integral_image(self):
  #   return self.gray.cumsum(axis=0).cumsum(axis=1)


  # '''
  def get_sum(self, x1, y1, x2, y2):
    A = self.integral[x2,y2]
    B = self.integral[x1-1,y2] if x1 > 0 else 0
    C = self.integral[x2,y1-1] if y1 > 0 else 0
    D = self.integral[x1-1,y1-1] if x1 > 0 and y1 > 0 else 0
    return A - B - C + D
  
  def show_info(self):
    print(f"Image path: {self.image_path}")
    print(f"RGB shape: {self.rgb.shape}")
    print(f"Grayscale shape: {self.gray.shape}")
    print(f"Integral shape: {self.integral.shape}")


img = ImageData('dataset/faces/oja.jpg')
