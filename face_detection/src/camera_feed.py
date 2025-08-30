# for i in range(3):
#     cap = cv2.VideoCapture(i)
#     ret, frame = cap.read()
#     print(f"Camera {i} open? {ret}")
#     cap.release()

import cv2

# cap = cv2.VideoCapture(0)


for i in range(3):
    cap = cv2.VideoCapture(i)
    ret, frame = cap.read()
    print(f"Camera {i} open? {ret}")
    cap.release()


while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("Test Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
