import cv2
import os
import cvzone
from cvzone.PoseModule import PoseDetector

# Body Keypoint Detector
detector = PoseDetector()

# Image Load
img = cv2.imread('pose_tracking_full_body_landmarks.png')

## video Load
cap = cv2.VideoCapture('Videos/1.mp4')


## Video width & height
# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# print(width , height)

## Live Camera Test
# cap = cv2.VideoCapture(0)


# Load Shirts path
shirts = 'Shirts'
shirt_path = os.listdir(shirts)
shirt_no = 0

# Shirt Change Button
img_button_right = cv2.imread('button.png', cv2.IMREAD_UNCHANGED)
img_button_left = cv2.flip(img_button_right,1)

counter_right = 0
counter_left = 0

# Button Load Speed
speed = 10

# Shirt Size
fixedRatio = 262 / 190
shirt_hight_wight_ratio = 581/440


while True:
    rat , frame = cap.read()
    # frame = cv2.flip(frame,1)

    # Body Keypoint Detection
    frame = detector.findPose(frame)
    lmList, bboxInfo = detector.findPosition(frame, bboxWithHands=False , draw=False)
    if bboxInfo:
        # center = bboxInfo["center"]
        # cv2.circle(frame, center, 5, (255, 0, 255), cv2.FILLED)

        ## Put Shirt in Video 
        shirt_land_map12 = lmList[12][1:3]
        shirt_land_map11 = lmList[11][1:3]
        img_shirt = cv2.imread(os.path.join(shirts,shirt_path[shirt_no]) , cv2.IMREAD_UNCHANGED)

        width_shirt = int((shirt_land_map11[0] - shirt_land_map12[0]) * fixedRatio)
        
        shirt_resize = cv2.resize(img_shirt, (width_shirt , int(width_shirt * shirt_hight_wight_ratio)))

        current_scale = (shirt_land_map11[0] - shirt_land_map12[0]) / 190
        offset = int(44 * current_scale) , int(48 * current_scale)
        try:
            frame = cvzone.overlayPNG(frame, shirt_resize, (shirt_land_map12[0] - offset[0] ,shirt_land_map12[1] - offset[1]))
        except:
            pass
    
    # Add Shirt Change Button
    frame = cvzone.overlayPNG(frame,img_button_right,(1074,293))
    frame = cvzone.overlayPNG(frame,img_button_left,(72,293))

    # Shirt Change with Right Button
    if lmList[16][1] < 300:
        counter_right += 1
        frame = cv2.ellipse(frame , (139 , 360) , (66,66) , 0 , 0 , counter_right * speed , (0 , 255 ,0) , 10)
        if speed * counter_right > 360:
            counter_right = 0
            if shirt_no < len(shirt_path)-1:
                shirt_no += 1

    # Shirt Change with Left Button
    elif lmList[15][1] > 950:
        counter_left += 1
        frame = cv2.ellipse(frame , (1138 , 360) , (66,66) , 0 , 0 , counter_left * speed , (0 , 255 ,0) , 10)
        if speed * counter_left > 360:
            counter_left = 0
            if shirt_no > 0:
                shirt_no -= 1

    
    else:
        counter_right = 0
        counter_left = 0


    # Play Video / Image
    cv2.imshow('frame', frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break