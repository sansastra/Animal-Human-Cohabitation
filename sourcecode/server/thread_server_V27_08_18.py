from threading import Thread , enumerate
from serial.serialutil import SerialException
from queue import Queue , Empty
from time import sleep
import serial
from xbee import XBee
from uuid import uuid4
import struct
from parameters import *
from animal_or_none.scripts.label_image import *
import struct
# TODO: remove randint after setting up decison algorithm
from random import randint

def check_for_danger(ml_result):
    '''
    @param : ml_result 'none,score=0.99944;animal,score=0.00056;'
    '''
    if ml_result.startswith( 'animal' ):
        return 1
    else:
        return 0

def classify(file_name):
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
        #start = time.time()
        results = sess.run(output_operation.outputs[0],
                      {input_operation.outputs[0]: t})
        #end=time.time()
    results = np.squeeze(results)

    top_k = results.argsort()[-5:][::-1]
    labels = load_labels(label_file)

    #print('\nEvaluation time (1-image): {:.3f}s\n'.format(end-start))
    template = "{} (score={:0.5f})"
    ml_result =""
    for i in top_k:
        print(template.format(labels[i], results[i]))
        ml_result+=template.format(labels[i], results[i])
    return ml_result

class Stream_handler:
    def __init__(self):
        self.nbr_packets = 0
        #self.file_name = str(uuid4())
        self.file_name = str(uuid4())+time.strftime("%Y_%m_%d-%H_%M_%S")
        self.file_data = []
    def rcv_file_data(self,rf_data):
        if rf_data[0]==0:
            #print ("[+] receiving file data ..")
            self.nbr_packets  = struct.unpack(">I",rf_data[1:5])[0]
            #print ("[+] Stream_handler nbr_packets",self.nbr_packets)
        else:
            # TODO: replace else with elif rf_data[0]==55:
            self.file_data.append(rf_data[5:])
            index =struct.unpack(">I", rf_data[1:5])[0]
            #print ("[+] Stream_handler  packet index ",index)
            if index == self.nbr_packets:
                print ("writing to file")
                f = open(self.file_name, "wb")
                for e in self.file_data:
                    f.write(e)
                del self.file_data[:]
                f.close()
                return True #if file recieved return True else return False
        return False

# Multithreaded Python server : zigbee Server Thread Pool
#each client will be handled by one thread
class ClientThread(Thread):
    """
    thread that will handle zigbee client.
    an instance of this class will be created for every client.
    once the communication (task) is done, thread will exit.
    """
    def __init__(self,source_addr):
        Thread.__init__(self)
        self.source_addr = source_addr
        self.rx_queue = Queue()
        self.__stream = Stream_handler()
        print ("[+] New thread started for client :",self.source_addr)

    def run__1(self):
        #execute main thread sh!t here
        #based on header content
        #if  FILE_TRANSFER_HEADER
        file_transfer_done = 0
        __stream = Stream_handler()
        while True:
            try:
                rf_data = self.rx_queue.get()
                file_transfer_done = __stream.rcv_file_data(rf_data)
                # @TODO : DO: If file recieved exit thread
                if file_transfer_done:
                    # run ML algorithm on the received image __stream.file_name
                    classify(__stream.file_name)
                    # @TODO : send order to sensor based on ML output.
                    return 0
            except Empty as e:
                pass


    def run(self):
        #execute main thread sh!t here
        #based on header content
        #if  FILE_TRANSFER_HEADER
        file_transfer_done = 0
        while True :
            try:
                rf_data = self.rx_queue.get()
                #TODO: catch exception : empty rf data
                flag = rf_data[0]
                data = rf_data[1:]
                if   flag == 1:#received notification from sensor node
                    print('[+] received notification from sensor node')
                    cmd=self.choose_command()
                    self.send_command(cmd)
                    # choose command here
                elif flag == 3:#received file data
                    print('[+] ML classification result')
                    # result format:
                    # none,score=0.99995;animal,score=0.00005;
                    print(data.decode("utf-8") )
                    #print(type(data.decode("utf-8") ))
                    if check_for_danger(data.decode("utf-8") )==1:
                        XBee(serial.Serial(PORT, BAUDRATE)).tx(dest_addr="\x00\x03",data="Danger")
                    # if ml_result==1:
                    #    XBee(serial.Serial(PORT, BAUDRATE)).tx(dest_addr="\x00\x03",data="Danger")
                    # TODO:check for danger here
                    # then exit
                    return 0
                elif flag == 0 or flag == 55:#received file data
                    file_transfer_done = self.__stream.rcv_file_data(rf_data)
                    if file_transfer_done:
                        # run ML algorithm on the received
                        # image __stream.file_name
                        ml_result = classify(self.__stream.file_name)
                        if check_for_danger(ml_result)==1:
                            XBee(serial.Serial(PORT, BAUDRATE)).tx(dest_addr="\x00\x03",data="Danger")
                        return 0
                    #print('[+] received file data')
            except Empty as e:
                pass

            # wait for data frame

    def choose_command(self):
        '''
        This method will send a command to the sensor to excecute
        the appropriate scenario according to a decision algorithm
        '''
        # 0 : onboadr classification
        # 1 : on server classification

        res = randint(0, 1)
        print ("decision = ",res)
        return str(res)

    def send_command(self,command):
        XBee(serial.Serial(PORT, BAUDRATE)).tx(dest_addr=self.source_addr,data=command)



# Multithreaded Python server :
threads = []

def call_back(xbee_message):
    """
    Function that receives incoming data and sends it
    to the appropriate handler (thread).
    If no handler found for that client then create a new one.

    @param: xbee_message : message  recieved from xbee device
    message format {'id': 'rx', 'rf_data': b'\x02world', 'options': b'\x00',
    'source_addr': b'\x00\x02', 'rssi': b'7'}

    """
    #data = xbee_message["rf_data"]
    source_addr = xbee_message["source_addr"]
    rf_data = xbee_message["rf_data"]
    create_new = True
    threads = enumerate()

    # check if a thread is already assigned for that client
    for t in threads:
        if t.name == source_addr.hex():
            # address already there
            # forward data to that thread
            #print ("client already there")
            create_new = False
            t.rx_queue.put(rf_data)
            break

   # if it's a new client -> creae new thread for it
    if create_new :
        newthread = ClientThread(source_addr)
        newthread.daemon = True #when main thread dies , all threads die
        #newthread.rx_queue.put(rf_data)
        newthread.start()
        threads.append(newthread)
        newthread.name = source_addr.hex()
        newthread.rx_queue.put(rf_data)

def main():
    try:
        serial_port = serial.Serial(PORT, BAUDRATE)
        xbee = XBee(serial_port, callback=call_back)
    except SerialException as e:
        print("[-] Xbee device not found !")
        exit(1)
    print("[+] Xbee server running... ")
    while True:
        try:
            sleep(1)
        except KeyboardInterrupt:
            break
    for t in threads:
        t.join()
    xbee.halt()
    serial_port.close()

if __name__ == '__main__':
    main()
