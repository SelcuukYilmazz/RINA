import numpy as np
import argparse
import cv2 as cv
import time
from pymavlink import mavutil
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal, Vehicle


########################################################################################################################
# Functions
# Arm and Takeoff

def arm_and_takeoff(altitude):

    while not vehicle.is_armable:
        print('waiting to be armable')
        time.sleep(1)

    print('Arming motors')
    vehicle.mode = VehicleMode('GUIDED')
    vehicle.armed = True

    while not vehicle.armed: time.sleep(1)

    print('Taking off')
    vehicle.simple_takeoff(altitude)

    while True:
        v_alt = vehicle.location.global_relative_frame.alt
        print('>> Altitude = %.1f m'%v_alt)
        if v_alt >= altitude - 1.0:
            print('Target altitude reached')
            break
        time.sleep(1)

def clear_mission(vehicle):
    # Clear Current Mission
    cmds = vehicle.commands
    cmds.clear()
    vehicle.flush()

    # Download the Mission Again
    cmds.download()
    cmds.wait_read()

def download_mission(vehicle):
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_read()
def get_current_mission(vehicle):
    # Download the Current Mission, Returns the Number Of Waypoints and the List
    print('Downloading The Mission')
    download_mission(vehicle)
    missionList = []
    n_wp = 0
    for wp in vehicle.commands:
        missionList.append(wp)
        n_wp +=1
    return n_wp,missionList

def add_last_waypoint_to_mission(vehicle,lat ,long ,alt):
    #-- Adds a last waypoint to a mission list
    download_mission()
    cmds = vehicle.commands

    # Save the mission to a temporary list
    missionList = []
    for wp in cmds:
        missionList.append(wp)

    # Append Last Waypoint
    wp_last = Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                      0,0,0,0,0,0,lat,long,alt)
    missionList.append(wp_last)

    # We Clear the Current Mission
    cmds.clear()

    # Write New Mission
    for wp in missionList:
        cmds.add(wp)
    cmds.upload()
    return(cmds.count)

def ChangeMode(vehicle,mode):
    # Change Autopilot Mode
    while vehicle.mode != Vehicle(mode):
        vehicle.mode = VehicleMode(mode)
        time.sleep(0.5)
    return True

# Initialize
gnd_speed = 10
mode = 'GROUND'

# Connect
vehicle = connect('udp:192.168.1.3:14550')

# Main Function
while True:
    if mode == 'GROUND':
        # Wait Until a Valid Mission Has Been Uploaded
        n_wp,missionList = get_current_mission(vehicle)
        time.sleep(2)

        if n_wp > 0:
            print('A Valid Mission Has Been Uploaded: takeoff')
            mode = 'TAKEOFF'
    elif mode == 'TAKEOFF':
        # Add Current Position as Last Waypoint
        add_last_waypoint_to_mission(vehicle,vehicle.location.global_relative_frame.lat,
                                     vehicle.location.global_relative_frame.lon,
                                     vehicle.location.global_relative_frame.alt)
        print('Final Waypoint Added to the Current Mission')
        time.sleep(1)

        # Takeoff

        arm_and_takeoff(10)

        # Change Mode To Auto

        ChangeMode(vehicle,'AUTO')

        # Set the Ground Speed

        vehicle.groundspeed = gnd_speed

        mode = 'MISSION'
        print('Switch to MISSION Mode')

    elif mode == 'MISSION':
        # We monito the mission, when current waypoint is equal to the number of wp
        # We go back home, we clear the mission and land

        # Current                       waypoint ID                 total number
        print('Current WP:%d of %d'%(vehicle.commands.next , vehicle.commands.count))

        if(vehicle.commands.next == vehicle.commands.count):
            print('Final wp reached: go back home')

            # Clear the mission
            clear_mission(vehicle)
            print('Mission Deleted')

            ChangeMode(vehicle,'RTL')

            mode = 'BACK'

    elif mode == 'BACK':
        # When the altitude is below 1, switch to GROUND
        if vehicle.location.global_relative_frame.alt < 1.0:
            print('Vehicle landed , back to GROUND')
            mode = 'GROUND'
    time.sleep(0.5)