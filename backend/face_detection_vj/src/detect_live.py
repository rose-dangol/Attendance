import cv2
import numpy as np
from haarlike_feature import compute_integral_image, haarlike_feature
from detect import to_gray, load_feature_list, load_cascade, image_pyramid_detections, non_max_suppression, draw_and_save

# Load cascade and features
feature_list = load_feature_list("./aug_dataset/feature_list.npy")
cascade = load_cascade("./classifiers")

# Open webcam
cap = cv2.VideoCapture(0)  # 0 = default camera

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = to_gray(frame)

    # Run detection
    detections = image_pyramid_detections(gray, cascade, feature_list,
                                          scale_step=0.8, step=6, min_size=(24,24), max_features=500)
    final = non_max_suppression(detections, iou_thresh=0.3)

    # Draw boxes
    # error
    # for (x1, y1, x2, y2, score) in final:
    #     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
    #     cv2.putText(frame, f"{score:.2f}", (x1, max(0, y1-5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 1)

    if not final:
        continue  # skip to next frame if no detections

    # Draw boxes
    for det in final:
      x1, y1, x2, y2, score = det
      # convert floats to integers
      x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
      cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
      cv2.putText(frame, f"{score:.2f}", (x1, max(0, y1-6)),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)


    cv2.imshow("Face Detection", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
