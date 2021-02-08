import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv

#Functions
def getContours(img,imgContour):
    contours,hierarchy = cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 2000:
            cv.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            corner = cv.arcLength(cnt,True)
            approx = cv.approxPolyDP(cnt,0.02*corner,True)
            print(len(approx))
            x,y,w,h = cv.boundingRect(approx)
            cv.rectangle(imgContour,(x , y ),(x + w , y + h ),(0,255,0),5)
            cv.putText(imgContour,'Points: ' + str(len(approx)),(x + w + 20, y + 20), cv.FONT_HERSHEY_DUPLEX,.7,(0,255,0),2)
            cv.putText(imgContour,'Area: ' + str(int(area)), (x + w + 20,y+45),cv.FONT_HERSHEY_DUPLEX,0.7,(0,255,0),2)

def empty(a):
    pass

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvaliable = isinstance(imgArray[0],list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvaliable:
        for x in range (0,rows):
            for y in range (0,cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv.resize(imgArray[x][y],(0,0),None,scale,scale)
                else:
                    imgArray[x][y] = cv.resize(imgArray[x][y],(imgArray[0][0].shape[1],imgArray[0][0].shape[0]),None,scale,scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv.cvtColor(imgArray[x][y],cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height,width,3),np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0,rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
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


#Interface
cv.namedWindow('Parameters')
cv.resizeWindow('Parameters',640,240)
cv.createTrackbar('Threshold1','Parameters',75,255,empty)
cv.createTrackbar('Threshold2','Parameters',64,255,empty)

#Video Capture from your camera

capture = cv.VideoCapture(0)

while True:
    isTrue,frame = capture.read()

    #Input Taken From Trackbar to Thresholds
    threshold1 = cv.getTrackbarPos('Threshold1','Parameters')
    threshold2 = cv.getTrackbarPos('Threshold2','Parameters')

    #Variable
    imgContour = frame.copy()

    # Blur

    blur = cv.GaussianBlur(frame,(7,7),1)

    # Grey Filter

    grey = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)

    # Canny Edge Detector

    canny = cv.Canny(grey,threshold1,threshold2)

    #Dilation Function
    kernel = np.ones((5,5))
    imgDil = cv.dilate(canny,kernel,iterations = 1)

    #Get Contours
    getContours(imgDil,imgContour)

    #Stack Images
    imgStack = stackImages(0.8,([frame,canny,grey],[imgDil,imgContour,imgContour]))
    cv.imshow('Video', imgStack)

    # Wait until you press d

    if cv.waitKey(20) & 0xFF == ord('d'):
        break

#Below works for quit code

capture.release()
cv.destroyAllWindows()




