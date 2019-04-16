import VirtualWire.py
import VirtualWireA.py
import board
import busio
import time
from analogio import AnalogIn
import array
numberOfAnalogPins = 4
data = numberOfAnalogPins
dataBytes = numberOfAnalogPins * 8
analogin = AnalogIn(board.A1)

def GetVoltage(pin):
    return (pin.value * 3.3) / 65536  # hookup board to test

def setup():
    VirtualWire.vw_tx_pin(12)
    busio.UART(board.TX, board.RX, baudrate=9600)
    print("setup")
    VirtualWire.vw_set_ptt_inverted.Value = True
    VirtualWireA.setup_vw.Value = True
    return
def loop():

    for i in range(0, numberOfAnalogPins):
        data[i] = array.analogRead(i)
def send(data, databytes):
    time.sleep(1)
    return
