import sys
from pymavlink import mavutil
from threading import Thread
from  Objects import Rectangle
from Objects import Circle
import process_image
import cv2 as cv
import time


# Create the connection
# master = mavutil.mavlink_connection('udpin:10.42.0.1:10020')
#
# Wait a heartbeat before sending commands
# master.wait_heartbeat()
#
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
# #     # Mavlink 2 supports up to 18 channels:
# #     # https://mavlink.io/en/messages/common.html#RC_CHANNELS_OVERRIDE
# #     # 0xFFFF = 65535 means 16 bit
#     rc_channel_values = [65535 for _ in range(18)]
#     rc_channel_values[channel_id - 1] = pwm
#     master.mav.rc_channels_override_send(
#         master.target_system,                # target_system
#         master.target_component,             # target_component
#         *rc_channel_values)                  # RC channel list, in microseconds.
#     master.mav.system_time_send(0,0)

class VideoWriterWidget(object):
    def __init__(self):
        # Create a VideoCapture objectw
        self.capture = cv.VideoCapture(0)


        # Default resolutions of the frame are obtained (system dependent)
        # Start the thread to read frames from the video stream
        door = Rectangle()
        circle = Circle()
        door.Start_time()
        circle.Start_time()
        # Start another thread to show/save frames
        self.start_recording(door,circle)
        # Read the next frame from the stream in a different thread
        # Timer Start

        while True:

            self.status, frame = self.capture.read()
            if (sys.argv[1] == "1"):
                self.first_mission(door,frame)
            if (sys.argv[1] == "2"):
                self.second_mission(circle,frame)
            # Wait until you press d
            if cv.waitKey(10) & 0xFF == ord('d'):
                break

            ########################################################################################################################
            # Below works for quit code

        self.capture.release()
        cv.destroyAllWindows()

    def start_recording(self,door,circle):
        # Create another thread to show/save frames
        scanning_thread = Thread(target=self.scanning,args=[door,circle])
        scanning_thread.start()





    def scanning(self,door,circle):
        initialize_time = time.time()
        current_time = time.time()

        while current_time - initialize_time<=5:
            current_time = time.time()
            #depth
            if circle.lock != True and door.lock != True:
                if current_time - initialize_time<= 2:
                    self.move(3,1400)
                    print("aşağı scan")
                #forward
                elif current_time - initialize_time <= 4:
                    self.move(5,1900)
                    print("ileri scan")
                #yaw
                elif current_time - initialize_time <= 5:
                    self.move(4,1200)
                    print("dönüş scan")



    def move(self,channel, power):
        pass
        # set_rc_channel_pwm(channel, power)

    def first_mission(self,door,frame):
        process_image.Rectangle_process(frame, door)

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

    def second_mission(self,circle,frame):
        process_image.Circle_Process(circle,frame)
        if len(circle.lock_coordinate)>0:
            if circle.lock_coordinate[0]<300:
                print("saga git")
                # set_rc_channel_pwm(6, 1600)
            elif circle.lock_coordinate[0]>340:
                print("sola git")
                # set_rc_channel_pwm(6, 1400)
            elif circle.lock_coordinate[1]<250:
                print("asagi git")
            elif circle.lock_coordinate[1]>290:
                print("yukari git")
            else:
                print("hedef ileride")
                # set_rc_channel_pwm(5, 1600)
        print(circle.lock_coordinate)

# Trackbar Interface
cv.namedWindow('Parameters')
cv.resizeWindow('Parameters', 1000,1000)
cv.createTrackbar('Threshold1', 'Parameters', 30, 255, process_image.empty)
cv.createTrackbar('Threshold2', 'Parameters', 19, 255, process_image.empty)
cv.createTrackbar('HUE Min', 'Parameters', 0, 360, process_image.empty)
cv.createTrackbar('HUE Max', 'Parameters', 100, 360, process_image.empty)
cv.createTrackbar('SAT Min', 'Parameters', 73, 255, process_image.empty)
cv.createTrackbar('SAT Max', 'Parameters', 173, 255, process_image.empty)
cv.createTrackbar('VALUE Min', 'Parameters', 0, 255, process_image.empty)
cv.createTrackbar('VALUE Max', 'Parameters', 255, 255, process_image.empty)
cv.createTrackbar('Brightness', 'Parameters',255, 2 * 255,process_image.empty)
cv.createTrackbar('Contrast', 'Parameters',127, 2 * 127,process_image.empty)

########################################################################################################################
########################################################################################################################
################################################ Main Code #############################################################

# Variables


VideoWriterWidget()

