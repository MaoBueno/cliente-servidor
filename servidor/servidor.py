import zmq
import os

context = zmq.Context()

s = context.socket(zmq.REP)
s.bind('tcp://*:8001')

user = s.recv_string()
s.send_string('')
operacion = s.recv_string()
s.send_string('')

if operacion == "upload":
    archivo= s.recv_string()
    s.send_string('')
    with open(archivo, 'wb') as f:
        byte = s.recv_multipart()
        f.write(byte[0])
elif operacion == 'download':
    archivo= s.recv_string()
    s.send_string('')
    s.recv_string()
    with open (archivo, 'rb') as f:
        byte = f.read()
        s.send_multipart([byte])
elif operacion =='list':
    s.recv_string()
    s.send_string("\n".join(os.listdir('.')))
    