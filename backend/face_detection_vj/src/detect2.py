"""
detect.py
Lightweight Viola-Jones inference (sliding window + cascade + NMS).
Dependencies: numpy, matplotlib, scipy.ndimage, haarlike_features.py (your module).
Run:
    python detect.py --input test_images/sample1.jpg --out results/sample1_detected.png
"""

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from scipy.ndimage import zoom
from haarlike_feature import haarlike_feature, compute_integral_image, precompute_feature

# -----------------------
# Helper utilities
# -----------------------
def load_numpy_obj(path):
    """Load a .npy file that may contain Python objects (use allow_pickle). Return Python object."""
    obj = np.load(path, allow_pickle=True)
    try:
        return obj.tolist()
    except Exception:
        return obj

def load_cascade(classifier_dir="./classifiers"):
    """Load all stageX_classifier.npy files sorted by stage number."""
    stages = []
    if not os.path.exists(classifier_dir):
        raise FileNotFoundError(f"Classifier folder not found: {classifier_dir}")
    files = sorted([f for f in os.listdir(classifier_dir) if f.startswith("stage") and f.endswith("_classifier.npy")])
    if not files:
        raise FileNotFoundError(f"No stage classifiers found in {classifier_dir}")
    for f in files:
        path = os.path.join(classifier_dir, f)
        stages.append(load_numpy_obj(path))
    return stages

def image_to_gray_float(img):
    """Convert image to grayscale float32 with pixel range [0,1]. Accepts RGB or grayscale."""
    img = img.astype(np.float32)
    if img.max() > 1.0:
        img = img / 255.0
    if img.ndim == 3:
        # RGB to luminance grayscale
        return img[:, :, 0]*0.299 + img[:, :, 1]*0.587 + img[:, :, 2]*0.114
    return img

# -----------------------
# Cascade evaluation on integral image
# -----------------------
def eval_strong_on_window(integral, top, left, weak_classifiers, feature_list):
    """
    Evaluate a strong classifier (list of weak classifiers) on the window positioned at (top,left)
    using the integral image of the whole (resized) image. We compute each weak classifier's
    feature value on demand (no full feature vector).
    Returns: (is_face_bool, score_float) where score is the weighted sum.
    """
    score = 0.0
    for wl in weak_classifiers:
        # each wl: dict with keys 'feature_idx','threshold','polarity','alpha'
        feat = feature_list[wl["feature_idx"]]  # (f_type, r, c, h, w)
        f_type, r, c, h, w = feat
        # feature coordinates are relative to the 24x24 window. Add window offset.
        row = int(top + r)
        col = int(left + c)
        # compute Haar-like feature value using integral of entire resized image
        fv = haarlike_feature(integral, f_type, row, col, h, w)
        # weak prediction (0 or 1)
        pred = 1 if (wl["polarity"] * fv >= wl["polarity"] * wl["threshold"]) else 0
        score += wl["alpha"] * (2*pred - 1)  # +alpha for pred==1, -alpha for pred==0
    return (score >= 0), score  # boolean decision, raw score

# -----------------------
# Non-Maximum Suppression (NMS)
# -----------------------
def iou(boxA, boxB):
    # boxes as (x, y, w, h)
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[0] + boxA[2], boxB[0] + boxB[2])
    yB = min(boxA[1] + boxA[3], boxB[1] + boxB[3])
    interW = max(0, xB - xA)
    interH = max(0, yB - yA)
    interArea = interW * interH
    areaA = boxA[2] * boxA[3]
    areaB = boxB[2] * boxB[3]
    union = areaA + areaB - interArea
    if union == 0:
        return 0
    return interArea / union

def non_max_suppression(boxes, scores, iou_thresh=0.3):
    """
    boxes: list of (x,y,w,h)
    scores: list of floats (same length)
    Returns filtered boxes + scores after NMS.
    """
    if len(boxes) == 0:
        return [], []
    idxs = np.argsort(scores)[::-1]  # sort by score desc
    keep = []
    while len(idxs) > 0:
        current = idxs[0]
        keep.append(current)
        rest = idxs[1:]
        suppressed = []
        for i in rest:
            if iou(boxes[current], boxes[i]) > iou_thresh:
                suppressed.append(i)
        idxs = np.array([i for i in rest if i not in suppressed])
    kept_boxes = [boxes[i] for i in keep]
    kept_scores = [scores[i] for i in keep]
    return kept_boxes, kept_scores

