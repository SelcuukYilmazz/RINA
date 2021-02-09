import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv

#  Functions
    # Getting Contours Of Image
def getContours(img,imgContour):
    contours,hierarchy = cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 2000:

            # Reduce Mistakes With Approximation Functions

            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.01 * peri, True)
            # x,y,w,h = cv.boundingRect(approx)
            rect = cv.minAreaRect(cnt)
            box = cv.boxPoints(rect)
            box = np.int0(box)
            center = (box[0]+box[2])//2
            print(box[0][0] + box[1][0] + 20)
            if len(approx) == 4:
                cv.drawContours(imgContour, [box], -1, (255, 0, 255), 7)
                cv.circle(imgContour,(center[0],center[1]), 0, (0,255,0), 15)
                cv.putText(imgContour,'Points: ' + str(len(approx)),(center[0] + 20,center[1] + 20), cv.FONT_HERSHEY_DUPLEX,.7,(0,255,0),2)
                cv.putText(imgContour,'Area: ' + str(int(area)), (center[0] + 20,center[1] + 45),cv.FONT_HERSHEY_DUPLEX,0.7,(0,255,0),2)



    # Whenever Trackbar Moves This Function Will Be Executed
def empty(a):
    pass

    # Stacking Given Images as nx3 matrix
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])

    # Checking Data Type

    rowsAvaliable = isinstance(imgArray[0],list)

    # Taking Variables

    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]

    # If Data is List Then Go

    if rowsAvaliable:
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


# Trackbar Interface
cv.namedWindow('Parameters')
cv.resizeWindow('Parameters',640,80)
cv.createTrackbar('Threshold1','Parameters',75,255,empty)
cv.createTrackbar('Threshold2','Parameters',64,255,empty)

# Capturing Video From Your Camera

capture = cv.VideoCapture(0)

while True:
    # If Camera Captures Video Than isTrue is True
    # frame Is Captured Video
    isTrue,frame = capture.read()


    # Input Taken From Trackbar to Thresholds
    threshold1 = cv.getTrackbarPos('Threshold1','Parameters')
    threshold2 = cv.getTrackbarPos('Threshold2','Parameters')

    # Detected Image (Working Image)
    imgContour = frame.copy()

    # Blur

    blur = cv.GaussianBlur(frame,(7,7),1)

    # Grey Filter

    grey = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)

    # Canny Edge Detector

    canny = cv.Canny(grey,threshold1,threshold2)

    # Dilation Function This Function Makes Bright Pixels Brighter And Program Can See Edges More Clearly With This
    kernel = np.ones((5,5))
    imgDil = cv.dilate(canny,kernel,iterations = 1)

    # Get Contours
    getContours(imgDil,imgContour)

    # Stack Images
    imgStack = stackImages(0.8,([frame,canny,grey],[imgDil,imgContour,imgContour]))
    cv.imshow('Video', imgStack)

    # Wait until you press d

    if cv.waitKey(20) & 0xFF == ord('d'):
        break

# Below works for quit code

capture.release()
cv.destroyAllWindows()




