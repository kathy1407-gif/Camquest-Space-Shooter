import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python import BaseOptions
import requests
import socket

# ---------- UDP SETUP ----------
UDP_IP = "127.0.0.1"
UDP_PORT = 25001
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# --------------------------------

def detect_hand_data(frame, hands):
    pass
    # add your right and left hand detection code here

def run_detection():
    model_path = "hand_landmarker.task"

    options = vision.HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        num_hands=2, #Because we want to detect both hands
        min_hand_detection_confidence=0.7,
        min_hand_presence_confidence=0.7,
        min_tracking_confidence=0.5
    )

    hands = vision.HandLandmarker.create_from_options(options)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # data = detect_hand_data(frame, hands)
        frame = cv2.flip(frame, 1)

        #if data:
        #    message = f" choose a format based on data, same will be used in unity "
        #    sock.sendto(message.encode("utf-8"), (UDP_IP, UDP_PORT))

        #    cv2.putText(frame, message, (20, 40),
        #                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        cv2.imshow("Hand Tracking", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    sock.close()
    cv2.destroyAllWindows()


# Download model if missing
url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
r = requests.get(url)
open("hand_landmarker.task", "wb").write(r.content)

run_detection()
