import numpy as np
from dataset import ImageDataset


# Create obj for faces
face_dataset = ImageDataset("./dataset_test/faces", "./aug_dataset/aug_faces" )

face_dataset.load_images()
face_dataset.set_output_dir()

face_dataset.augment_images()
face_dataset.save_as_npy("./aug_dataset/faces_aug.npy")

# labels for faces
faces = np.load("./aug_dataset/faces_aug.npy")
labels_faces = np.ones(len(faces), dtype=np.int32)

np.save("./aug_dataset/face_sample.npy", faces)
np.save("./aug_dataset/face_lable.npy", labels_faces)
print("Positive samples saved as face_sample.npy and labels as face_lable.npy")



# Prepare no faces
# Create obj for no faces
noface_dataset = ImageDataset("./dataset_test/no_faces", "./aug_dataset/patches_nofaces")

noface_dataset.load_images()
noface_dataset.set_output_dir()

noface_dataset.extract_negative_patches()
noface_dataset.save_as_npy("./aug_dataset/nofaces_patches.npy")

# labels for no faces
nofaces = np.load("./aug_dataset/nofaces_patches.npy")
labels_nofaces = np.zeros(len(nofaces), dtype=np.int32)

np.save("./aug_dataset/noface_patchsample.npy", nofaces)
np.save("./aug_dataset/noface_lable.npy", labels_nofaces)
print("Negative samples saved as noface_patchsample.npy and labels as noface_lable.npy")




# Combine and shuffle data

# load +ve sample
X_faces = np.load("./aug_dataset/face_sample.npy")
y_faces = np.load("./aug_dataset/face_lable.npy")

# load -ve sample
X_nofaces = np.load("./aug_dataset/noface_patchsample.npy")
y_nofaces = np.load("./aug_dataset/noface_lable.npy")

print("Faces:", X_faces.shape, y_faces.shape)
print("No Faces:", X_nofaces.shape, y_nofaces.shape)


# combine features
X = np.concatenate([X_faces, X_nofaces], axis=0) # Faces: (15, 24, 24) (15,)
# combine labels
y = np.concatenate([y_faces,y_nofaces], axis=0) # No Faces: (40, 24, 24) (40,)

print("Combined X(features) shape:", X.shape) # Combined X(features) shape: (55, 24, 24) 
print("Combined y(labels) shape:", y.shape) # Combined y(labels) shape: (55,)

# (55,) means 1D array of 55 elements =>[1,1,1,1....]  eg:
# arr = np.array([1,2,3])
# print(arr.shape) # (3,)

# 
indeces = np.arange(len(X)) # np.arange => similar to range
np.random.shuffle(indeces) # ramdomly shuffle/reorder the elements in indeces
# it modifies the original array i.e indeces => doesnt give a new one so no need of var for it 

# index anusar X and y ni shuffle
X = X[indeces]
y = y[indeces]

print("After shuffle:", X.shape, y.shape)

# save combined(faces and no faces) and shuffled features and lables
np.save("./aug_dataset/X.npy", X)
np.save("./aug_dataset/y.npy", y)
print("Final dataset saved as X.npy and y.npy")




