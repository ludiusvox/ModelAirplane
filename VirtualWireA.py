
# // VirtualWire.h
# //
# // Virtual Wire implementation for Arduino and other boards
# // See the README file in this directory for documentation
# //
# // Author: Mike McCauley (mikem@airspayce.com)
# DO NOT CONTACT THE AUTHOR DIRECTLY: USE THE LISTS
# // Copyright (C) 2008 Mike McCauley
# // $Id: VirtualWire.h,v 1.14 2014/03/26 01:09:36 mikem Exp mikem $
# Refactored 2019 by Aaron Linder (ludiusvox)
VW_MAX_MESSAGE_LEN = 80
RX_SAMPLES_PER_BIT = 8
WX_SAMPLES_PER_BIT = 8
VW_WX_SAMPLES_PER_BIT = 10
VW_RX_SAMPLES_PER_BIT = 10
VW_MAX_PAYLOAD = VW_MAX_MESSAGE_LEN - 3
VW_RX_RAMP_LEN = 160
VW_RAMP_INC = (VW_RX_RAMP_LEN/VW_RX_SAMPLES_PER_BIT) * 1
VW_RAMP_TRANSITION = VW_RX_RAMP_LEN/2
VW_RAMP_INC_REDUCE = 1
VW_RAMP_ADJUST = 1
VW_RAMP_INC_REDUCE = (VW_RAMP_INC-VW_RAMP_ADJUST)
VW_RAMP_INC_ADVANCE = (VW_RAMP_INC+VW_RAMP_ADJUST)
VW_HEADER_LEN = 8
# // Set the digital IO pin which will be used to enable
# the transmitter (press to talk, PTT)'
# # This pin will only be accessed if
# # the transmitter is enabled
# # \param[in] pin The Arduino pin number to enable
# the transmitter. Defaults to 10.
def vw_set_ptt_pin(pin):
    return pin
# # Set the digital IO pin to be for transmit data.
# # This pin will only be accessed if
# # the transmitter is enabled
# # \param[in] pin The Arduino pin number
# for transmitting data. Defaults to 12.
def vw_set_tx_pin(pin):
    return pin
# # Set the digital IO pin to be for receive data.
# # This pin will only be accessed if
# # the receiver is enabled
# # \param[in] pin The Arduino pin number for receiving data. Defaults to 11.
def vw_set_rx_pin(pin):
    return pin
    # # By default the RX pin is expected to be
    # low when idle, and to pulse high
    # # for each data pulse.
    # # This flag forces it to be inverted.
    # This may be necessary if your transport medium
    # # inverts the logic of your signal, such as happens
    # with some types of A/V tramsmitter.
    # # \param[in] inverted True to invert sense of receiver input
def vw_set_rx_inverted(inverted):
    return inverted
    # By default the PTT pin goes high when the transmitter is enabled.
    # This flag forces it low when the transmitter is enabled.
    # param[in] inverted True to invert PTT
def vw_set_ptt_inverted(inverted):
    return inverted

    # Initialise the VirtualWire software,
    # to operate at speed bits per second
    # Call this one in your
    # () after any vw_set_* calls
    # Must call vw_rx_start() before you will get any messages
    # \param[in] speed Desired speed in bits per second
def vw_setup(speed):
    return speed

    # Start the Phase Locked Loop listening to the receiver
    # Must do this before you can receive any messages
    # When a message is available (good checksum or not), vw_have_message();
    # will return true.
def vw_rx_start():
    return

    # Stop the Phase Locked Loop listening to the receiver
    # No messages will be received until vw_rx_start() is called again
    # Saves interrupt processing cycles
def vw_rx_stop():
    return

    # Returns the state of the
    # transmitter
    # \return true if the transmitter is active else false
def vw_tx_active():
    return
    # Block until the transmitter is idle
    # then returns
def vw_wait_tx():
    return
    # Block until a message is available
    # then returns
def vw_wait_rx():
    return
    # Block until a message is available or for a max time
    # \param[in] milliseconds Maximum time to wait in milliseconds.
    # \return true if a message is available, false if the wait timed out.
def vw_wait_rx_max(milliseconds):
    return milliseconds
    # Send a message with the given length. Returns almost immediately,
    # and message will be sent at the right timing by interrupts
    # \param[in] buf Pointer to the data to transmit
    # \param[in] len Number of octetes to transmit
    # \return true if the message was accepted for transmission,
    # false if the message is too long (>VW_MAX_MESSAGE_LEN - 3)
def vw_send(buf, len):
    return len
    # Returns true if an unread message is available
    # \return true if a message is available to read
def vw_have_message():
    return
    # If a message is available (good checksum or not), copies
    # up to *len octets to buf.
    # \param[in] buf Pointer to location to save the read data
    # (must be at least *len bytes.
    # \param[in,out] len Available space in buf. Will be set to the
    # actual number of octets read
    # \return true if there was a message and the checksum was good
def vw_get_message(buf, len):
    return len

    # Returns the count of good messages received
    # Caution,: this is an 8 bit count and can easily overflow
    # \return Count of good messages received
def vw_get_rx_good():
    return

    # Returns the count of bad messages received, ie
    # messages with bogus lengths, indicating corruption
    # or lost octets.
    # Caution,: this is an 8 bit count and can easily overflow
    # \return Count of bad messages received
def vw_get_rx_bad():
    return