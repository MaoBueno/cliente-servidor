# Arquitectura cliente servidor
# Mauricio Bueno Osorio
# Entrega I

import zmq      # Provee la comunocación a través de sockets
import sys
import json


context = zmq.Context()

# Crea un socket y lo conecta a tarvés del protocolo tcp con el equipo local en el puerto 8001
s= context.socket(zmq.REQ)
s.connect('tcp://localhost:8001')


argumentos = {
    'user':sys.argv[1], 
    'operacion':sys.argv[2],
    'archivo': sys.argv[3] if sys.argv[2] != 'list' else 0
}

SIZE = 10485760


if argumentos.get('operacion') == "upload":
    with open (argumentos.get('archivo'), 'rb') as f:
        Mbyte = f.read(SIZE)
        while True:
            if not Mbyte:
                break
            datos = json.dumps(argumentos)
            s.send_json(datos)
            s.recv_string()
            s.send_multipart([Mbyte])
            s.recv_string()
            Mbyte = f.read(SIZE)
            
elif argumentos.get('operacion') == 'download':
    with open (argumentos.get('archivo'), 'ab') as f:
        while True:
            datos = json.dumps(argumentos)
            s.send_json(datos)
            s.recv_string()
            s.send_string('')
            byte = s.recv_multipart()
            
            if len(byte[0]) == 0:
                break
            
            f.write(byte[0])
        
elif argumentos.get('operacion') == 'list':
    datos = json.dumps(argumentos)
    s.send_json(datos)
    s.recv_string()
    s.send_string('')
    listar_archivos = s.recv_string()
    print (listar_archivos)
    
elif argumentos.get('operacion') == 'sharelink':
    datos = json.dumps(argumentos)
    s.send_json(datos)
    s.recv_string()
    s.send_string('')
    link = s.recv_string()
    print (link)
    
elif argumentos.get('operacion') == 'downloadlink':
    datos = json.dumps(argumentos)
    s.send_json(datos)
    s.recv_string()
    s.send_string('')
    nombre = s.recv_string()
    argumentos['archivo'] = nombre
    argumentos['operacion'] = 'download'
    
    with open (argumentos.get('archivo'), 'ab') as f:
        while True:
            datos = json.dumps(argumentos)
            s.send_json(datos)
            s.recv_string()
            s.send_string('')
            byte = s.recv_multipart()
            
            if len(byte[0]) == 0:
                break
            
            f.write(byte[0])