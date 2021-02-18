import numpy as np
import cv2 as cv
import math
import matplotlib.pyplot as plt
from Objects import Rectangle


#######################################################################################################################
#  Functions
    # Getting Contours Of Image
def getContours(img,imgContour,door):
    contours,hierarchy = cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv.contourArea(cnt)

        # If area getting bigger then lock to that area and release this but if it is a rectangle
        if area >= door.area[2]:

            # Reduce Mistakes With Approximation Functions
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.025 * peri, True)
            if len(approx) == 4:
                # Reset time everytime code gets in here
                door.Start_time()

                for i in range(len(door.area)):
                    if area > door.area[i]:
                        door.area[i] = area
                        rect = cv.minAreaRect(cnt)
                        temp_box = cv.boxPoints(rect)
                        temp_box = np.int0(temp_box)

                        if i == 0:
                            door.environment_box = temp_box
                            door.corners = len(approx)
                            door.lock = True
                        elif len(door.environment_center) == 2:
                            if i == 1 and door.area[0]-area >= door.area[0]//20 and door.environment_center[1] < ((temp_box[0] + temp_box[2]) // 2)[1]:
                                door.lower_box = temp_box
                                door.corners = len(approx)

                            elif i == 2 and door.area[0] - area > door.area[0]//10 and door.environment_center[1] > ((temp_box[0] + temp_box[2]) // 2)[1]:
                                door.higher_box = temp_box
                                door.corners = len(approx)



                        break
                temp = door.environment_box.view(np.ndarray)
                temp = temp[np.lexsort((temp[:, 1],))]
                door.upper_corners = temp[:2]
                if abs(door.upper_corners[0][1] - door.upper_corners[1][1]) >= 5 :
                    print('Yamuk lan bu!')


    door.Scan_time()
    # Reset every 60 repeats
    if door.scan_time >= 2:
        door.environment_box = []
        door.higher_box = []
        door.lower_box = []
        door.area = [186,185,184]
        door.environment_center = []
        door.upper_corners = []
        door.lock = False

    # If door locked on something then draw it
    if door.lock:
        door.environment_center = (door.environment_box[0] + door.environment_box[2]) // 2
        cv.drawContours(imgContour, [door.environment_box], -1, (255, 0, 255), 7)
        if len(door.higher_box) > 0:
            cv.drawContours(imgContour, [door.higher_box], -1, (255, 0, 255), 7)
            cv.putText(imgContour,'Yüksek Puan',(door.higher_box[1][0],door.higher_box[1][1]),cv.FONT_HERSHEY_DUPLEX,0.7,(0,0,255),2)
        if len(door.lower_box) > 0:
            cv.drawContours(imgContour, [door.lower_box], -1, (255, 0, 255), 7)
            cv.putText(imgContour, 'Düşük Puan', (door.lower_box[1][0],door.lower_box[1][1]), cv.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255), 2)
        cv.circle(imgContour,(door.upper_corners[0][0],door.upper_corners[0][1]),0,(0,0,255),5)
        cv.circle(imgContour, (door.upper_corners[1][0],door.upper_corners[1][1]), 0, (0, 0, 255), 5)
        cv.circle(imgContour,(door.environment_center[0],door.environment_center[1]), 0, (0,255,0), 15)
        cv.putText(imgContour,'Points: ' + str(door.corners),(door.environment_center[0] + 20,door.environment_center[1] + 20), cv.FONT_HERSHEY_DUPLEX,.7,(0,255,0),2)
        cv.putText(imgContour,'Area: ', (door.environment_center[0] + 20,door.environment_center[1] + 45),cv.FONT_HERSHEY_DUPLEX,0.7,(0,255,0),2)
        cv.putText(imgContour,'X_Axis: '+str(door.environment_center[0]),((door.environment_center[0] + 20,door.environment_center[1] + 70)),cv.FONT_HERSHEY_DUPLEX,0.7,(0,255,0),2)
        cv.putText(imgContour,'Y_Axis: ' + str(door.environment_center[1]), ((door.environment_center[0] + 20, door.environment_center[1] + 95)),cv.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)

    return


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
def Rectangle_process(capture,door):

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
    imgDil = cv.dilate(canny, kernel, iterations=3)

    # Erode Function This Function Makes Photo Little Smaller
    imgDil = cv.erode(imgDil, kernel, iterations=2)

    # Get Contours
    getContours(imgDil, imgContour,door)

    # Stack Images
    imgStack = stackImages(0.8, ([frame, canny, mask], [imgDil, imgContour, result]))
    cv.imshow('All', imgStack)
    return

def Circle_Process(capture):

    # If Camera Captures Video Than isTrue is True
    # frame Is Captured Video
    isTrue,frame = capture.read()

    # Copied Original Image to output variable
    output = frame.copy()

    # Brighten Image
    Intensity_Matrix = np.ones(frame.shape, dtype='uint8') * 60
    frame = cv.add(frame, Intensity_Matrix)

    # Changing Color of Image to Gray So We Can Detect Edges Easily
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)

    # Doing Blur on Image So We Can Detect Edges Easily
    gray = cv.GaussianBlur(gray,(21,21),cv.BORDER_DEFAULT)

    # Detecting Circles Are In all_circs
    all_circs = cv.HoughCircles(gray,cv.HOUGH_GRADIENT,0.9,120,param1=60,param2=30,minRadius=60,maxRadius=500)

    # If Any Circle Detected Then Go
    if type(all_circs) != type(None):

        # Make Circle Around Circles
        all_circs_rounded = np.uint16(np.around(all_circs))
        for i in all_circs_rounded[0,:]:
            cv.circle(output,(i[0],i[1]),i[2],(50,200,200),5)
            cv.circle(output,(i[0],i[1]),2,(255,0,0),3)
            cv.putText(output,'Center x: '+str(i[0]),(i[0]+20,i[1]),cv.FONT_HERSHEY_DUPLEX,.7,(0,255,0),2)
            cv.putText(output, 'Center y: ' + str(i[1]), (i[0] + 20, i[1]-25), cv.FONT_HERSHEY_DUPLEX, .7, (0, 255, 0), 2)
            cv.putText(output, 'Area : ' + str(int(math.pi*(i[2]**2))), (i[0] + 20, i[1]-50), cv.FONT_HERSHEY_DUPLEX, .7, (0, 255, 0), 2)

    cv.imshow('Circles',output)



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

########################################################################################################################
########################################################################################################################
################################################ Main Code #############################################################

# Variables
door = Rectangle()

# Capturing Video From Your Camera
capture = cv.VideoCapture(0)

# Timer Start
door.Start_time()

while True:
    Rectangle_process(capture,door)
    # Circle_Process(capture)


    # Wait until you press d
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

########################################################################################################################
# Below works for quit code

capture.release()
cv.destroyAllWindows()


