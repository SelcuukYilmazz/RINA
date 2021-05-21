import numpy as np
import cv2 as cv
import math
# import Calibration
import matplotlib.pyplot as plt
from Objects import Rectangle
from Objects import Circle


###############################################################################
#  Functions
    # Getting Contours Of Image
def getContours(img, imgContour, door):
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv.contourArea(cnt)

        # If area getting bigger then lock to that area and release this but if it is a rectangle
        if area >= door.area[1]:

            # Reduce Mistakes With Approximation Functions
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.025 * peri, True)
            if len(approx) == 4:
                # Reset time everytime code gets in here
                door.Start_time()
                # Decides which square will be change (lower,higher or enviromental)
                for i in range(len(door.area)):
                    if area > door.area[i]:

                        rect = cv.minAreaRect(cnt)
                        temp_box = cv.boxPoints(rect)
                        temp_box = np.int0(temp_box)

                        temp_center = (temp_box[0]+temp_box[2])//2


                        if i == 0 and area>=door.area[1]*3:
                            door.area[i] = area
                            door.lower_box = temp_box
                            door.corners = len(approx)
                            door.lock = True
                            door.lower_center = temp_center
                            break

                        elif i == 1 and area<=door.area[0]/3:
                            door.area[i] = area
                            door.higher_box = temp_box
                            door.corners = len(approx)
                            door.lock = True
                            door.higher_center = temp_center
                            break

                # Controls for decent rectangle
                # if isinstance(door.higher_box[0], np.ndarray):
                #     temp = door.higher_box.view(np.ndarray)
                #     temp = temp[np.lexsort((temp[:, 1],))]
                #     door.upper_corners = temp[:2]
                #     if abs(door.upper_corners[0][1] - door.upper_corners[1][1]) >= 30:
                #         print('Yamuk!')
                #         door.decent_shape = False

    door.Scan_time()
    # Reset every 1.5 seconds
    if door.scan_time >= 1.5:
        door.higher_box = []
        door.lower_box = []
        door.area = [185, 184]
        door.higher_center = []
        door.lower_center = []
        door.upper_corners = []
        door.lock = False
        door.decent_shape = True

    # If door locked on something then draw it
    if door.lock:
        if len(door.higher_box) == 4:
            # Change higher rectangle's center and draw it

            cv.circle(imgContour, (door.higher_center[0], door.higher_center[1]), 0, (255, 255, 255), 5)
            cv.drawContours(imgContour, [door.higher_box], -1, (255, 0, 255), 7)
            cv.putText(imgContour, 'Yüksek Puan', (door.higher_box[1][0], door.higher_box[1][1]),
                       cv.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255), 2)
            cv.putText(imgContour, 'Points: ' + str(door.corners),
                       (door.higher_center[0] + 20, door.higher_center[1] + 20), cv.FONT_HERSHEY_DUPLEX, .7, (0, 255, 0),
                       2)
            cv.putText(imgContour, 'Area: ', (door.higher_center[0] + 20, door.higher_center[1] + 45),
                       cv.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)
            cv.putText(imgContour, 'X_Axis: ' + str(door.higher_center[0]),
                       ((door.higher_center[0] + 20, door.higher_center[1] + 70)), cv.FONT_HERSHEY_DUPLEX, 0.7,
                       (0, 255, 0), 2)
            cv.putText(imgContour, 'Y_Axis: ' + str(door.higher_center[1]),
                       ((door.higher_center[0] + 20, door.higher_center[1] + 95)), cv.FONT_HERSHEY_DUPLEX, 0.7,
                       (0, 255, 0), 2)
        if len(door.lower_box) == 4:
            # Change lower rectangle's center and draw it

            cv.circle(imgContour, (door.lower_center[0], door.lower_center[1]), 0, (255, 255, 255), 5)
            cv.drawContours(imgContour, [door.lower_box], -1, (255, 0, 255), 7)
            cv.putText(imgContour, 'Düşük Puan', (door.lower_box[1][0], door.lower_box[1][1]), cv.FONT_HERSHEY_DUPLEX,
                       0.7, (0, 0, 255), 2)
            cv.putText(imgContour, 'Points: ' + str(door.corners),
                       (door.lower_center[0] + 20, door.lower_center[1] + 20), cv.FONT_HERSHEY_DUPLEX, .7, (0, 255, 0),
                       2)
            cv.putText(imgContour, 'Area: ', (door.lower_center[0] + 20, door.lower_center[1] + 45),
                       cv.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)
            cv.putText(imgContour, 'X_Axis: ' + str(door.lower_center[0]),
                       ((door.lower_center[0] + 20, door.lower_center[1] + 70)), cv.FONT_HERSHEY_DUPLEX, 0.7,
                       (0, 255, 0), 2)
            cv.putText(imgContour, 'Y_Axis: ' + str(door.lower_center[1]),
                       ((door.lower_center[0] + 20, door.lower_center[1] + 95)), cv.FONT_HERSHEY_DUPLEX, 0.7,
                       (0, 255, 0), 2)
        # cv.circle(imgContour, (door.upper_corners[0][0], door.upper_corners[0][1]), 0, (0, 0, 255), 5)
        # cv.circle(imgContour, (door.upper_corners[1][0], door.upper_corners[1][1]), 0, (0, 0, 255), 5)


    return


    # Whenever Trackbar Moves This Function Will Be Executed
