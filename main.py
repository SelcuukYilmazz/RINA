import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv

# Functions

#Find Contours

def find_Contour(src):


    # Threshold
    ret,thresh = cv.threshold(src,127,255,0)

    # Find Contours
    return


#Video Capture from your camera

capture = cv.VideoCapture(0)

print(cv.waitKey(20)&0xFF)
print(ord('d'))
while True:
    isTrue,frame = capture.read()

    #Resize Video

    dimensions=(450,450)
    frame = cv.resize(frame,dimensions,interpolation=cv.INTER_AREA)

    # Create Blank Window

    blank = np.zeros(frame.shape,dtype='uint8')
    cv.imshow('Blank',blank)

    # Grey Filter
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('Video', frame)

    # Draw Rectangle

    cv.rectangle(frame, (frame.shape[1] // 6, frame.shape[0] // 6),
                 ((frame.shape[1] // 6) * 5, (frame.shape[0] // 6) * 5), (0, 0, 255), 3)
    cv.imshow('Video', frame)

    #Edge Cascade
    canny= cv.Canny(frame,125,175)
    cv.imshow('Edges',canny)

    #Find Contours

    contours, hierarchy = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    print(str(len(contours))+" Contours Found!")

    #Draw Contours on Blank Window

    cv.drawContours(blank,contours,-1,(0,255,0),2)
    cv.imshow('Contours Screen',blank)

    # Wait until you press d

    if cv.waitKey(20) & 0xFF == ord('d'):
        break


#Below works for quit code

capture.release()
cv.destroyAllWindows()




