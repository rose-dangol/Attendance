# detect.py
import os
import numpy as np
from matplotlib import image as mpimg
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.ndimage import zoom
from haarlike_feature import compute_integral_image, haarlike_feature

# -------------------------
# Helpers: load saved objects
# -------------------------
# def load_feature_list(path="./aug_dataset/feature_list.npy"):
#     data = np.load(path, allow_pickle=True)
#     # ensure it's a python list of tuples
#     if isinstance(data, np.ndarray):
#         try:
#             data = data.tolist()
#         except:
#             pass
#     return data
def load_feature_list(path="./aug_dataset/feature_list.npy"):
    data = np.load(path, allow_pickle=True)
    # convert each element to proper type
    proper_data = []
    for feat in data:
        f_type = feat[0]  # already string
        r = int(feat[1])
        c = int(feat[2])
        h = int(feat[3])
        w = int(feat[4])
        proper_data.append((f_type, r, c, h, w))
    return proper_data

def load_cascade(classifier_dir="./classifiers"):
    # load all files matching "*_classifier.npy" sorted by name
    if not os.path.exists(classifier_dir):
        raise FileNotFoundError(f"{classifier_dir} not found.")
    files = sorted([f for f in os.listdir(classifier_dir) if f.endswith("_classifier.npy")])
    cascade = []
    for f in files:
        arr = np.load(os.path.join(classifier_dir, f), allow_pickle=True)
        # convert numpy-object to python list if needed
        if isinstance(arr, np.ndarray):
            try:
                arr = arr.tolist()
            except:
                pass
        cascade.append(arr)
    if not cascade:
        raise ValueError("No classifier files found in classifiers folder.")
    return cascade

# -------------------------
# Prediction utilities
# -------------------------
def predict_stage_from_feature_vector(feature_vector, weak_classifiers):
    """Return (passed_bool, stage_score) for a single stage (weak_classifiers=list)."""
    score = 0.0
    for wl in weak_classifiers:
        fidx = wl["feature_idx"]
        thresh = wl["threshold"]
        pol = wl["polarity"]
        alpha = wl["alpha"]
        fv = feature_vector[fidx]
        pred = 1 if (pol * fv >= pol * thresh) else 0
        score += alpha * (2 * pred - 1)   # convert pred {0,1} to {-1,+1}
    return (score >= 0), score

def predict_cascade(feature_vector, cascade):
    """Apply cascade stages sequentially. Return (passed_bool, final_score)."""
    final_score = 0.0
    for stage in cascade:
        passed, stage_score = predict_stage_from_feature_vector(feature_vector, stage)
        if not passed:
            return False, stage_score  # rejected by this stage
        final_score = stage_score    # update final score (keep last stage score)
    return True, final_score

# -------------------------
# Feature extraction for one window
# -------------------------
def window_feature_vector(integral, feature_list, top, left):
    """
    Compute Haar features (vector) for a specific 24x24 window whose top-left is (top,left)
    relative to the integral image.
    """
    fv = np.zeros(len(feature_list), dtype=np.float32)
    for j, feat in enumerate(feature_list):
        f_type, r, c, h, w = feat
        # absolute coordinates inside the image
        row = int(top + r)
        col = int(left + c)
        fv[j] = haarlike_feature(integral, f_type, row, col, h, w)
    return fv

# -------------------------
# Sliding window + pyramid
# -------------------------
def scan_scaled_image(scaled_gray, scale, cascade, feature_list, window_size=(24,24), step=6, max_features=None):
    """
    Scan one scaled (grayscale) image and return detections mapped to original image coords.
    scale = scaled_image_size / original_image_size (zoom factor used on original).
    Return list of boxes: (x1,y1,x2,y2,score)
    """
    h, w = scaled_gray.shape
    win_h, win_w = window_size
    detections = []
    integral = compute_integral_image(scaled_gray)

    # optional reduce number of features considered for speed (None => use all)
    use_features = feature_list if max_features is None else feature_list[:max_features]

    for top in range(0, h - win_h + 1, step):
        for left in range(0, w - win_w + 1, step):
            fv = window_feature_vector(integral, use_features, top, left)
            passed, score = predict_cascade(fv, cascade)
            if passed:
                # map scaled coords back to original image coordinates
                x1 = int(left / scale)
                y1 = int(top / scale)
                x2 = int((left + win_w) / scale)
                y2 = int((top + win_h) / scale)
                detections.append((x1, y1, x2, y2, float(score)))
    return detections

