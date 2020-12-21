import RPi.GPIO as IO
import time
IR_PIN = 26
IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(IR_PIN,IO.IN) #GPIO 26 -> IR sensor as input

from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.devices import XBee64BitAddress
import base64

REMOTE_ADDRESS = "0013A20040E4DD23"
device = XBeeDevice("/dev/ttyAMA0",9600)

import time

def send():
    start = time.time()
    #device.open()
    # Instantiate a remote XBee device object.
    remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string(REMOTE_ADDRESS))
    # Send data using the remote object.
    with open("jpeg.jpg","rb") as f:
        buffer = f.read(100)
        while buffer != b"":
            device.send_data(remote_device, buffer)
            buffer = f.read(100)
        f.close()
    #device.close()
    print("--- %s seconds ---" % (time.time() - start))


device.open()
while 1:
    if(IO.input(IR_PIN) == True):
       send()
       time.sleep (1)

device.close()

