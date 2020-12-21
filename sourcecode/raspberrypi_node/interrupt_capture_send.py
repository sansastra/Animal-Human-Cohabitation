import time
import RPi.GPIO as IO
from picamera import PiCamera
import uuid
from ZigbeeFileTransfer import sender

def interruption_handler(pin):
    file_name = str(uuid.uuid4())+".jpeg"
    camera = PiCamera()
    camera.resolution = (299,299)
    camera.capture(open(file_name,'wb'))
    camera.close()
    sender.send_file(file_name)

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
    try:
        main()
    except KeyboardInterrupt:
        print "Bye"
