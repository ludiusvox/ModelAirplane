import busio
import board
import bitbangio
import time
import digitalio
import pulseio

global D11
input_pin = 'D11'
global D12
output_pin = 'D12'
# // static array holding servo data for all channels
# // counter holding the channel being pulse
# // iteration counter used in the interrupt routines;
ISRCount = 0
ChannelCount = 0  # // counter holding the number of attached channels
isStarted = False  # // flag to indicate if the ISR has been initialised
MIN_PULSE_WIDTH = 0
MAX_PULSE_WIDTH = 65535
duty_cycle = 0
servos = pulseio.PWMOUT(board.D5, frequency=5000, duty_cycle=0)
FRAME_SYNC_INDEX = 0
NBR_CHANNELS = 8
servo_t = servos[NBR_CHANNELS+1]
DEFAULT_PULSE_WIDTH = duty_cycle
# // frame sync delay is the first entry in the channel array
FRAME_SYNC_PERIOD = 20000  # // total frame duration in microseconds
FRAME_SYNC_DELAY = ((FRAME_SYNC_PERIOD -
                    (NBR_CHANNELS * DEFAULT_PULSE_WIDTH)) / 128)
# // number of iterations of the ISR to get the desired frame rate
DELAY_ADJUST = time.sleep(.08)
# // number of microseconds of calculation overhead to be subtracted
# from pulse timings
Channel = 0
SPI = bitbangio.SPI(21, MOSI=board.D11, MISO=board.D12)

def ISR():
    ISRCount + 1
    # // increment the overlflow counter
    if (ISRCount == servos[Channel].counter):
        # // are we on the final iteration for this channel{
        TCNT2 = servos[Channel].remainder
        # // yes, set count for overflow after remainder ticks
        return TCNT2

    elif (ISRCount > servos[Channel].counter):
        # // we have finished timing the channel so pulse it low and move on
        if True:
            bitbangio.SPI()
            # // check if activated
            Channel = digitalio.DigitalInOut(board.D12)
            Channel.value = False
            # // pulse this channel low if active
            Channel + 1  # // increment to the next channel
            ISRCount = 0  # // reset the isr iteration counter
            TCNT2 = 0
            # // reset the clock counter register
            return

    if((Channel != FRAME_SYNC_INDEX) and (Channel <= NBR_CHANNELS)):	
        # // check if we need to pulse this channel
        # set correct servo later
        servo1 = pulseio.PWMOUT(board.D5, frequency=5000, duty_cycle=50)
        while True:
            # // check if activated
            Channel = digitalio.DigitalInOut(board.D12)
        Channel.value = True
        return
    elif Channel > NBR_CHANNELS:
        Channel = 0  # // all done so start over
        return
def modservotimer():
    if ChannelCount < NBR_CHANNELS:
        chanIndex = ChannelCount + 1
    # // assign a channel number to this instance
        return
    else:
        chanIndex = 0
    return

    if chanIndex > 0:
        print("attaching chan = ", chanIndex)
        pin = digitalio.DigitalInOut(board.pinio)
        pin.value = True
        servos[chanIndex].board.pin
        # servos[chanIndex].PinA.value = true
        return chanIndex
def writeChan(chan, duty_cycle):
    if((chan > 0) and (chan <= NBR_CHANNELS)):  # // ensure channel is valid
        if duty_cycle < MIN_PULSE_WIDTH:  # // ensure pulse width is valid
            duty_cycle = MIN_PULSE_WIDTH
    elif duty_cycle > MAX_PULSE_WIDTH:
        duty_cycle = MAX_PULSE_WIDTH
        duty_cycle -= DELAY_ADJUST
        #  // subtract the time it takes to process the start and
        # end pulses (mostly from digitalWrite)
    servos[chan].counter = duty_cycle / 128
    servos[chan].remainder = 255 - (2 * (duty_cycle -
                                    (servos[chan].counter * 128)))
    # the number of 0.5us ticks for timer overflow
    return
def modservotimerdetach():  # servos[chanIndex].board.isActive = false
    return

def modsrevotimerwrite(pulsewidth):
    return writeChan(chanIndex, pulsewidth)
    # // call the static function to store the data for this servo


def modservotimerread():
    return


def modservotimerattached():
    # return servos[chanIndex].busio.pinio.value
    return
def initISR():
    for i in (1, NBR_CHANNELS):
        writeChan(i, DEFAULT_PULSE_WIDTH)
        servos[FRAME_SYNC_INDEX].counter = FRAME_SYNC_DELAY
        # // store the frame sync period
        Channel = 0  # // clear the channel index
        ISRCount = 0  # // clear the value of the ISR counter;

        # /* setup for timer 2 */
        # TIMSK2 = 0  // disable interrupts
        # TCCR2A = 0  // normal counting mode
        # TCCR2B = _BV(CS21) // set prescaler of 8
        # TCNT2 = 0     // clear the timer2 count
        # TIFR2 = _BV(TOV2)  // clear pending interrupts;
        # TIMSK2 =  _BV(TOIE2) // enable the overflow interrupt

        isStarted = True  # // flag to indicate this initialisation code has been executed