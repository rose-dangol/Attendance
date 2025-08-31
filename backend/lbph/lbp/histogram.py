import numpy as np

def lbph_features(lbp_image, grid_x=8, grid_y=8):
    h, w = lbp_image.shape
    grid_h = h // grid_y
    grid_w = w // grid_x
    features = []

    for y in range(grid_y):
        for x in range(grid_x):
            cell = lbp_image[y*grid_h:(y+1)*grid_h, x*grid_w:(x+1)*grid_w]
            hist, _ = np.histogram(cell.ravel(), bins=256, range=(0, 256))
            hist = hist.astype("float")
            hist /= (hist.sum() + 1e-6)
            features.extend(hist)

    return np.array(features)
