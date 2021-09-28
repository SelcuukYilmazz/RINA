import sys
from pymavlink import mavutil
from threading import Thread
from  Objects import Rectangle
from Objects import Circle
from dronekit import *
import process_image
import cv2 as cv
import time

vehicle = connect('udp:10.42.0.243:14550', wait_ready=True)



class MainThread(object):

    # ARACI ÇALIŞTIRMAK İÇİN YORUMDAN ÇIKAR
    def arm_and_takeoff(self,aTargetAltitude):
        # """
        # Arms vehicle and fly to aTargetAltitude.
        # """
        #
        # print("Basic pre-arm checks")
        # # Don't try to arm until autopilot is ready
        # while not vehicle.is_armable:
        #     print(" Waiting for vehicle to initialise...")
        #     time.sleep(1)
        #
        # print("Arming motors")
        # # Copter should arm in GUIDED mode
        # vehicle.mode = VehicleMode("GUIDED")
        # vehicle.armed = True
        #
        # # Confirm vehicle armed before attempting to take off
        # while not vehicle.armed:
        #     print(" Waiting for arming...")
        #     time.sleep(1)
        #
        # print("Taking off!")
        # vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude
        #
        # # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
        # #  after Vehicle.simple_takeoff will execute immediately).
        # while True:
        #     print(" Altitude: "+ vehicle.location.global_relative_frame.alt)
        #     # Break and return from function just below target altitude.
        #     if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
        #         print("Reached target altitude")
        #         break
        #     time.sleep(1)
        pass
    # ARACI ÇALIŞTIRMAK İÇİN YORUMDAN ÇIKAR
    def send_ned_velocity(self,velocity_x, velocity_y, velocity_z, yaw_velocity, duration):
        # """
        # Move vehicle in direction based on specified velocity vectors.
        # """
        # msg = vehicle.message_factory.set_position_target_local_ned_encode(
        #     0,  # time_boot_ms (not used)
        #     0, 0,  # target system, target component
        #     mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
        #     0b0000111111000111,  # type_mask (only speeds enabled)
        #     0, 0, 0,  # x, y, z positions (not used)
        #     velocity_x, velocity_y, velocity_z,  # x, y, z velocity in m/s
        #     0, 0, 0,  # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        #     yaw_velocity, 0)  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
        #
        # # send command to vehicle on 1 Hz cycle
        # for x in range(0, duration):
        #     vehicle.send_mavlink(msg)
        #     time.sleep(1)
        pass

    def __init__(self):
        # Create a VideoCapture objectw
        self.capture = cv.VideoCapture(0)
        self.capture.set(cv.CAP_PROP_FRAME_WIDTH,320)
        self.capture.set(cv.CAP_PROP_FRAME_HEIGHT,240)

        # Default resolutions of the frame are obtained (system dependent)
        # Start the thread to read frames from the video stream
        door = Rectangle()
        circle = Circle()
        door.Start_time()
        circle.Start_time()
        # Start another thread to show/save frames
        scanning_thread = Thread(target=self.scanning, args=[door, circle])
        scanning_thread.start()
        # Read the next frame from the stream in a different thread
        # Timer Start

        if (sys.argv[1]=="1"):
            self.TrackbarCreator(30, 19, 97, 129, 0, 44, 175, 227, 255, 127)
        elif (sys.argv[1] == "2"):
            self.TrackbarCreator(30, 19, 96, 132, 16, 86, 51, 123, 255, 127)
        while True:
            self.status, frame = self.capture.read()
            if (sys.argv[1] == "1"):
                self.first_mission(door,frame)
            elif (sys.argv[1] == "2"):
                self.second_mission(circle,frame)
            # Wait until you press d
            if cv.waitKey(10) & 0xFF == ord('d'):
                break

            ########################################################################################################################
            # Below works for quit code

        self.capture.release()
        cv.destroyAllWindows()

    def scanning(self,door,circle):
        initialize_time = time.time()
        current_time = time.time()

        while current_time - initialize_time<=10 and circle.lock != True and door.lock != True:
            current_time = time.time()
            # Vehicle taking off target altitude
            self.arm_and_takeoff(-20)
            print("asagı scan")

            #forward
            print("ileri scan")
            self.send_ned_velocity(0,0,10,4)

            #yaw
            self.send_ned_velocity(0,0,0,10,2)
            print("donus scan")

    def first_mission(self,door,frame):
        process_image.Rectangle_process(frame, door)

        if door.decent_shape == False:
            if door.upper_corners[0][1] > door.upper_corners[1][1]:
                if door.upper_corners[0][0] < 300:
                    print('sola git ve saga don')
                    # set_rc_channel_pwm(6, 1400)
                    # set_rc_channel_pwm(4, 1400)
                elif door.upper_corners[0][0] > 340:
                    print('saga git ve sola don')
                    # set_rc_channel_pwm(6, 1600)
                    # set_rc_channel_pwm(4, 1600)
            if door.upper_corners[0][1] < door.upper_corners[1][1]:
                if door.upper_corners[1][0] < 300:
                    print('sola git ve saga don')
                    # set_rc_channel_pwm(6, 1400)
                    # set_rc_channel_pwm(4, 1400)
                elif door.upper_corners[1][0] > 340:
                    print('saga git ve sola don')
                    # set_rc_channel_pwm(6, 1600)
                    # set_rc_channel_pwm(4, 1600)
        else:

            if len(door.higher_center) > 0:
                if door.higher_center[0] < 300:
                    print('yuksek sola kaydir')
                    # set_rc_channel_pwm(6, 1400)
                elif door.higher_center[0] > 340:
                    print('yuksek saga kaydir')
                    # set_rc_channel_pwm(6, 1600)
                else:
                    if door.higher_center[1] < 300:
                        print('yuksek asagi kaydir')
                    elif door.higher_center[1] > 340:
                        print('yuksek yukari kaydir')
                    else:
                        print('hizada yuksek puan')
                        # set_rc_channel_pwm(5, 1600)

            else:
                if len(door.lower_center) > 0:
                    if door.lower_center[0] < 300:
                        print('dusuk sola kaydir')
                        # set_rc_channel_pwm(6, 1400)
                    elif door.lower_center[0] > 340:
                        print('dusuk saga kaydir')
                        # set_rc_channel_pwm(6, 1600)
                    else:
                        if door.lower_center[1] < 300:
                            print('dusuk asagi kaydir')
                        elif door.lower_center[1] > 340:
                            print('dusuk yukari kaydir')
                        else:
                            print('hizada dusuk puan')
                            # set_rc_channel_pwm(5, 1600)
                else:
                    print('kapi bulunamadi aramaya devam ediliyor')


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

    def TrackbarCreator(self,defaultTh1,defaultTh2,defaultHueMin,defaultHueMax,defaultSatMin,defaultSatMax,
                        defaultValueMin,defaultValueMax,defaultBrightness,defaultContrast):
        cv.namedWindow('Parameters')
        cv.resizeWindow('Parameters', 1000, 1000)
        cv.createTrackbar('Threshold1', 'Parameters', defaultTh1, 255, process_image.empty)
        cv.createTrackbar('Threshold2', 'Parameters', defaultTh2, 255, process_image.empty)
        cv.createTrackbar('HUE Min', 'Parameters', defaultHueMin, 360, process_image.empty)
        cv.createTrackbar('HUE Max', 'Parameters', defaultHueMax, 360, process_image.empty)
        cv.createTrackbar('SAT Min', 'Parameters', defaultSatMin, 255, process_image.empty)
        cv.createTrackbar('SAT Max', 'Parameters', defaultSatMax, 255, process_image.empty)
        cv.createTrackbar('VALUE Min', 'Parameters', defaultValueMin, 255, process_image.empty)
        cv.createTrackbar('VALUE Max', 'Parameters', defaultValueMax, 255, process_image.empty)
        cv.createTrackbar('Brightness', 'Parameters', defaultBrightness, 2 * 255, process_image.empty)
        cv.createTrackbar('Contrast', 'Parameters', defaultContrast, 2 * 127, process_image.empty)

MainThread()