def image_pyramid_detections(gray_image, cascade, feature_list, scale_step=0.8, step=6, min_size=(24,24), max_features=None):
    """
    Build image pyramid by shrinking the image repeatedly by scale_step (<1).
    Returns list of all detections across scales.
    """
    detections = []
    orig_h, orig_w = gray_image.shape
    scale = 1.0
    while True:
        scaled_h = int(orig_h * scale)
        scaled_w = int(orig_w * scale)
        if scaled_h < min_size[0] or scaled_w < min_size[1]:
            break
        # resize using zoom (scale < 1 shrinks)
        scaled = zoom(gray_image, (scale, scale), order=1)
        dets = scan_scaled_image(scaled, scale, cascade, feature_list, window_size=min_size, step=step, max_features=max_features)
        detections.extend(dets)
        scale *= scale_step
    return detections

# -------------------------
# Non-Maximum Suppression (NMS)
# -------------------------
def non_max_suppression(boxes, iou_thresh=0.3):
    """
    boxes: list of (x1,y1,x2,y2,score)
    returns filtered boxes after NMS
    """
    if not boxes:
        return []
    arr = np.array(boxes)
    x1 = arr[:,0].astype(float)
    y1 = arr[:,1].astype(float)
    x2 = arr[:,2].astype(float)
    y2 = arr[:,3].astype(float)
    scores = arr[:,4].astype(float)

    areas = (x2 - x1) * (y2 - y1)
    order = scores.argsort()[::-1]  # descending scores
    keep = []

    while order.size > 0:
        i = order[0]
        keep.append(i)
        if order.size == 1:
            break
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1)
        h = np.maximum(0.0, yy2 - yy1)
        inter = w * h
        iou = inter / (areas[i] + areas[order[1:]] - inter + 1e-10)

        inds = np.where(iou <= iou_thresh)[0]
        order = order[inds + 1]  # +1 because inds indexes order[1:]
    return arr[keep].tolist()

# -------------------------
# Drawing results
# -------------------------
def draw_and_save(image, boxes, out_path=None):
    fig, ax = plt.subplots(1, figsize=(10, 8))
    ax.imshow(image, cmap="gray")
    for (x1,y1,x2,y2,score) in boxes:
        w = x2 - x1
        h = y2 - y1
        rect = patches.Rectangle((x1, y1), w, h, linewidth=2, edgecolor='red', facecolor='none')
        ax.add_patch(rect)
        ax.text(x1, max(0,y1-6), f"{score:.2f}", color='y', fontsize=8, weight='bold')
    plt.axis('off')
    if out_path:
        plt.savefig(out_path, bbox_inches='tight', pad_inches=0)
    else:
        plt.show()
    plt.close(fig)

# -------------------------
# Utilities: grayscale conversion
# -------------------------
def to_gray(img):
    # img from mpimg can be float [0,1] or uint8 [0,255] or already grayscale
    if img.ndim == 3:
        img = img.astype(np.float32)
        if img.max() > 1.0:
            img = img / 255.0
        return img[:,:,0]*0.299 + img[:,:,1]*0.587 + img[:,:,2]*0.114
    else:
        img = img.astype(np.float32)
        if img.max() > 1.0:
            img = img / 255.0
        return img

# -------------------------
# Main CLI
# -------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Viola-Jones style detection (lightweight).")
    parser.add_argument("image", help="Input image path")
    parser.add_argument("--classifiers", default="./classifiers", help="Classifiers folder")
    parser.add_argument("--feature_list", default="./aug_dataset/feature_list.npy", help="Feature list file")
    parser.add_argument("--out", default="./results/detected.png", help="Output image path")
    parser.add_argument("--step", type=int, default=6, help="Sliding window stride (pixels)")
    parser.add_argument("--scale_step", type=float, default=0.8, help="Pyramid shrink factor (<1)")
    parser.add_argument("--nms_iou", type=float, default=0.3, help="NMS IoU threshold")
    parser.add_argument("--max_features", type=int, default=None, help="Optional: use only first N features for speed")
    args = parser.parse_args()

    img = mpimg.imread(args.image)
    gray = to_gray(img)
    feature_list = load_feature_list(args.feature_list)
    print(feature_list[:5]) #
    cascade = load_cascade(args.classifiers)

    detections = image_pyramid_detections(gray, cascade, feature_list,
                                          scale_step=args.scale_step, step=args.step,
                                          min_size=(24,24), max_features=args.max_features)
    final = non_max_suppression(detections, iou_thresh=args.nms_iou)
    # ensure results folder exists
    # os.makedirs(os.path.dirname(args.out), exist_ok=True)
    out_dir = os.path.abspath(os.path.dirname(args.out))
    os.makedirs(out_dir, exist_ok=True)
    draw_and_save(img, final, out_path=args.out)
    print(f"Detections: {len(final)} boxes saved to {args.out}")
