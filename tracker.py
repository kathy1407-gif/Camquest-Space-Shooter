import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python import BaseOptions
import requests
import socket
import math

# ---------- UDP SETUP ----------
UDP_IP = "127.0.0.1"
UDP_PORT = 25001
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# --------------------------------

TARGETED_FINGERS={8:"Index", 12:"Middle", 16:"Ring"}
history={}

def detect_flick(hand_landmarks):

    if hand_landmarks is None:
        return 'None'

    detected_flick=[]
    
    for tip_id, finger_name in TARGETED_FINGERS.items():
        tip=hand_landmarks[tip_id]
        curr_pos=(tip.x,tip.y)

        if tip_id in history:
            prev_x,prev_y=history[tip_id]

            distance=math.sqrt((curr_pos[0]-prev_x)**2 + (curr_pos[1]-prev_y)**2)

            if distance > 0.07:
                detected_flick.append(finger_name)

        history[tip_id]=curr_pos

    if detected_flick:
        return detected_flick[0]
    else:
        return 'None'
        

def detect_direction(hand_landmarks):

    index_tip=hand_landmarks[8]
    index_pip=hand_landmarks[6]

    dx= index_tip.x - index_pip.x
    dy= index_tip.y - index_pip.y

    direction='Standing'

    if dx > 0.025:
        direction= 'Left'
    elif dx < -0.035:
        direction= 'Right'
    if dy < -0.12 and abs(dy) > abs(dx)*1.2:
        direction= 'Standing'
    
    return direction

   

def detect_hand_data(frame, hands):
    img_rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    mp_img=mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)

    results=hands.detect(mp_img)

    right_landmarks=None
    left_landmarks=None

    direction='Standing'
    flick='None'

    if results.hand_landmarks:
        
        #if (results.handedness[0][0].category_name=="Right"):
         #   right_landmarks=results.hand_landmarks[0]
        #elif (results.handedness[1][0].category_name=="Right"):
        #    right_landmarks=results.hand_landmarks[1]
        #if (results.handedness[0][0].category_name=="Left"):
         #   left_landmarks=results.hand_landmarks[0]
        #elif (results.handedness[1][0].category_name=="Left"):
        #    left_landmarks=results.hand_landmarks[1]
    
        for i, handed_list in enumerate(results.handedness):
            handed = handed_list[0]
            if handed.category_name == "Right":
                right_landmarks = results.hand_landmarks[i]
            elif handed.category_name == "Left":
                left_landmarks = results.hand_landmarks[i]
        

        if left_landmarks is not None:
            direction=detect_direction(left_landmarks)
        if right_landmarks is not None:
            flick=detect_flick(right_landmarks)

        

        h,w,_=frame.shape
        if(right_landmarks):
            for i in range(5):
                cv2.line(frame, (int(right_landmarks[4*i+1].x*w),int(right_landmarks[4*i+1].y*h)),(int(right_landmarks[4*i+2].x*w),int(right_landmarks[4*i+2].y*h)),(255,255,255))
                cv2.line(frame, (int(right_landmarks[4*i+2].x*w),int(right_landmarks[4*i+2].y*h)),(int(right_landmarks[4*i+3].x*w),int(right_landmarks[4*i+3].y*h)),(255,255,255))
                cv2.line(frame, (int(right_landmarks[4*i+3].x*w),int(right_landmarks[4*i+3].y*h)),(int(right_landmarks[4*i+4].x*w),int(right_landmarks[4*i+4].y*h)),(255,255,255))
            for i in range(4):
                cv2.line(frame, (int(right_landmarks[4*i+1].x*w),int(right_landmarks[4*i+1].y*h)),(int(right_landmarks[4*i+5].x*w),int(right_landmarks[4*i+5].y*h)),(255,255,255))
            cv2.line(frame, (int(right_landmarks[0].x*w),int(right_landmarks[0].y*h)),(int(right_landmarks[17].x*w),int(right_landmarks[17].y*h)),(255,255,255))
            cv2.line(frame, (int(right_landmarks[0].x*w),int(right_landmarks[0].y*h)),(int(right_landmarks[1].x*w),int(right_landmarks[1].y*h)),(255,255,255))

            for lm in right_landmarks:
                cx,cy=int(lm.x*w),int(lm.y*h)
                cv2.circle(frame,(cx,cy),3,(0,0,255),-1)

        if(left_landmarks):
            for i in range(5):
                cv2.line(frame, (int(left_landmarks[4*i+1].x*w),int(left_landmarks[4*i+1].y*h)),(int(left_landmarks[4*i+2].x*w),int(left_landmarks[4*i+2].y*h)),(255,255,255))
                cv2.line(frame, (int(left_landmarks[4*i+2].x*w),int(left_landmarks[4*i+2].y*h)),(int(left_landmarks[4*i+3].x*w),int(left_landmarks[4*i+3].y*h)),(255,255,255))
                cv2.line(frame, (int(left_landmarks[4*i+3].x*w),int(left_landmarks[4*i+3].y*h)),(int(left_landmarks[4*i+4].x*w),int(left_landmarks[4*i+4].y*h)),(255,255,255))
            for i in range(4):
                cv2.line(frame, (int(left_landmarks[4*i+1].x*w),int(left_landmarks[4*i+1].y*h)),(int(left_landmarks[4*i+5].x*w),int(left_landmarks[4*i+5].y*h)),(255,255,255))
            cv2.line(frame, (int(left_landmarks[0].x*w),int(left_landmarks[0].y*h)),(int(left_landmarks[17].x*w),int(left_landmarks[17].y*h)),(255,255,255))
            cv2.line(frame, (int(left_landmarks[0].x*w),int(left_landmarks[0].y*h)),(int(left_landmarks[1].x*w),int(left_landmarks[1].y*h)),(255,255,255))

            for lm in left_landmarks:
                cx,cy=int(lm.x*w),int(lm.y*h)
                cv2.circle(frame,(cx,cy),3,(0,0,255),-1)

    return direction,flick
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

        directed,flicked = detect_hand_data(frame, hands)
        frame = cv2.flip(frame, 1)
        
        cv2.rectangle(frame,(10,10), (400,100), (0,0,0),-1)
        cv2.putText(frame,f"Direction: {directed}",(20,40),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        cv2.putText(frame, f"Flick: {flicked}", (20,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),2)


        if directed:
            message = f"Direction: {directed} Flick: {flicked}"
            sock.sendto(message.encode("utf-8"), (UDP_IP, UDP_PORT))

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

