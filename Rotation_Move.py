"""
Example of how to use RC_CHANNEL_OVERRIDE messages to force input channels
in Ardupilot. These effectively replace the input channels (from joystick
or radio), NOT the output channels going to thrusters and servos.
"""

# Import mavutil
from pymavlink import mavutil

# Create the connection
master = mavutil.mavlink_connection('udpin:192.168.1.3:10020')
# Wait a heartbeat before sending commands
master.wait_heartbeat()

# Create a function to send RC values
# More information about Joystick channels
# here: https://www.ardusub.com/operators-manual/rc-input-and-output.html#rc-inputs
def set_rc_channel_pwm(channel_id, pwm=1500):
    """ Set RC channel pwm value
    Args:
        channel_id (TYPE): Channel ID
        pwm (int, optional): Channel pwm value 1100-1900
    """
    if channel_id < 1 or channel_id > 18:
        print("Channel does not exist.")
        return

    # Mavlink 2 supports up to 18 channels:
    # https://mavlink.io/en/messages/common.html#RC_CHANNELS_OVERRIDE
    rc_channel_values = [65535 for _ in range(18)]
    rc_channel_values[channel_id - 1] = pwm
    master.mav.rc_channels_override_send(
        master.target_system,                # target_system
        master.target_component,             # target_component
        *rc_channel_values)                  # RC channel list, in microseconds.



while True:
    # # Set some roll
    # set_rc_channel_pwm(2, 1900)
    #
    # #Stop ROV Where It is
    # set_rc_channel_pwm(3,1540)
    #
    # # Go to right
    # set_rc_channel_pwm(6,1900)
    #
    # # Set some yaw to right
    # set_rc_channel_pwm(4, 1900)
    #
    # # Take ROV To Air
    # set_rc_channel_pwm(3,1600)
    #
    # # Take ROV To Depths
    # set_rc_channel_pwm(3,1400)
    #
    # # The camera pwm value is the servo speed
    # # and not the servo position
    # # Set camera tilt to 45º with full speed
    # set_rc_channel_pwm(8, 1900)
    #
    # # Set channel 12 to 1500us
    # # This can be used to control a device connected to a servo output by setting the
    # # SERVO[N]_Function to RCIN12 (Where N is one of the PWM outputs)
    # set_rc_channel_pwm(12, 1500)

    # Roll Sides
    set_rc_channel_pwm(2,1900)

    # Hover Vehicle
    set_rc_channel_pwm(3,1900)

    # Rotate Right
    set_rc_channel_pwm(4,1900)

    # Go Forward
    set_rc_channel_pwm(5,1900)

    # Go Right
    set_rc_channel_pwm(6,1900)
