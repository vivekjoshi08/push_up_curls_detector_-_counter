import cv2
from cvzone.PoseModule import PoseDetector
import cvzone
import angle_check

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
        #angles of hand ( shoulder, elbow, wrist)
        right_hand_angle = detector.findAngle(image, 12, 14, 16, draw = False)
        waste_angle_right = detector.findAngle(image, 12, 0, 11, draw = False)

        left_hand_angle = detector.findAngle(image, 15, 13, 11, draw = False)
        #waste_angle_left = detector.findAngle(image, 0, 11, 13, draw = True)

        #creating percentage value for bar-plot using angles
        if right_hand_angle > 190 :
            right_check = angle_check.dumble_curl(right_hand_angle)
            left_check = angle_check.dumble_curl(left_hand_angle)
            check = 2
            #filling bar
            right_bar = angle_check.filling_bar(right_check)
            left_bar = angle_check.filling_bar(left_check)

        elif right_hand_angle < 190 :

            if waste_angle_right < 130 :

                right_check = angle_check.pushup(right_hand_angle)
                left_check = angle_check.pushup(left_hand_angle)
                check = 1
                #filling bar
                right_bar = angle_check.filling_bar(right_check)
                left_bar = angle_check.filling_bar(left_check)
            else:
                right_check = 0
                left_check = 0
                right_bar = angle_check.filling_bar(0)
                left_bar = angle_check.filling_bar(0)

        

        #creating bar on live frame
        #right side bar
        cv2.rectangle(image, (15,right_bar), (15+15, 60+590), (0,255,0), cv2.FILLED)
        cv2.rectangle(image, (15, 60), (15+15, 60+590), (255,255,255))
        #left side bar
        cv2.rectangle(image, (1220,left_bar), (1220+15, 60+590), (0,255,0), cv2.FILLED)
        cv2.rectangle(image, (1220, 60), (1220+15, 60+590), (255,255,255))

        if right_check == 100 and left_check == 100:
            if flag == 0:
                if check == 1:
                    push_up_counter += 0.5
                    check = 0
                elif check == 2:
                    dumble_counter += 0.5
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

