import numpy as np

def compute_lbp(gray_img):
    h, w = gray_img.shape
    lbp_img = np.zeros((h, w), dtype=np.uint8)

    for i in range(1, h - 1):
        for j in range(1, w - 1):
            center = gray_img[i, j]
            binary = 0
            binary |= (gray_img[i-1, j-1] >= center) << 7
            binary |= (gray_img[i-1, j]   >= center) << 6
            binary |= (gray_img[i-1, j+1] >= center) << 5
            binary |= (gray_img[i,   j+1] >= center) << 4
            binary |= (gray_img[i+1, j+1] >= center) << 3
            binary |= (gray_img[i+1, j]   >= center) << 2
            binary |= (gray_img[i+1, j-1] >= center) << 1
            binary |= (gray_img[i,   j-1] >= center) << 0
            lbp_img[i, j] = binary

    return lbp_img
