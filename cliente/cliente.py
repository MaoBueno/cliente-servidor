import zmq      # Provee la comunocación a través de sockets
import sys


context = zmq.Context()

# Crea un socket y lo conecta a tarvés del protocolo tcp con el equipo local en el puerto 8001
s= context.socket(zmq.REQ)
s.connect('tcp://localhost:8001')

user = sys.argv[1]
operacion = sys.argv[2]

SIZE = 1048576

''' s.send_string(user)
s.recv_string()
s.send_string(operacion)
s.recv_string() '''


if operacion == "upload":
    archivo = sys.argv[3]
    with open (archivo, 'rb') as f:
        Mbyte = f.read(SIZE)
        while True:
            if not Mbyte:
                break
            s.send_string(user)
            s.recv_string()
            s.send_string(operacion)
            s.recv_string()
            s.send_string(archivo)
            s.recv_string()
            s.send_multipart([Mbyte])
            s.recv_string()
            Mbyte = f.read(SIZE)
            
elif operacion == 'download':
    archivo = sys.argv[3]
    s.send_string(archivo)
    s.recv_string()
    with open(archivo, 'wb') as f:
        s.send_string('')
        byte = s.recv_multipart()
        f.write(byte[0])
elif operacion == 'list':
    s.send_string('')
    aux = s.recv_string()
    print (aux)
elif operacion == 'sharelink':
    archivo = sys.argv[3]
    s.send_string(archivo)
    link = s.recv_string()
    print (link)
elif operacion == 'downloadlink':
    link= sys.argv[3]
    s.send_string(link)
    nombre = s.recv_string()
    s.send_string('')
    with open(nombre, 'wb') as f:
        byte = s.recv_multipart()
        f.write(byte[0])