# -----------------------
# Detection pipeline
# -----------------------
def detect_faces_in_image(img_orig,
                          cascade_stages,
                          feature_list,
                          window_size=24,
                          scale_step=1.25,
                          stride=4,
                          min_scale_factor=1.0,
                          verbose=True):
    """
    img_orig: original RGB or grayscale image (numpy array)
    cascade_stages: list of stage weak_classifiers (each is list of dicts)
    feature_list: list of features (tuples) computed for 24x24 window
    Returns: list of detections in original image coords: (x, y, w, h, score)
    """
    img_gray = image_to_gray_float(img_orig)
    orig_h, orig_w = img_gray.shape
    detections = []

    scale = 1.0
    # Keep generating smaller versions of original image (pyramid) until smaller than window
    while True:
        # zoom_factor to resize original down by 'scale'
        zoom_factor = 1.0 / scale
        # produce resized image for this pyramid level
        resized = zoom(img_gray, (zoom_factor, zoom_factor), order=1) if scale != 1.0 else img_gray
        rh, rw = resized.shape
        if rh < window_size or rw < window_size:
            break

        # integral image for resized image (used to compute Haar features quickly)
        integral_full = compute_integral_image(resized)

        # sliding window over resized image
        for top in range(0, rh - window_size + 1, stride):
            for left in range(0, rw - window_size + 1, stride):
                # Fast cascade evaluation: stage by stage
                passed_all = True
                final_score = None
                for stage_idx, stage_wl in enumerate(cascade_stages):
                    passed, score = eval_strong_on_window(integral_full, top, left, stage_wl, feature_list)
                    if not passed:
                        passed_all = False
                        break
                    final_score = score  # last stage score
                if passed_all:
                    # map coords back to original image scale
                    x_orig = int(np.round(left * scale))
                    y_orig = int(np.round(top * scale))
                    w_orig = int(np.round(window_size * scale))
                    h_orig = int(np.round(window_size * scale))
                    detections.append((x_orig, y_orig, w_orig, h_orig, float(final_score if final_score is not None else 0.0)))
        # go to next scale
        scale *= scale_step

    # apply NMS on collected detections
    if len(detections) == 0:
        return []
    boxes = [(d[0], d[1], d[2], d[3]) for d in detections]
    scores = [d[4] for d in detections]
    kept_boxes, kept_scores = non_max_suppression(boxes, scores, iou_thresh=0.3)
    result = [(b[0], b[1], b[2], b[3], s) for b, s in zip(kept_boxes, kept_scores)]
    return result

# -----------------------
# Visualization + CLI
# -----------------------
def draw_and_save_detections(img_path, detections, out_path):
    img = mpimg.imread(img_path)
    fig, ax = plt.subplots(1)
    ax.imshow(img, interpolation="nearest")
    for (x, y, w, h, score) in detections:
        rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        ax.text(x, y-6, f"{score:.2f}", color='yellow', fontsize=8, bbox=dict(facecolor='black', alpha=0.4))
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close(fig)

def main():
    parser = argparse.ArgumentParser(description="Viola-Jones style face detector (lightweight).")
    parser.add_argument("--input", required=True, help="Input image path")
    parser.add_argument("--out", required=False, default=None, help="Output image path (with boxes).")
    parser.add_argument("--stride", type=int, default=4, help="Sliding window stride in pixels.")
    parser.add_argument("--scale", type=float, default=1.25, help="Pyramid scale step (e.g., 1.25).")
    parser.add_argument("--nms", type=float, default=0.3, help="NMS IoU threshold.")
    args = parser.parse_args()

    img_path = args.input
    out_path = args.out if args.out else ("results/" + os.path.basename(img_path).rsplit('.',1)[0] + "_detected.png")
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    # load cascade & features
    cascade = load_cascade("./classifiers")
    # load feature_list if exists, else precompute (step=3 or 6 depending on speed)
    if os.path.exists("./aug_dataset/feature_list.npy"):
        feature_list = load_numpy_obj("./aug_dataset/feature_list.npy")
    else:
        feature_list = precompute_feature(window_size=24, step=3)

    # ensure these are Python lists (not numpy object arrays)
    if hasattr(feature_list, "tolist"):
        feature_list = feature_list.tolist()
    cascade = [stage.tolist() if hasattr(stage, "tolist") else stage for stage in cascade]

    # read image
    img = mpimg.imread(img_path)

    # detection
    detections = detect_faces_in_image(img,
                                       cascade_stages=cascade,
                                       feature_list=feature_list,
                                       window_size=24,
                                       scale_step=args.scale,
                                       stride=args.stride)
    print(f"Detections (after NMS): {len(detections)}")
    for d in detections:
        print(f"  x={d[0]} y={d[1]} w={d[2]} h={d[3]} score={d[4]:.4f}")

    # draw & save
    draw_and_save_detections(img_path, detections, out_path)
    print(f"Saved output to {out_path}")

if __name__ == "__main__":
    main()
