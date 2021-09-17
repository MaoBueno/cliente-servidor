import zmq      # Provee la comunocación a través de sockets
import sys

context = zmq.Context()

# Crea un socket y lo conecta a tarvés del protocolo tcp con el equipo local en el puerto 8001
s= context.socket(zmq.REQ)
s.connect('tcp://localhost:8001')


with open ('imagen.jpg', 'rb') as f:
    byte = f.read()
    s.send_multipart([byte])

m= s.recv_string()

print(m)

