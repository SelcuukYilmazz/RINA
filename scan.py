from pymavlink import mavutil
import datetime

def scanning():

    start = datetime.datetime.now()
    #depth
    if start<=2:
        set_rc_channel_pwm(3, 1400)
        start = 0



    start = datetime.datetime.now()
    #forward
    if start-2<=0:
        set_rc_channel_pwm(5,1900)
        start = 0

    start = datetime.datetime.now()
    #roll
    if start<=3:
        set_rc_channel_pwm(4,1200)
        start = 0

    # forward
    if start - 2 <= 0:
        set_rc_channel_pwm(5, 1900)
        start = 0