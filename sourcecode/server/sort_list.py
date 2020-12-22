import struct
my_data = []
my_data.append(struct.pack(">B",55)+struct.pack(">I",2)+" world")
my_data.append(struct.pack(">B",55)+struct.pack(">I",3)+" ;)")
my_data.append(struct.pack(">B",55)+struct.pack(">I",1)+"hello")

def get_key(element):
    return struct.unpack(">I", element[1:5])[0]

my_data.sort(key=get_key)

for e in my_data:
    print e[5:]

