import cv2

def bar_creation(image, right_bar, left_bar):

    #right side bar
    cv2.rectangle(image, (15,right_bar), (15+15, 60+590), (0,255,0), cv2.FILLED)
    cv2.rectangle(image, (15, 60), (15+15, 60+590), (255,255,255))

    #left side bar
    cv2.rectangle(image, (1220,left_bar), (1220+15, 60+590), (0,255,0), cv2.FILLED)
    cv2.rectangle(image, (1220, 60), (1220+15, 60+590), (255,255,255))