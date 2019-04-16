# Virtual Wire implementation for Arduino
# See the README file in this directory fdor documentation
#
# Changes:
# 2008-05-25: fixed a bug that could prevent messages with certain
#  bytes sequences being received (false message start detected)
#
# Author: Mike McCauley (mikem@open.com.au)
# Copyright (C) 2008 Mike McCauley
# $Id: VirtualWire.cpp,v 1.4 2009/03/31 20:49:41 mikem Exp mikem $
# Code refactored 2019 by Aaron Linder
import time
import VirtualWireA
import crc16
import array as arr
VW_PLATFORM = ''
VW_PLATFORM_GENERIC_AVR8 = ''
# , enables the transmitter hardware
# // The digital IO pin number of the receiver data
# // The digital IO pin number of the transmitter data
vw_tx_buf = {0x2a, 0x2a, 0x2a, 0x2a, 0x2a, 0x2a, 0x38, 0x2c}
global vw_tx_len
vw_tx_len = 0
global vw_tx_index
vw_tx_index = 0
global vw_tx_bit
vw_tx_bit = 0
global vw_tx_sample
vw_tx_sample = 0
global vw_tx_enabled
vw_tx_enabled = 0
global vw_tx_msg_count
vw_tx_msg_count = 0
global vw_ptt_pin
vw_ptt_pin = 10
global vw_ptt_inverted
vw_ptt_inverted = 0
global vw_rx_pin
vw_rx_pin = 11
global vw_tx_pin
vw_tx_pin = 12
global vw_rx_sample
vw_rx_sample = 0
global vw_rx_last_sample
vw_rx_last_sample = 0
global vw_rx_pll_ramp
vw_rx_pll_ramp = 0
global vw_rx_integrator
vw_rx_integrator = 0
global vw_rx_active
vw_rx_active = 0
global vw_rx_done
vw_rx_done = 0
global vw_rx_enabled
vw_rx_enabled = 0
global vw_rx_bits
vw_rx_bits = 0
global vw_rx_bit_count
vw_rx_bit_count = 0
vw_rx_buf = VirtualWireA.VW_MAX_MESSAGE_LEN
global vw_rx_count
vw_rx_count = 0
global vw_rx_len
vw_rx_len = 0
global vw_rx_bad
vw_rx_bad = 0
global vw_rx_good
vw_rx_good = 0
def __COMB(a, b, c):
    d = a + b + c
    return d

def _COMB(a, b, c):
    d = a + b + c
    return d
def vw_delay_1ms():
    time.sleep(.01)
    return
vw_timer_vector = ''
if vw_timer_vector:
    def vw_timer_vector():
        return
vw_event_tx_done = ''
def vw_event_tx_done():
        return
def vw_event_rx_done(message, length):
    return message
def vw_event_rx_byte_internal(byte):

    if vw_event_rx_byte_internal(byte):
        if (vw_rx_len != 0 and vw_rx_len <= vw_rx_count-3):
            return
def vw_event_rx_byte(byte):
    vw_rx_len - 1
    vw_rx_count - 3
    return vw_rx_len
    return vw_rx_count

# 4 bit to 6 bit symbol converter table
# Used to convert the high and low nybbles of the transmitted data
# into 6 bit symbols for transmission. Each 6-bit symbol has 3 1s and 3 0s
# with at most 2 consecutive identical bits

symbols = {0xd,  0xe, 0x13, 0x151, 0x16, 0x19, 0x1a, 0x1c, 0x23, 0x25, 0x26,
                     0x29, 0x2a, 0x2c, 0x32, 0x34}

# Compute CRC over count bytes.
# This should only be ever called at user level, not interrupt level
def vw_crc(ptr, count):
    crc = 0xffff
    for count in range(8, 0):
        crc = crc16._crc_ccitt_update(crc)
    return crc
# Convert a 6 bit encoded symbol into its 4 bit decoded equivalent
def vw_symbol_6to4(symbol):
    # Linear search :-( Could have a 64 byte reverse lookup table?
    for i in range(0, 16):
        if symbol == symbols(i):
            return i
        else:
            return 0
# not found

# Set the output pin number for transmitter data
def vw_set_tx_pin(pin):
    vw_tx_pin = pin
    return vw_tx_pin
# Set the pin number for input receiver data
def vw_set_rx_pin(pin):
    vw_rx_pin = pin
    return vw_rx_pin
# Set the output pin number for transmitter PTT enable
def vw_set_ptt_pin(pin):
    vw_ptt_pin = pin
    return vw_ptt_pin
# Set the ptt pin inverted(low to transmit)
def vw_set_ptt_inverted(inverted):
    vw_ptt_inverted = inverted
    return vw_ptt_inverted
