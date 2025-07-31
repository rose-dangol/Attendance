from image_data import ImageData
import numpy as np
# from matplotlib import image as mpimg 
import time

start_time = time.time()
class HaarFeatureScanner:
  def __init__(self, image_data):
    self.img = image_data
    self.integral= image_data.integral

    self.feature_type = [
      ("horizontal_edge", 2, 1),
      ("vertical_edge", 1, 2),
      ("horizontal_line", 3, 1),
      ("vertical_line", 1, 3),
      ("checkerboard", 2, 2)
    ]

  def haarlike_feature(self, feature_type, row, col, height, width):
    # white_sum = 0
    # black_sum = 0

    gs = self.img.get_sum

    if feature_type == "horizontal_edge":
      white_sum = gs(row, col, row + height//2, col + width)
      black_sum = gs(row + height//2, col, row + height, col + width)
      return white_sum - black_sum

    elif feature_type == "vertical_edge":
      white_sum = gs(row, col, row + height, col + width//2)
      black_sum = gs(row, col + width//2,row + height, col + width)

      return white_sum - black_sum

    elif feature_type == "horizontal_line":
      white_sum1 = gs(row, col, row + height//3, col + width)
      black_sum = gs(row + height//3, col, row + 2*height//3, col + width)
      white_sum2  = gs(row + 2*height//3, col, row + height, col + width)
      return (white_sum1 + white_sum2) - black_sum

    elif feature_type == "vertical_line":
      white_sum1 = gs(row, col, row + height, col + width//3)
      black_sum = gs(row, col + width//3, row + height, col + 2*width//3)
      white_sum2  = gs(row, col + 2*width//3, row + height, col + width)
      return (white_sum1 + white_sum2) - black_sum

    elif feature_type == "checkerboard":
      white_sum1 = gs(row, col, row + height//2, col + width//2)
      black_sum1 = gs(row, col + width//2, row + height//2, col + width)
      black_sum2 = gs(row + height//2, col, row + height, col + width//2)
      white_sum2  = gs(row + height//2, col + width//2, row + height, col + width)
      return (white_sum1 + white_sum2) - (black_sum1 + black_sum2)

    # else:
    #   return ValueError("Unknown feature type") 
    
    # return feature_value
  

  
  # def generate_all_features(self, window_size = 24, step = 3):
  def generate_all_features(self, window_size = 12, step = 9):
  # def generate_all_features(self, window_size = 24, step = 3):
    # feature_type = [
    #   ("horizontal_edge", 2, 1),
    #   ("vertical_edge", 1, 2),
    #   ("horizontal_line", 3, 1),
    #   ("vertical_line", 1, 3),
    #   ("checkerboard", 2, 2)
    # ]
    rows, cols = self.img.gray.shape

    # all_features = []
    for f_type, min_h, min_w in self.feature_type:
      for h in range(min_h, window_size+1, min_h): 
      # for h in [min_h, min_h*2, min_h*3]: 
        for w in range(min_w, window_size+1, min_w):
        # for w in [min_w, min_w*2, min_w*3]:

          if h > rows or w > cols:
            continue
          
          # For sliding window
          for r in range(0, rows - h + 1, step):     # so that sliding window doesnt go out of bound
            for c in range(0, cols - w + 1, step):    # so that sliding window doesnt go out of bound
              feature_value = self.haarlike_feature(f_type, r, c, h, w)
              yield (f_type, (r, c), (h, w), feature_value)

    



img = ImageData('dataset/faces/WIN_20250710_12_34_22_Pro.jpg')
scanner = HaarFeatureScanner(img)

count = 0
# for feat in scanner.generate_all_features(window_size=24, step=3):      # long time
for feat in scanner.generate_all_features(window_size=12, step=9):      # 10.624948024749756 secs
# for feat in scanner.generate_all_features(window_size=12, step=5):      # 31.829795122146606 secs
# for feat in scanner.generate_all_features(window_size=12, step=3):
# for feat in scanner.generate_all_features(window_size=24, step=9):      # 40.53484916687012 secs
# for feat in scanner.generate_all_features(window_size=24, step=5):      # 126.53914332389832 secs
# for feat in scanner.generate_all_features(window_size=24, step=3):      # 342.6353735923767 secs for completion
  if count < 5:
    print(feat)
  count += 1

print(f"Total features extracted: {count}")   # Total features extracted: 110409360 ( for window_size=24, step=3)
                                              # Total features extracted: 12341905  (for window_size=24, step=9)
end_time = time.time()
elapsed_time = end_time - start_time

print(f"{elapsed_time} secs for completion")



