from picamera import PiCamera
import uuid

def capture():
    file_name = str(uuid.uuid4())+".jpeg"
#my_file = open(file_name,'wb')
    camera = PiCamera()
    #camera.resolution = (3280,2464)
    camera.resolution = (299,299)
    camera.capture(open(file_name,'wb'))
    camera.close()

if __name__ == '__main__':
    import time
    start_time = time.time()
    capture()
    print("--- %s seconds ---" % (time.time() - start_time))