def empty(a):
    pass

# Image Process Main Function
def Rectangle_process(capture,door):

    # If Camera Captures Video Than isTrue is True
    # frame Is Captured Video
    isTrue, frame = capture.read()


    # Input Taken From Trackbar to Thresholds
    threshold1 = cv.getTrackbarPos('Threshold1', 'Parameters')
    threshold2 = cv.getTrackbarPos('Threshold2', 'Parameters')

    # Color Detection Trackbars
    hueMin = cv.getTrackbarPos('HUE Min', 'Parameters')
    hueMax = cv.getTrackbarPos('HUE Max', 'Parameters')
    satMin = cv.getTrackbarPos('SAT Min', 'Parameters')
    satMax = cv.getTrackbarPos('SAT Max', 'Parameters')
    valMin = cv.getTrackbarPos('VALUE Min', 'Parameters')
    valMax = cv.getTrackbarPos('VALUE Max', 'Parameters')

    # Original Image to HSV
    imgHsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Color Detection Numpy Matrix
    lower = np.array([hueMin, satMin, valMin])
    upper = np.array([hueMax, satMax, valMax])
    mask = cv.inRange(imgHsv, lower, upper)
    result = cv.bitwise_and(frame, frame, mask=mask)

    # Detected Image (Working Image)
    imgContour = frame.copy()

    # # Blur
    blur = cv.GaussianBlur(frame, (7, 7),1)

    # Grey Filter
    grey = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)

    grey = cv.bilateralFilter(grey, 1, 10, 120)
    # Canny Edge Detector
    canny = cv.Canny(grey, threshold1, threshold2)

    # Puts circle shape middle of image
    cv.circle(imgContour, (320,320), 20, (255, 255, 255), 5)

    # Get Contours
    getContours(canny, imgContour,door)

    cv.imshow('xxx',canny)
    cv.imshow('Result', imgContour)
    return

def Circle_Process(capture,circle):

    # If Camera Captures Video Than isTrue is True
    # frame Is Captured Video
    isTrue,frame = capture.read()

    # Copied Original Image to output variable
    output = frame.copy()

    # Changing Color of Image to Gray So We Can Detect Edges Easily
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)

    # Doing Blur on Image So We Can Detect Edges Easily
    gray = cv.GaussianBlur(gray,(19,19),cv.BORDER_DEFAULT)

    # Detecting Circles Are In all_circs
    all_circs = cv.HoughCircles(gray,cv.HOUGH_GRADIENT,0.9,120,param1=60,param2=30,minRadius=60,maxRadius=500)

    # Puts circle shape middle of image
    cv.circle(output, (320, 270), 20, (255, 255, 255), 5)

    # If Any Circle Detected Then Go
    if type(all_circs) != type(None):
            # Make Circle Around Circles
            all_circs_rounded = np.uint16(np.around(all_circs))
            for i in all_circs_rounded[0,:]:
                circle.Scan_time()
                if circle.area == 0 or circle.area > int(math.pi * (i[2] ** 2)) or circle.scan_time>3:
                    circle.Start_time()
                    circle.area = int(math.pi * (i[2] ** 2))
                    circle.lock_coordinate = [i[0]+i[2]-5,i[1]]
                    circle.box=i


    if len(circle.box)!=0:
        cv.circle(output, (circle.box[0], circle.box[1]), circle.box[2], (50, 200, 200), 5)
        cv.circle(output, (circle.box[0] + circle.box[2] - 5, circle.box[1]), 5, (255, 0, 0), 3)
        cv.putText(output, 'Center x: ' + str(circle.box[0]), (circle.box[2] + 20, circle.box[1]), cv.FONT_HERSHEY_DUPLEX, .7, (0, 255, 0), 2)
        cv.putText(output, 'Center y: ' + str(circle.box[1]), (circle.box[2] + 20, circle.box[1] - 25), cv.FONT_HERSHEY_DUPLEX, .7, (0, 255, 0), 2)
        cv.putText(output, 'Area : ' + str(circle.area), (circle.box[0] + 20, circle.box[1] - 50), cv.FONT_HERSHEY_DUPLEX, .7,
                   (0, 255, 0), 2)

    cv.imshow('Circles',output)