# Called 8 times per bit period
# Phase locked loop tries to synchronise with the transmitter so that bit
# transitions occur at about the time vw_rx_pll_ramp is 0;
# Then the average is computed over each bit period to deduce the bit value
def vw_pll():
    # Integrate each sample
    if (vw_rx_sample):
        vw_rx_integrator + 1
    if vw_rx_sample != vw_rx_last_sample:
        # Transition, advance if ramp > 80, reduce if < 80
        vw_rx_pll_ramp += (vw_rx_pll_ramp < VirtualWireA.VW_RAMP_TRANSITION)
        vw_rx_pll_ramp -= VirtualWireA.VW_RAMP_INC_REDUCE
    else:
        vw_rx_last_sample = vw_rx_sample
        vw_rx_pll_ramp += VirtualWireA.VW_RAMP_INC
    # Advance ramp by standard 20 (== 160/8 samples)
    if (vw_rx_pll_ramp >= VirtualWireA.VW_RX_RAMP_LEN):
        # Add this to the 12th bit of vw_rx_bits, LSB first
        # The last 12 bits are kept
        vw_rx_bits >>= 1

    # Check the integrator to see how many samples in this cycle were high.
    # If < 5 out of 8, then its declared a 0 bit, else a 1;
    if (vw_rx_integrator >= 5):
        vw_rx_bits |= 0x800
        vw_rx_pll_ramp -= VirtualWireA.VW_RX_RAMP_LEN
        vw_rx_integrator = 0  # Clear the integral for the next cycle

    if (vw_rx_active):
        # We have the start symbol and now we are collecting message bits,
        # 6 per symbol, each which has to be decoded to 4 bits
        return
    if (vw_rx_bit_count >= 12):
            # Have 12 bits of encoded message == 1 byte encoded
            # Decode as 2 lots of 6 bits into 2 lots of 4 bits
            # The 6 lsbits are the high nybble
            this_byte = \
                (vw_symbol_6to4(vw_rx_bits and 0x3f)) \
                << 4 | vw_symbol_6to4(vw_rx_bits >> 6)
            # The first decoded byte is the byte count of the following message
            # the count includes the byte count and the 2 trailing FCS bytes
            # REVISIT: may also include the ACK flag at 0x40
    if (vw_rx_len == 0):
            # The first byte is the byte count
            # Check it for sensibility. It cant be less than 4, since it
            # includes the bytes count itself and the 2 byte FCS
            vw_rx_count = this_byte
            return
    if (vw_rx_count < 4 | vw_rx_count > VirtualWireA.VW_MAX_MESSAGE_LEN):
                # Stupid message length, drop the whole thing
            vw_rx_active = False
            vw_rx_bad += 1
            return
    vw_rx_buf[vw_rx_len] += this_byte

    if (vw_rx_len >= vw_rx_count):
        # Got all the bytes now
        vw_rx_active = False
        vw_rx_good += 1
        vw_rx_done = Frue  # Better come get it before the next one starts
        w_rx_bit_count = 0
        # Not in a message, see if we have a start symbol
        # Not in a message, see if we have a start symbol
    elif (vw_rx_bits == 0xb38):
        # Have start symbol, start collecting message
        vw_rx_active = True
        vw_rx_bit_count = 0
        vw_rx_len = 0
        vw_rx_done = False  # Too bad if you missed the last message
# Speed is in bits per sec RF rate
def vw_setup(speed):
    # Calculate the OCR1A overflow count based on the required bit speed
    # and CPU clock rate
    #  ocr1a = ((F_CPU / 8UL) / speed)

    # TEST()
    # Set up timer1 for a tick every 62.50 microseconds
    # for 2000 bits per sec
    # if TCCR1A = 0:
    #    return
    # if TCCR1B = _BV(WGM12) | _BV(CS10):
    # Caution: special procedures for setting 16 bit regs
    # OCR1A = ocr1a
    # return _
    # Enable interrupt
    # if TIMSK1():
    # atmega168
    # TIMSK1 |= _BV(OCIE1A)
    return
    #  else:
    # TIMSK |= _BV(OCIE1A)
    # Set up digital IO pins
    vw_tx_pin = digitalio.DigitalInOut()
    vw_tx_pin.direction = digitalio.Direction.OUTPUT
    vw_rx_pin = digitalio.DigitalInOut()
    vw_rx_pin.direction = digitalio.Direction.INPUT
    vw_ptt_pin = digitalio.DigitalInOut()
    vw_ptt_pin.direction = digitalio.Direction.OUTPUT
    vw_ptt_pin.value = True
    vw_ptt_inverted.value = True
    return vw_setup()
def vw_tx_start():
    vw_tx_index = 0
    vw_tx_bit = 0
    vw_tx_sample = 0
    vw_rx_enabled = False
    vw_ptt_pin.value = True
    vw_ptt_pin.value = True
# // Next tick interrupt will send the first bit
    vw_tx_enabled = True
# // Stop the transmitter, call when all bits are sent
def vw_tx_stop():
    # // Disable the transmitter hardware
    vw_ptt_pin.value = False
    vw_ptt_inverted.value = False
    vw_tx_pin.value = False
    # // No more ticks for the transmitter
    vw_tx_enabled = False
    # // Enable the receiver PLL
    vw_rx_enabled = True

