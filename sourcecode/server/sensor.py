from serial import Serial
from xbee import XBee
from parameters import *
serial      = Serial(PORT,BAUDRATE)
xbee      = XBee(serial)


def notify_and_wait():
    
    #xbee = XBee(serial_port, callback=execute_command)
    xbee.halt()
    serial_port.close()

def execute_command(message)
    print(message)
