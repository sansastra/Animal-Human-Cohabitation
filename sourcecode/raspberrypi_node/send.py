from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.devices import XBee64BitAddress
import base64
REMOTE_ADDRESS = "0013A20040E4DD23"
device = XBeeDevice("/dev/ttyAMA0",115200)
import time
start = time.time()
device.open()
# Instantiate a remote XBee device object.
remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string(REMOTE_ADDRESS))
# Send data using the remote object.
#with open("jpeg_107.jpg","rb") as f:
#    buffer = f.read(100)
#    while buffer != b"":
device.send_data(remote_device, "Hi")
#        buffer = f.read(100)
#    f.close()
device.close()
print("--- %s seconds ---" % (time.time() - start))
exit()
