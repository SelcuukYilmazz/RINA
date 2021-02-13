import numpy as np
import argparse
import cv2 as cv
import time
from pymavlink import mavutil
import sys

# Import mavutil
from pymavlink import mavutil

master = mavutil.mavlink_connection('udpin:192.168.1.3:10020',baud=115200)
master.wait_heartbeat()

# https://mavlink.io/en/messages/common.html#MAV_CMD_COMPONENT_ARM_DISARM

# Arm
# master.arducopter_arm() or:
while True:
    command = int(input('command : '))
    if command == 1 :
        master.mav.command_long_send(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            1, 0, 0, 0, 0, 0, 0)

    elif command == 0 :
        master.mav.command_long_send(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            0, 0, 0, 0, 0, 0, 0)