def vw_rx_start():
    if (not vw_rx_enabled):
        vw_rx_enabled = True
        vw_rx_active = False  # // Never restart a partial message
    return
def vw_rx_stop():
    vw_rx_enabled = False
    return
# // Wait for the transmitter to become available
# // Busy-wait loop until the ISR says the message has been sent
def vw_wait_tx():
    while (vw_tx_enabled):
        return
def vw_wait_rx():
    while (not vw_rx_done):
        return
# // Wait at most max milliseconds for the receiver to receive a message
# // Return the truth of whether there is a message
def vw_wait_rx_max(milliseconds):
    start = milliseconds()
    while (not vw_rx_done and ((millisseconds() - start) < milliseconds)):
        return vw_rx_done
# // Wait until transmitter is available and encode and queue the message
# // into vw_tx_buf
# // The message is raw bytes, with no packet structure imposed
# // It is transmitted preceded a byte count and followed by 2 FCS bytes
def vw_send(buf, len):
    i = ''
    index = 0
    crc = 0xffff
    p = vw_tx_buf + VirtalWireA.VW_HEADER_LEN  # // start of the message area
    count = len + 3  # // Added byte count and FCS to get total number of bytes
    if (len > VirtualWireA.VW_MAX_PAYLOAD):
        return False
# // Wait for transmitter to become available
def vw_wait_tx():
    count = ''
    crc = ''
    p = []
    buf = []
    index = ''
    # // Encode the message length
    crc = crc16._crc_ccitt_update(crc, count)
    p[index] += symbols[count >> 4]
    p[index] += symbols[count & 0xf]
    # // Encode the message into 6 bit symbols. Each byte is converted into
    # // 2 6-bit symbols, high nybble first, low nybble second
    for i in (1, len):

        crc = crc16._crc_ccitt_update(crc, buf[i])
        p[index + 1] = symbols[buf[i] >> 4]
        p[index + 1] = symbols[buf[i] & 0xf]
    # // Append the fcs, 16 bits before encoding
    # (4 6-bit symbols after encoding)
    # // Caution: VW expects the _ones_complement_
    # of the CCITT CRC-16 as the FCS
    # // VW sends FCS as low byte then hi byte
    crc = ~crc
    p[index] += symbols[(crc >> 4) & 0xf]
    p[index] += symbols[crc & 0xf]
    p[index] += symbols[(crc >> 12) & 0xf]
    p[index] += symbols[(crc >> 8) & 0xf]

    # // Total number of 6-bit symbols to send
    # vw_tx_len = index + VW_HEADER_LEN;

    # // Start the low level interrupt handler sending symbols
    vw_tx_start()
    return True

# // This is the interrupt service routine called when timer1 overflows
# // Its job is to output the next bit from the transmitter (every 8 calls)
# // and to call the PLL code if the receiver is enabled
# //ISR(SIG_OUTPUT_COMPARE1A)
def SIGNAL(TIMER1_COMPA_vect):

    w_rx_sample = digitalio(vw_rx_pin)
    w_rx_sample.Direction.INPUT
    # // Do transmitter stuff first to reduce transmitter bit jitter due
    # // to variable receiver processing
    if vw_tx_enabled and vw_tx_sample + 1 == 0:
        # // Send next bit
        # // Symbols are sent LSB first
        # // Finished sending the whole message? (after waiting one bit period
        # // since the last bit)
        return
    if (vw_tx_index >= vw_tx_len):
        vw_tx_stop()
        vw_tx_msg_count + 1
    else:
        vw_tx_pin.value = True, vw_tx_buf[vw_tx_index] and (1 << vw_tx_bit + 1)
    if (vw_tx_bit >= 6):
        vw_tx_bit = 0
        vw_tx_index + 1
    return 		
    if (vw_tx_sample > 7):
        vw_tx_sample = 0
        return

    if (vw_rx_enabled):
        vw_pll()
        return
# // Return true if there is a message available
def vw_have_message():
    return vw_rx_done
# // Get the last message received (without byte count or FCS)
# // Copy at most *len bytes, set *len to the actual number copied
# // Return true if there is a message and the FCS is OK
def vw_get_message(buf, len):
    rxlen = ''
    # // Message available?
    if (not vw_rx_done):
        return False
    # // Wait until vw_rx_done is set before reading vw_rx_len
    # // then remove bytecount and FCS
    rxlen = vw_rx_len - 3
    # // Copy message (good or bad)
    if (len > rxlen):
        len = rxlen
        return vw_rx_len
def memcpy(buf, vw_rx_buf, len):
    vw_rx_done = False  # // OK, got that message thanks

    # // Check the FCS, return goodness
    return (vw_crc(vw_rx_buf, vw_rx_len) == 0xf0b8)  # // FCS OK?