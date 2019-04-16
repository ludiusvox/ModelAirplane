# Note that analogWrite of PWM on pins 3 and 11
# is disabled when the first servo is attached
# The methods are:
# ServoTimer2 - Class for manipulating servo motors connected to Arduino pins.
# attach(pin )  - Attaches a servo motor to an i/o pin.
# attach(pin, min, max  ) - Attaches to a pin setting
# min and max values in microseconds
# default min is 544, max is 2400
import modservotimer.py
import array
MIN_PULSE_WIDTH = 750	
MAX_PULSE_WIDTH = 2250	
DEFAULT_PULSE_WIDTH = 1500
FRAME_SYNC_PERIOD = 20000
NBR_CHANNELS = 8

nbr = array.nbr(0, 31)  # // a pin number from 0 to 31
isActive = ''
ServoPin_t = ''
byte_counter = ''
byte_remainder = ''
servo_t = ''

class modservo():
    def moderservotimer():

        return

    def modservotimerattach():
        return

    def modservotimerattach1():
        return

    def modservotimerdetach():
        return

    def modservotimerwrite():
        return

    def modservotimerread():
        return

    def modservotimerattached():
        return
