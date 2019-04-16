
import VirtualWire.py as vw
from analogio import AnalogIn
import time
from digitaio import DigitalInOut, Direction
import board
import busio
numberOfAnalogPins = 4
data = ''
sizeof = 80
data[numberOfAnalogPins]
databytes = numberOfAnalogPins * sizeof(int)

def setup():
    button1 = DigitalInOut(board.A1)
    button1.direction = Direction.OUTPUT
    vw.vw_set_ptt_inverted(True)
    uart = busio.UART(board.TX, board.RX, Baudrate=9600)

def loop():
    for i in (0, numberOfAnalogPins):
        data[i] = AnalogIn(board.D5)
    vw.vw_send(data, 80)
    time.sleep(1)  # //send every second
    return

def send(data, databytes):
    vw.vw_send(data, databytes)
    vw.vw_wait_tx()  # // Wait until the whole message is gone
