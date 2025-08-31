import os
import numpy as np
from matplotlib import image as mpimg
from scipy.ndimage import rotate, zoom
# from image_data import ImageData

# class FaceDataset:
class ImageDataset:
  # class att => shared by all objs 
  # image_size = 24

  def __init__(self, input_dir, output_dir):
    self.input_dir = input_dir
    self.output_dir = output_dir
    self.images = []

  # load image
  def load_images(self):
    # loads all img from input_dir and stores in self.images
    for file in os.listdir(self.input_dir):
      if file.lower().endswith((".jpg", ".png", ".jpeg")):
        path = os.path.join(self.input_dir, file)
        img = mpimg.imread(path).astype(np.float32) # astype=> changes datatype 
                                                    #always convt loaded image to float32 => but doesnt normalize to [0,1]  

        ''' # convt to float32 betn 0 and 1
        if img.dtype == np.uint32:
          img = img.astype(np.float32)/255.0  
        '''# normalize only if image originally uint32 but we already convt to float32 above so this line no use

        # normalize
        if img.max() > 1.0:
          img /= 255.0

        # rbg to grayscale
        gray =  (
          img[:,:,0] * 0.299  +   # Red
          img[:,:,1] * 0.587 +    # Green
          img[:,:,2] * 0.114      # Blue
        )
        # self.images.append(img) # no cause stores the whole image in images  butt we need to...
        # store as tuple (filname_without_ext, image) => so that we pass the actual filename and not the image araay when saving augmented images
        '''filename = os.path.splitext(file)[0] ''' 
        # .splitext(file) => splits file into file name and extension and returns as tuple ('filename', '.ext')
        # [0] => takes element is first position => filename
        # [1] => takes element in 2nd position => .ext
         
        self.images.append((file.split(".")[0], gray))


    print(f"Loaded {len(self.images)} images from {self.input_dir}")
  
  # make folder to store aug and patched img if not already exist 
  def set_output_dir(self):
    if not os.path.exists(self.output_dir):
      os.makedirs(self.output_dir)
    print(f"Output directry set to: {self.output_dir}")

  # # rbg to grayscale
  # def rgb_to_gray(self, image):
  #   # luminance formula
  #   return (
  #     image[:,:,0] * 0.299  +   # Red
  #     image[:,:,1] * 0.587 +    # Green
  #     image[:,:,2] * 0.114      # Blue
  #   )

  # resize to 24X24
  def resize_faces(self, image, target_size=(24,24)):
      
      # using Nearest neighbour milexaina....
      '''
      # target_h, target_w = image.shape
      # src_h, src_w = image.shape[:2]

      # resized = np.zeros((target_h, target_w,3))
      # for i in range(target_h):
      #   for j in range(target_w):
      #     y = int(i * src_h/target_h)
      #     x = int(j * src_w/target_w)
      #     resized[i,j] = image[y,x]
      # return resized
      '''
      # using bilinear interpolation
      h, w = image.shape[:2]
      zoom_factors = (target_size[0]/h, target_size[1]/w)
      return zoom(image,zoom_factors, order=1)
  
  # brightness adjust
  def brightness_adjust(self, image,factor):
    # normalize to 0-1
    # if image.dtype == np.uint8:
    #   image = image.astype(np.float32) / 255.0
    # or
    # if image.max() > 1.0:
    #   image = image / 255.0
    # not doing these in load_images() not here 

    return np.clip(image*factor, 0, 1)  # multiply image brightmness by factor and clip to [0, 1] ???

  # randon rotate +-10 degree
  def random_rotate(self, image, angle=(-10,10)):
    angle = np.random.uniform(*angle)
    return rotate(image, angle, reshape=False)

  # augment for faces
  def augment_images(self):
    augmented = []

    for filename, gray in self.images:
    # for img_obj in self.images:   # for image obj of ImageData
      # gray = self.rgb_to_gray(img)
      # gray = img_obj.gray 
      # why img_obj.gray or img_obj.filename not self.gray or self.filename => cause self points to current obj of class we are in but here we need to get the gray and filename attribute inside Imagedata 
      # filename = img_obj.filename 

      # normalize to 0-1
      # if gray.max() > 1.0:
      #   gray = gray / 255.0

      resized = self.resize_faces(gray)

          
      # save imag to aug_faces folder
      mpimg.imsave(os.path.join(self.output_dir,f"{filename}_orig.png"),resized, cmap="gray")                                        # original img save
      mpimg.imsave(os.path.join(self.output_dir,f"{filename}_flip.png"),np.fliplr(resized), cmap="gray")                             # horizontal flip
      mpimg.imsave(os.path.join(self.output_dir,f"{filename}_bright.png"),self.brightness_adjust(resized, 1.5), cmap="gray")         # brightness adjust to bright
      mpimg.imsave(os.path.join(self.output_dir,f"{filename}_dark.png"),self.brightness_adjust(resized, 0.8), cmap="gray")           # brightness adjust to bright
      mpimg.imsave(os.path.join(self.output_dir,f"{filename}_rotate.png"),self.random_rotate(resized,angle = (-10,10)), cmap="gray") # Ramdom rotation

      # store in empty list augmented 
      '''
      augmented.append(resized)
      augmented.append(np.fliplr(resized))
      augmented.append(self.brightness_adjust(resized, 1.5))
      augmented.append(self.brightness_adjust(resized, 0.8))
      augmented.append(self.random_rotate(resized))
      '''
      # append adds something as a single element to a list
      # eg: append([a,b]) => adds [a,b] as a single ele to supppose [c,d,[a,b]]
      # extends adds each elements inside the list individually 
      # eg: extend([a,b,c]) => adds each ele a,b,c individually to list => [d, a, b,c]
      # does the same thing as above just not write append multiple times
      augmented.extend([
        resized,
        np.fliplr(resized),
        self.brightness_adjust(resized, 1.5),
        self.brightness_adjust(resized, 0.8),
        self.random_rotate(resized)
      ])

    # store all augmented images in empty list images 
    self.images = augmented
    print(f"Augmented {len(self.images)} images.")

  # extract patches from no face images
  def extract_negative_patches(self, patch_size=24, patch_per_img=10):
    patches = []
    for filename, gray in self.images:
      h, w = gray.shape
      for i in range(patch_per_img): # _ -> doesnt matter what we call temp var 

        x = np.random.randint(0, w - patch_size +1) 
        y = np.random.randint(0, h - patch_size +1)
        # +1 => cause n = np.random.randint(low,high) => n must be >= low and < high   => so if w = 50 => 50-24=26 => n = (0, 26) => therefor n = 25 possible for random no. which looses 1 valid position so +1

        # array slicing in numpy to extract subimage(patch) from large img
        # to get/access a region => slice rows(y-axis) and cols(x axis)     => slice = ech to extract specific portion/subset of numpy array
        # gray[start_rw : end_rw, start_col : end_col]
        patch = gray[y:y+patch_size, x:x+patch_size]

        # add to list
        patches.append(patch)

        # save patches of image to patches_noface folder
        mpimg.imsave(os.path.join(self.output_dir,f"{filename}_patch_{i}.png"),patch, cmap="gray") 
        # {_} => _ => var => if i instead of _ then {i} => cause it shoud save each patch => if not put the empty only dir         

    self.images = patches

  # save as .npy file
  def save_as_npy(self, file_path):
    # convert list to numpy array
    images_array = np.array(self.images, dtype=np.float32) # store as 32 bit float to save memory

    # cliping to [0,1] before saving to .npy file for safety => so that min pixel value is not in -0...something saused bybileanear interrpolation => voila jones doesn really care about this but if we have to use same dataset for suppose CNN then it will effect???
    images_array = np.clip(images_array, 0.0, 1.0) 

    # save to .npy file => cause fast compress & easy to load
    np.save(file_path, images_array)

    print(f"{images_array.shape[0]} images saved to {file_path}.")








