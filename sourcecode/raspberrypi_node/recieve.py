import serial
import uuid
s = serial.Serial("/dev/ttyAMA0",115200,timeout=3)

while True:
    data = s.read(3)
    if(data==b"\xFF\xD8\xFF"):
        file_name = str(uuid.uuid4())+".jpeg"
        my_file = open(file_name,"wb")
        #my_file.write(data)
        #data=s.read(2)
        while(data[-2:] !=b"\xFF\xD9"):
            print(data)
            my_file.write(data)
            data = s.read(s.inWaiting())
        my_file.write(data)
        my_file.close()
        s.close()
        quit()


