from Objects import Rectangle
from Objects import Circle
import process_image
import cv2 as cv
import time
import Objects

def second_mission(capture,circle):
    process_image.Circle_Process(capture, circle)
    if len(circle.lock_coordinate)>0:
         if circle.lock_coordinate[0]<300:
             print("saga git")
             #set_rc_channel_pwm(6, 1600)
         elif circle.lock_coordinate[0]>340:
             print("sola git")
             #set_rc_channel_pwm(6, 1400)
         elif circle.lock_coordinate[1]<250:
             print("asagi git")
         elif circle.lock_coordinate[1]>290:
             print("yukari git")
         else:
             print("hedef ileride")
             #set_rc_channel_pwm(5, 1600)
    print(circle.lock_coordinate)

# Trackbar Interface
cv.namedWindow('Parameters')
cv.resizeWindow('Parameters', 640, 640)
cv.createTrackbar('Threshold1', 'Parameters', 79, 255, process_image.empty)
cv.createTrackbar('Threshold2', 'Parameters', 55, 255, process_image.empty)
cv.createTrackbar('HUE Min', 'Parameters', 0, 179, process_image.empty)
cv.createTrackbar('HUE Max', 'Parameters', 100, 179, process_image.empty)
cv.createTrackbar('SAT Min', 'Parameters', 73, 255, process_image.empty)
cv.createTrackbar('SAT Max', 'Parameters', 173, 255, process_image.empty)
cv.createTrackbar('VALUE Min', 'Parameters', 0, 255, process_image.empty)
cv.createTrackbar('VALUE Max', 'Parameters', 255, 255, process_image.empty)

circle = Circle()

capture = cv.VideoCapture(0)
capture.set(cv.CAP_PROP_FPS, 20)
capture.set(cv.CAP_PROP_FRAME_WIDTH, int(320))
capture.set(cv.CAP_PROP_FRAME_HEIGHT, int(240))

# Timer Start

circle.Start_time()
while True:
    if objects.move == True:
        scan.scanning()
    frame1 = time.time()
    # first_mission(capture,door)
    second_mission(capture,circle)
    frame2 = time.time()
    #print("ALL FPS " + str(1/(frame2-frame1)))

    # Wait until you press d
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

########################################################################################################################
# Below works for quit code

capture.release()
cv.destroyAllWindows()
