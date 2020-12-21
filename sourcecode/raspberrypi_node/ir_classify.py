import RPi.GPIO as IO
import time
import subprocess
IR_PIN = 26
IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(IR_PIN,IO.IN) #GPIO 26 -> IR sensor as input
cmd = ["python3" "-m" "animal_or_none.scripts.label_image"     "--graph=animal_or_none/tf_files/retrained_graph.pb"      "--image=animal_or_none/test1.jpg"]
while 1:
    if(IO.input(IR_PIN) == True):
       print("mv detected")
       subprocess.Popen(cmd)
       time.sleep (1)
