import cv2
from cvzone.PoseModule import PoseDetector
import cvzone
import angle_check
import bar_creation

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

detector = PoseDetector()

flag, check, push_up_counter, dumble_counter, count_ = 0, 0, 0, 0, 0

while True:
    success, image = cap.read()

    image = detector.findPose(image, draw = False)
    imlist, box = detector.findPosition(image, draw = False)

    if imlist:
        #angle: ( shoulder, elbow, wrist)
        right_hand_elbow = detector.findAngle(image, 12, 14, 16, draw = True)
        left_hand_elbow = detector.findAngle(image, 15, 13, 11, draw = True)
        
        #angle: (nose with shoulders)
        nose_angle_with_shoulders = detector.findAngle(image, 12, 0, 11, draw = True)

        #angle: (2 shouldes and elbow)
        right_elbow_shoulders = detector.findAngle(image, 11, 12, 14, draw = True)
        left_elbow_shoulders = detector.findAngle(image, 12, 11, 13, draw = True)

        #angle: (knee, hip, shoulder)
        right_knee_hip_shoulder = detector.findAngle(image, 26, 24, 12, draw = True)
        left_knee_hip_shoulder = detector.findAngle(image, 25, 23, 11, draw = True)


        #creating percentage value for bar-plot using angles

        #dumble_curl
        if right_hand_elbow > 190 and nose_angle_with_shoulders > 250 and nose_angle_with_shoulders < 300:
            right_check = angle_check.dumble_curl(right_hand_elbow)
            left_check = angle_check.dumble_curl(left_hand_elbow)
            check = 1
            right_bar = angle_check.filling_bar(right_check)
            left_bar = angle_check.filling_bar(left_check)

        #jumpingjack
        elif right_elbow_shoulders < 110 and right_knee_hip_shoulder > 165:
            right_check = angle_check.jumping_jack.right_abc(right_elbow_shoulders)
            left_check = angle_check.jumping_jack.left_abc(left_elbow_shoulders)

        #push_up
        elif right_hand_elbow < 190 :

            if nose_angle_with_shoulders < 130 :

                right_check = angle_check.pushup(right_hand_elbow)
                left_check = angle_check.pushup(left_hand_elbow)
                check = 2
                right_bar = angle_check.filling_bar(right_check)
                left_bar = angle_check.filling_bar(left_check)
            else:
                right_check = 0
                left_check = 0
                right_bar = angle_check.filling_bar(0)
                left_bar = angle_check.filling_bar(0)
        
        bar_creation.bar_creation(image, right_bar, left_bar)


        #counting
        if right_check == 100 and left_check == 100:
            if flag == 0:
                if check == 1:
                    dumble_counter += 0.5
                    check = 0
                    
                elif check == 2:
                    push_up_counter += 0.5
                    check = 0
                count_ += 0.5
                flag = 1

        elif right_check == 0 and left_check == 0:
            if flag == 1:
                if check == 1:
                    push_up_counter += 0.5
                    check = 0
                elif check == 2:
                    dumble_counter += 0.5
                    check = 0
                count_ += 0.5
                flag = 0
        

        #count bar
        cvzone.putTextRect(image, f'Count_pushup: {int(push_up_counter)} ', (45,20), 1, 2, (0,0,0), (255,255,255), border=1, colorB = (0,255,0))
        cvzone.putTextRect(image, f'Count_curls: {int(dumble_counter)} ', (1000,20), 1, 2, (0,0,0), (255,255,255), border=1, colorB = (0,255,0))
        cvzone.putTextRect(image, f'Calories burned: {round(int(push_up_counter)*0.3, 2)} cal', (45, 50), 1, 2, (0,0,0), (255,255,255), border=1, colorB = (0,255,0))
        cvzone.putTextRect(image, f'Calories burned: {round(int(dumble_counter)*0.02, 2)} cal', (1000, 50), 1, 2, (0,0,0), (255,255,255), border=1, colorB = (0,255,0))
        cvzone.putTextRect(image, f'Total calories burned: {round((int(push_up_counter)*0.3) + (int(dumble_counter)*0.02), 2)} cal', (25, 700), 1, 2, (0,0,0), (255, 255, 255), border=1, colorB= (0,255,0))    

    cv2.imshow('Counter', image)
    if cv2.waitKey(1) == ord('q'):
        break

