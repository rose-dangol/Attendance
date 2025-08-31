import cv2
from recognize import recognize_face

def distance_to_accuracy(dist, scale=2.0):
    acc = max(0, 100 - dist * scale)
    return round(acc, 2)

def main():
    cap = cv2.VideoCapture(0)
    print("🔵 Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = cv2.resize(gray, (64, 64))

        name, dist = recognize_face(face)
        accuracy = distance_to_accuracy(dist)

        cv2.putText(frame, f"{name} ({accuracy}%)", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Face Attendance", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
