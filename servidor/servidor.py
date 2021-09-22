import zmq

context = zmq.Context()

s = context.socket(zmq.REP)
s.bind('tcp://*:8001')

user = s.recv_string()
s.send_string('')
operacion = s.recv_string()
s.send_string('')
archivo= s.recv_string()
s.send_string('')

if operacion == "upload":
    with open(archivo, 'wb') as f:
        byte = s.recv_multipart()
        f.write(byte[0])

    s.send_string('Recibido')