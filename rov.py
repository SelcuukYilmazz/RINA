# Import mavutil
import sys

from pymavlink import mavutil
from  Objects import Rectangle
from Objects import Circle
import process_image
import cv2 as cv
import time

# Create the connection
# master = mavutil.mavlink_connection('udpin:192.168.1.5:10020')

# Wait a heartbeat before sending commands
# master.wait_heartbeat()

# Create a function to send RC values
# More information about Joystick channels
# here: https://www.ardusub.com/operators-manual/rc-input-and-output.html#rc-inputs
# def set_rc_channel_pwm(channel_id, pwm=1500):
#     """ Set RC channel pwm value
#     Args:
#         channel_id (TYPE): Channel ID
#         pwm (int, optional): Channel pwm value 1100-1900
#     """
#     if channel_id < 1 or channel_id > 18:
#         print("Channel does not exist.")
#         return
#
#     # Mavlink 2 supports up to 18 channels:
#     # https://mavlink.io/en/messages/common.html#RC_CHANNELS_OVERRIDE
#     # 0xFFFF = 65535 means 16 bit
#     rc_channel_values = [65535 for _ in range(18)]
#     rc_channel_values[channel_id - 1] = pwm
#     master.mav.rc_channels_override_send(
#         master.target_system,                # target_system
#         master.target_component,             # target_component
#         *rc_channel_values)                  # RC channel list, in microseconds.
#     master.mav.system_time_send(0,0)


def first_mission(capture,door):
    process_image.Rectangle_process(capture, door)

    if door.decent_shape == False:
        if door.upper_corners[0][1] > door.upper_corners[1][1]:
            if door.upper_corners[0][0] < 300:
                print('sola git ve sağa dön')
                # set_rc_channel_pwm(6, 1400)
                # set_rc_channel_pwm(4, 1400)
            elif door.upper_corners[0][0] > 340:
                print('sağa git ve sola dön')
                # set_rc_channel_pwm(6, 1600)
                # set_rc_channel_pwm(4, 1600)
        if door.upper_corners[0][1] < door.upper_corners[1][1]:
            if door.upper_corners[1][0] < 300:
                print('sola git ve sağa dön')
                # set_rc_channel_pwm(6, 1400)
                # set_rc_channel_pwm(4, 1400)
            elif door.upper_corners[1][0] > 340:
                print('sağa git ve sola dön')
                # set_rc_channel_pwm(6, 1600)
                # set_rc_channel_pwm(4, 1600)
    else:

        if len(door.higher_center) > 0:
            if door.higher_center[0] < 300:
                print('yüksek sola kaydır')
                # set_rc_channel_pwm(6, 1400)
            elif door.higher_center[0] > 340:
                print('yüksek sağa kaydır')
                # set_rc_channel_pwm(6, 1600)
            else:
                if door.higher_center[1] < 300:
                    print('yüksek aşağı kaydır')
                elif door.higher_center[1] > 340:
                    print('yüksek yukarı kaydır')
                else:
                    print('hizada yüksek puan')
                    # set_rc_channel_pwm(5, 1600)

        else:
            if len(door.lower_center) > 0:
                if door.lower_center[0] < 300:
                    print('düşük sola kaydır')
                    # set_rc_channel_pwm(6, 1400)
                elif door.lower_center[0] > 340:
                    print('düşük sağa kaydır')
                    # set_rc_channel_pwm(6, 1600)
                else:
                    if door.lower_center[1] < 300:
                        print('düşük aşağı kaydır')
                    elif door.lower_center[1] > 340:
                        print('düşük yukarı kaydır')
                    else:
                        print('hizada düşük puan')
                        # set_rc_channel_pwm(5, 1600)
            else:
                print('kapı bulunamadı aramaya devam ediliyor')


def second_mission(capture,circle):
    process_image.Circle_Process(capture, circle)
    # if len(circle.lock_coordinate)>0:
    #     if circle.lock_coordinate[0]<300:
    #         print("saga git")
    #         set_rc_channel_pwm(6, 1600)
    #     elif circle.lock_coordinate[0]>340:
    #         print("sola git")
    #         set_rc_channel_pwm(6, 1400)
    #     elif circle.lock_coordinate[1]<250:
    #         print("asagi git")
    #     elif circle.lock_coordinate[1]>290:
    #         print("yukari git")
    #     else:
    #         print("hedef ileride")
    #         set_rc_channel_pwm(5, 1600)
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

########################################################################################################################
########################################################################################################################
################################################ Main Code #############################################################

# Variables
door = Rectangle()
circle = Circle()

# Capturing Video From Your Camera
capture = cv.VideoCapture(0)
capture.set(cv.CAP_PROP_FPS, 20)
capture.set(cv.CAP_PROP_FRAME_WIDTH, int(320))
capture.set(cv.CAP_PROP_FRAME_HEIGHT, int(240))
cv.waitKey(10)

# Timer Start
door.Start_time()
circle.Start_time()
while True:
    frame1 = time.time()
    if(sys.argv[1] == "1"):
        first_mission(capture,door)
    if (sys.argv[1] == "2"):
        second_mission(capture,circle)
    frame2 = time.time()
    print("ALL FPS " + str(1/(frame2-frame1)))

    # Wait until you press d
    if cv.waitKey(10) & 0xFF == ord('d'):
        break

########################################################################################################################
# Below works for quit code

capture.release()
cv.destroyAllWindows()
