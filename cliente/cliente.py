import zmq      # Provee la comunocación a través de sockets
import sys

context = zmq.Context()

# Crea un socket y lo conecta a tarvés del protocolo tcp con el equipo local en el puerto 8001
s= context.socket(zmq.REQ)
s.connect('tcp://localhost:8001')

user = sys.argv[1]
operacion = sys.argv[2]
archivo = sys.argv[3]


if operacion == "upload":
    s.send_string(user)
    s.recv_string()
    s.send_string(operacion)
    s.recv_string()
    s.send_string(archivo)
    s.recv_string()
    with open (archivo, 'rb') as f:
        byte = f.read()
        s.send_multipart([byte])
    m= s.recv_string()
elif operacion == 'download':
    s.send_string(user)
    s.recv_string()
    s.send_string(operacion)
    s.recv_string()
    s.send_string(archivo)
    s.recv_string()
    with open(archivo, 'wb') as f:
        s.send_string('')
        byte = s.recv_multipart()
        f.write(byte[0])
    s.send_string('Recibido')