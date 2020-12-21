import RPi.GPIO as IO
import time
IR_PIN = 26
IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(IR_PIN,IO.IN) #GPIO 26 -> IR sensor as input

while 1:
    if(IO.input(IR_PIN) == True):
       print("mv detected")
       time.sleep (1)
