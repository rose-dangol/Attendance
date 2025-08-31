import cv2
import numpy as np
from lbp.lbp import compute_lbp
from lbp.histogram import lbph_features

def recognize_face(test_img):
    database = np.load("models/lbph_database.npy", allow_pickle=True)
    test_img = cv2.resize(test_img, (64, 64))
    lbp_test = compute_lbp(test_img)
    test_feat = lbph_features(lbp_test)

    min_dist = float("inf")
    predicted_label = "Unknown"

    for label, db_feat in database:
        dist = np.linalg.norm(test_feat - db_feat)
        if dist < min_dist:
            min_dist = dist
            predicted_label = label

    return predicted_label, min_dist
