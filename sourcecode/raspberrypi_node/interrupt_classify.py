import time
import RPi.GPIO as IO

def interruption_handler(pin):
    print("recieved interruption")

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
