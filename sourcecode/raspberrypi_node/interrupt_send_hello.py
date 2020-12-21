import time
import RPi.GPIO as IO
from camera import capture

from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.devices import XBee64BitAddress
import base64
REMOTE_ADDRESS = "0013A20040E4DD23"
device = XBeeDevice("/dev/ttyAMA0",115200)
import time
def send():
    start = time.time()
    device.open()
    # Instantiate a remote XBee device object.
    remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string(REMOTE_ADDRESS))
    # Send data using the remote object.
    device.send_data(remote_device, "Hello Wolrd!")
    device.close()
    print("--- %s seconds ---" % (time.time() - start))


def interruption_handler(pin):
    print("sending")
    send()

def main():
    IR_PIN = 26
    IO.setwarnings(False)
    IO.setmode(IO.BCM)
    IO.setup(IR_PIN,IO.IN) #GPIO 26 -> IR sensor as input
    IO.add_event_detect(IR_PIN,IO.RISING)
    IO.add_event_callback(IR_PIN,interruption_handler)
    while True:
        time.sleep(1)

if __name__=="__main__":
    main()
