from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.devices import XBee64BitAddress
import time
import RPi.GPIO as IO
from camera import capture

REMOTE_ADDRESS = "0013A20040E4DD23"
device = XBeeDevice("/dev/ttyAMA0",115200)



def interruption_handler(pin):
    print("capturing")
    start = time.time()
    capture()
    device.open()
    # Instantiate a remote XBee device object.
    remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string(REMOTE_ADDRESS))
    with open("jpeg.jpg","rb") as f:
        buffer = f.read(100)
        while buffer != b"":
            device.send_data(remote_device, buffer)
            buffer = f.read(100)
        f.close()
    device.close()
    print("--- %s seconds ---" % (time.time() - start))

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



