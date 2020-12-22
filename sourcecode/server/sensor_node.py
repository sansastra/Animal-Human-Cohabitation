import serial
from xbee import XBee
import struct
import RPi.GPIO as IO
from picamera import PiCamera
from animal_or_none.scripts.label_image import *
from camera import capture
from ZigbeeFileTransfer import sender
from uuid import uuid4
import time
SERVER_ADDRESS = "\x00\x01"
BAUDRATE             = 57600
PORT                 = '/dev/ttyAMA0'

serial_port = serial.Serial(PORT, BAUDRATE)
xbee = XBee(serial_port)


def capture(file_name):
    camera = PiCamera()
    camera.resolution = (299,299)
    camera.capture(open(file_name,'wb'))
    camera.close()

def resize(infile):
    # image_path = 'test_images/leopard2.jpg'
    size = (299, 299)
    # infile = image_path
    outfile = os.path.splitext(infile)[0] + '_resized.jpg'
    try:
        im = Image.open(infile)
        im.thumbnail(size, Image.ANTIALIAS)
        old_im_size = im.size
        #By default, black colour would be used as the background for padding!
        new_im = Image.new("RGB", size)
        new_im.paste(im,(int((size[0]-old_im_size[0])/2),int((size[1]-old_im_size[1])/2)))
        new_im.save(outfile, "JPEG")
    except IOError:
        print ("Cannot resize '%s'" % infile)


def classify(file_name):
    import tensorflow as tf
    model_file = "animal_or_none/tf_files/retrained_graph.pb"
    label_file = "animal_or_none/tf_files/retrained_labels.txt"
    input_height = 224
    input_width = 224
    input_mean = 128
    input_std = 128
    input_layer = "input"
    output_layer = "final_result"

    graph = load_graph(model_file)
    t = read_tensor_from_image_file(file_name,
                                  input_height=input_height,
                                  input_width=input_width,
                                  input_mean=input_mean,
                                  input_std=input_std)

    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name);
    output_operation = graph.get_operation_by_name(output_name);

    with tf.Session(graph=graph) as sess:
    #    start = time.time()
        results = sess.run(output_operation.outputs[0],
                      {input_operation.outputs[0]: t})
        end=time.time()
    results = np.squeeze(results)
    top_k = results.argsort()[-5:][::-1]
    labels = load_labels(label_file)
    #print('\nEvaluation time (1-image): {:.3f}s\n'.format(end-start))
    template = "{},score={:0.5f};"
    ml_result =""
    for i in top_k:
        print(template.format(labels[i], results[i]))
        ml_result+=template.format(labels[i], results[i])
    return ml_result

def excecute_command(command):
    if   command == "1":#received notification from sensor node
        print('[+] sending image')
        sender.send_file(file_name)
    elif command == "0":#received file header
        print('[+] running classification')
        payload= struct.pack(">B",3)
        classification_result = classify(file_name)
        print("image class:"+classification_result)
        payload+= classification_result
        xbee.tx(dest_addr=SERVER_ADDRESS,data=payload)

def interruption_handler(pin):
    print("mvt detected")
    #capture picture
    file_name = str(uuid4())+".jpeg"
    capture(file_name)
    #send notification
    #wait for command
    #excecute command
    payload= struct.pack(">B",1)
    payload+="mouvement detected".encode()
    xbee.tx(dest_addr=SERVER_ADDRESS,data=payload)
    del payload
    #wait for command from server
    ## TODO: in case server not found or does not respond
    #retry a couple of times
    response = xbee.wait_read_frame()
    print(response)
    command = response["rf_data"]
    #excecute command
    if   command == b'1':#received notification from sensor node
        print('[+] sending image')
        sender.send_file(file_name)
    elif command == b'0':#received file header
        print('[+] running classification')
        payload= struct.pack(">B",3)
        classification_result = classify(file_name)
        print("image class:"+classification_result)
        payload += classification_result.encode()
        xbee.tx(dest_addr=SERVER_ADDRESS,data=payload)


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
        print ("Bye")

    #THE END!
    xbee.halt()
    serial_port.close()
