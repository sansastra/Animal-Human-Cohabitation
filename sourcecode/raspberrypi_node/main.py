import tensorflow as tf
from animal_or_none.scripts.label_image import classify
import os, sys
from PIL import Image
from picamera import PiCamera
import uuid
import time

def capture(file_name):
    #file_name = str(uuid.uuid4())+".jpg"
    my_file = open(file_name,'wb')
    camera = PiCamera()
    camera.resolution = (3280,2464)
    camera.capture(my_file,resize=(299,299))
    my_file.close()
    camera.close()

if __name__ == "__main__":
    start = time.time()
    file_name = str(uuid.uuid4())+".jpg"

    capture(file_name)

    classify(file_name
        ,"animal_or_none/tf_files/retrained_graph.pb"
        ,"animal_or_none/tf_files/retrained_labels.txt")

    print("Total time : ")
    print(time.time()-start)
