from serial import Serial
from xbee import XBee
from parameters import *
serial      = Serial(PORT,BAUDRATE)
xbee      = XBee(serial)
