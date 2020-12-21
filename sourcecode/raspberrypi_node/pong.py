"""import serial
import time
from xbee import XBee

serial_port = serial.Serial('/dev/ttyUSB0', 9600)

def print_data(data):
    print (data)

xbee = XBee(serial_port, callback=print_data)

while True:
    try:
        time.sleep(0.001)
    except KeyboardInterrupt:
        break

xbee.halt()
serial_port.close()
"""
import serial
from xbee import XBee
import struct
from time import sleep

SERVER_ADDRESS = "\x00\x01"
BAUDRATE             = 57600
PORT                 = '/dev/ttyAMA0'
def pong(msg):
    print(msg)
    payload= struct.pack(">B",2)
    payload+="Hi".encode()
    xbee.tx(dest_addr=SERVER_ADDRESS,data=payload)
    print("ping received")

serial = serial.Serial(PORT, BAUDRATE)
xbee = XBee(serial,callback=pong)

while True:
    try:
        sleep(0.001)
    except KeyboardInterrupt:
        print("Bye!")
        break

    #THE END!
xbee.halt()
serial.close()
