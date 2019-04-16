import modservotimer
import modservotimerh1
import Virtualwire as vw
import modservotimerh
import time
import busio
import board
import array as arr
modservotimerh1.modservotimer.myservo1

modservotimerh1.modservotimer.myservo2
modservotimerh1.modservotimer.myservo3
modservotimerh1.modservotimer.myservo4
uart = busio.UART(board.TX, board.RX, baudrate=9600)
numberOfAnalogPins = 4  # // how many analog integer values to receive
data = 4 * arr.array()  # // the data buffer
value = 4 * arr.array1()
# // the number of bytes in the data buffer
dataBytes = numberOfAnalogPins * 32
msgLength = dataBytes

def setup():
    # set output correctly
    myservo1.modservotimerattach(9)  # //Propeller
    myservo2.modservotimerattach(10)  # //Rudder
    myservo3.modservotimerattach(8)  # // Ailron
    myservo4.modservotimerattach(12)  # // Elevator
    while True:
        data = busio.UART.read(32)
    if data is not None:
        print(data)

    # Initialize the IO and ISR
    vw.vw_set_ptt_inverted(True)
    vw.vw_set_rx_pin(11)
    vw.vw_rx_start()  # // Start the receiver
    vw.vx_set(2000)
def loop():
    if vw.vw_get_message(data, msgLength):
        if data is not None:
            print("Got: " + data)
        if(msgLength == dataBytes):
            for i in (1, numberOfAnalogPins):
                value[0] = map(data[0], 0, 1023, 1000, 2000)
                value[i] = map(data[i], 0, 1023, 0, 179)
                #  // Write into the servo
                return
    return
modservotimer.myservo1.write(value[0])
modservotimer.myservo2.write(value[1])
modservotimer.myservo3.write(value[2])
modservotimer.myservo4.write(value[3])
time.sleep(.5)
modservotimerh.refresh() # //refresh the servo
