import serial
from xbee import XBee
BAUDRATE             = 57600
PORT                 = '/dev/ttyAMA0'
serial_port = serial.Serial(PORT, BAUDRATE)
xbee = XBee(serial_port)
xbee.tx(dest_addr="\x00\x01",data="hello")
xbee.halt()
serial_port.close()
