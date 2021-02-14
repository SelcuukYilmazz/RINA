import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import time


#######################################################################################################################
#  Functions
    # Getting Contours Of Image
def getContours(img,imgContour,relative_area,box,corners,time):
    print(relative_area)
    contours,hierarchy = cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area >= relative_area:
            # Reduce Mistakes With Approximation Functions
            time = 0
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.025 * peri, True)
            if len(approx) == 4:
                relative_area = area
                rect = cv.minAreaRect(cnt)
                box = cv.boxPoints(rect)
                box = np.int0(box)
                corners = len(approx)

    if time == 20:
        box = []
        relative_area = 186

    if len(box) != 0:
        center = (box[0] + box[2]) // 2
        cv.drawContours(imgContour, [box], -1, (255, 0, 255), 7)
        cv.circle(imgContour,(center[0],center[1]), 0, (0,255,0), 15)
        cv.putText(imgContour,'Points: ' + str(corners),(center[0] + 20,center[1] + 20), cv.FONT_HERSHEY_DUPLEX,.7,(0,255,0),2)
        cv.putText(imgContour,'Area: ' + str(int(relative_area)), (center[0] + 20,center[1] + 45),cv.FONT_HERSHEY_DUPLEX,0.7,(0,255,0),2)
        cv.putText(imgContour,'X_Axis: '+str(center[0]),((center[0] + 20,center[1] + 70)),cv.FONT_HERSHEY_DUPLEX,0.7,(0,255,0),2)
        cv.putText(imgContour,'Y_Axis: ' + str(center[1]), ((center[0] + 20, center[1] + 95)),cv.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)
    return relative_area,box,corners,time


    # Whenever Trackbar Moves This Function Will Be Executed
def empty(a):
    pass

    # Stacking Given Images as nx3 matrix
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])

    # Checking Data Type

    rowsAvailable = isinstance(imgArray[0],list)

    # Taking Variables

    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]

    # If Data is List Then Go

    if rowsAvailable:
        for x in range (0,rows):
            for y in range (0,cols):

                # If Image Width and Height Is Equals To First Image Then Resize Both Image

                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv.resize(imgArray[x][y],(0,0),None,scale,scale)

                # If Image Width and Height Is Not Equals To First Image Then Resize Both Image But Different Ratios

                else:
                    imgArray[x][y] = cv.resize(imgArray[x][y],(imgArray[0][0].shape[1],imgArray[0][0].shape[0]),None,scale,scale)

                # If Image is Grey Filtered Then Make It BGR

                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv.cvtColor(imgArray[x][y],cv.COLOR_GRAY2BGR)

        # Create Empty Window Then Open Screens On It

        imageBlank = np.zeros((height,width,3),np.uint8)
        hor = [imageBlank]*rows
        for x in range(0,rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)

    # If Data Is Not List Then Take Pictures One By One And Make All Functions Above As The Same

    else:
        for x in range(0,rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv.resize(imgArray[x],(0,0),None,scale,scale)
            else:
                imgArray[x] = cv.resize(imgArray[x],(imgArray[0].shape[1],imgArray[0].shape[0]),None,scale,scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv.cvtColor(imgArray[x],cv.COLOR_GRAY2BGR)
        hor =np.hstack(imgArray)
        ver = hor
    return ver


# Image Process Main Function
def image_process(capture, relative_area,box,corners,time):
    # If Camera Captures Video Than isTrue is True
    # frame Is Captured Video
    isTrue, frame = capture.read()

    # Brighten Image
    Intensity_Matrix = np.ones(frame.shape, dtype='uint8') * 60
    frame = cv.add(frame, Intensity_Matrix)

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

    # Blur

    blur = cv.GaussianBlur(frame, (7, 7), 1)

    # Grey Filter

    grey = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)

    # Canny Edge Detector

    canny = cv.Canny(grey, threshold1, threshold2)

    # Dilation Function This Function Makes Bright Pixels Brighter And Program Can See Edges More Clearly With This
    kernel = np.ones((3, 3))
    imgDil = cv.dilate(canny, kernel, iterations=4)

    # Erode Function This Function Makes Photo Little Smaller

    imgDil = cv.erode(imgDil, kernel, iterations=2)

    # Get Contours
    relative_area,box,corners,time = getContours(imgDil, imgContour,relative_area,box,corners,time)

    # Stack Images
    imgStack = stackImages(0.8, ([frame, canny, mask], [imgDil, imgContour, result]))
    cv.imshow('All', imgStack)
    return relative_area,box,corners,time




########################################################################################################################
########################################################################################################################
############################################# Main Code ######################################
# Variables
relative_area = 186
box = []
corners = 0
time = 0
# Capturing Video From Your Camera
capture = cv.VideoCapture(0)

# Trackbar Interface
cv.namedWindow('Parameters')
cv.resizeWindow('Parameters', 640, 640)
cv.createTrackbar('Threshold1', 'Parameters', 82, 255, empty)
cv.createTrackbar('Threshold2', 'Parameters', 67, 255, empty)
cv.createTrackbar('HUE Min', 'Parameters', 0, 179, empty)
cv.createTrackbar('HUE Max', 'Parameters', 100, 179, empty)
cv.createTrackbar('SAT Min', 'Parameters', 73, 255, empty)
cv.createTrackbar('SAT Max', 'Parameters', 173, 255, empty)
cv.createTrackbar('VALUE Min', 'Parameters', 0, 255, empty)
cv.createTrackbar('VALUE Max', 'Parameters', 255, 255, empty)
while True:
    relative_area,box,corners,time = image_process(capture,relative_area,box,corners,time)
    time += 1
    # Wait until you press d
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

########################################################################################################################
# Below works for quit code

capture.release()
cv.destroyAllWindows()


