

class SoftwareServo(pin, angle, pulse0, min16, max16):
    # pin
    # angle       // in degrees
    # pulse0     // pulse width in TCNT0 counts
    # min16       // minimum pulse, 16uS units  (default is 34)
    # max16       // maximum pulse, 16uS units, 0-4ms range (default is 150)
    def refresh():
        return
SoftwareServo()
attach(int)  # // attach to a pin, sets pinMode, returns 0 on failure, won't
# // position the servo until a subsequent write() happens
detach()
write(int)
read()
attached()
setMinimumPulse(int)
setMaximumPulse(int)
refresh()