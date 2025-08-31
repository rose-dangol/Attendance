import numpy as np
import time
# from tqdm import tqdm

def compute_integral_image(image):
  return image.cumsum(axis=0).cumsum(axis=1)


def get_sum(integral, x1, y1, x2, y2):
  A = integral[x2,y2]
  B = integral[x1-1,y2] if x1 > 0 else 0
  C = integral[x2,y1-1] if y1 > 0 else 0
  D = integral[x1-1,y1-1] if x1 > 0 and y1 > 0 else 0
  return A - B - C + D


def haarlike_feature(integral,feature_type, row, col, height, width):
  # white_sum = 0
  # black_sum = 0

  # gs = self.img.get_sum
  # gs = lambda r1,c1,r2,c2: get_sum(integral,r1,c1,r2,c2)

  if feature_type == "horizontal_edge":
    # white_sum = gs(row, col, row + height//2 -1, col + width -1)
    white_sum = get_sum(integral, row, col, row + height // 2 -1, col + width - 1)
    black_sum = get_sum(integral, row + height // 2, col, row + height - 1, col + width - 1)
    return white_sum - black_sum

  elif feature_type == "vertical_edge":
    white_sum = get_sum(integral, row, col, row + height - 1, col + width//2 -1)
    black_sum = get_sum(integral, row, col + width//2,row + height -1, col + width - 1)
    return white_sum - black_sum

  elif feature_type == "horizontal_line":
    white_sum1 = get_sum(integral, row, col, row + height // 3 -1, col + width -1)
    black_sum = get_sum(integral, row + height // 3, col, row + 2*height // 3 - 1, col + width - 1)
    white_sum2  = get_sum(integral, row + 2*height // 3, col, row + height - 1, col + width - 1)
    return white_sum1 + white_sum2 - black_sum

  elif feature_type == "vertical_line":
    white_sum1 = get_sum(integral, row, col, row + height -1, col + width // 3 - 1)
    black_sum = get_sum(integral, row, col + width // 3, row + height - 1, col + 2*width // 3 - 1)
    white_sum2  = get_sum(integral, row, col + 2*width // 3, row + height - 1, col + width - 1)
    return (white_sum1 + white_sum2) - black_sum

  elif feature_type == "checkerboard":
    white_sum1 = get_sum(integral, row, col, row + height//2 - 1, col + width//2 - 1)
    black_sum1 = get_sum(integral, row, col + width//2, row + height//2 - 1, col + width - 1)
    black_sum2 = get_sum(integral, row + height//2, col, row + height - 1, col + width//2 - 1)
    white_sum2  = get_sum(integral, row + height//2, col + width//2, row + height - 1, col + width - 1)
    return (white_sum1 + white_sum2) - (black_sum1 + black_sum2)  
  # else:
  #   return ValueError("Unknown feature type") 
  
  # return feature_value



'''
creates list of all posible haar like featur position and size => used later for feature extraction
precompute them at once instead of again and again

window_size = 24, step = 3 => default parameters
'''
def precompute_feature(window_size = 24, step = 3): 
  # creating list of tuples containing (feature_name, min_height, min_width)
  feature_type = [
    ("horizontal_edge", 2, 1),
    ("vertical_edge", 1, 2),
    ("horizontal_line", 3, 1),
    ("vertical_line", 1, 3),
    ("checkerboard", 2, 2)
  ]
  # rows, cols = self.img.gray.shape

  all_features = [] # empty list => to store all posible features 

  for f_type, min_h, min_w in feature_type:         # loops throug each features in feature_type list
    for h in range(min_h, window_size+1, min_h):    # loops throug all possible height(h) of feature => starting with min till window size 
      for w in range(min_w, window_size+1, min_w):  # loops throug all possible width(w) of feature

        # if h > rows or w > cols:
        #   continue
        
        # For sliding window 
        for r in range(0, window_size - h + 1, step):     # window_size - h + 1 => so that sliding window doesnt go out of bound
          for c in range(0, window_size - w + 1, step):   # window_size - w + 1 => so that sliding window doesnt go out of bound
            all_features.append((f_type,r,c,h,w))         # stores the features tpe , position and size in all_features as tuple

  print(f"Total features precomputed: {len(all_features)}")
  return all_features   # returnss all_feature list => [('horizontal_edge', 0,0,2,1),('horizontal_edge', 0,3,2,1)....]
  

# extract feature matrix
'''
Take dataset(X) and list of all_features from precompute_feature()
then compute integral image for each
and extract haarlike feature
'''
def extract_features(X, feature_list):
  num_samples = X.shape[0]            # total no. of sample in dataset
  num_features = len(feature_list)    # no. of features precomputed
  feature_matrix = np.zeros((num_samples, num_features), dtype=np.float32) # create matrix of zeros 

  '''
  for each img in X 
  take one img
  compute its integral  # we use integral image for fast haar calc 
  '''
  for i in range(num_samples):
    img = X[i]
    integral = compute_integral_image(img)
    '''
    for each feature ko detail => (feature_type, position, size)
    call haarlike_feature() => which reaturns feature_value
    store it in feature_matrix[i, j]
    '''
    for j, feat in enumerate(feature_list):
      f_type, r, c, h, w = feat
      feature_matrix[i, j] = haarlike_feature(integral, f_type, r, c, h, w)

  return feature_matrix # return feature_matix => 

# extack feature Batchwise for faster computation for larger dataset
'''
instead of processing all samples at once we process it in batchs(batch of 200: 0-199, 200-399, ...) => so that the memory is reused => so that it doesnt crash 
'''
def extract_features_batchwise(X, feature_list, batch_size=200):
  num_samples = X.shape[0]            # total no. of sample in dataset
  num_features = len(feature_list)    # no. of features precomputed
  feature_matrix = np.zeros((num_samples, num_features), dtype=np.float32) # create matrix of zeros 

  for start in range(0, num_samples, batch_size):
    end = min(start + batch_size, num_samples) 
    print(f"Processing batch from {start} to {end-1}...") 
    for i in range(start, end):
      img = X[i]
      integral = compute_integral_image(img)
      '''
      for each feature ko detail => (feature_type, position, size)
      call haarlike_feature() => which reaturns feature_value
      store it in feature_matrix[i, j]
      '''
      for j, feat in enumerate(feature_list):
        f_type, r, c, h, w = feat
        feature_matrix[i, j] = haarlike_feature(integral, f_type, r, c, h, w)

  return feature_matrix


if __name__ == "__main__": # ensures file only runs when code executed => not when importing modules!!!
  X = np.load("./aug_dataset/X.npy") # load X.npy
  print(f"Loaded dataset: {X.shape}") # print its shape

  feature_list = precompute_feature(window_size=24, step=6)  # step=3 is very slow so calles with 6 steps 
  start = time.time()
  # features = extract_features(X, feature_list) # 
  features = extract_features_batchwise(X, feature_list, batch_size=200) #  
  end = time.time()

  print(f"Feature matrix shape: {features.shape}")
  print(f"Extraction took {end-start:.2f} sec")

  # save as .npy file 
  np.save("./aug_dataset/features.npy", features)
  np.save("./aug_dataset/feature_list.npy", feature_list)
  print("Saved features.npy and feature_list.npy")

