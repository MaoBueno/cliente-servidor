import zmq

context = zmq.Context()

s = context.socket(zmq.REP)
s.bind('tcp://*:8001')

with open('imagenCopia.jpg', 'wb') as f:
    byte = s.recv_multipart()
    f.write(byte[0])

s.send_string('Recibido')