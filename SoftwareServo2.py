import time
from board import SCL, SDA
import busio

from adafruit_metrom0 import metrom0
from adafruit_motor import servo

i2c = busio.I2C(SCL, SDA)

metrom0 = metrom0(i2c)

metrom0.frequency = 50

servo7 = servo.ContinuousServo(metrom0.channels[7])

print("forwards")
servo7.throttle = 1
time.sleep(.1)

print("backwards")
servo7.throttle = -1

print("stop")
servo7.throttle = 0

metrom0.deinit()