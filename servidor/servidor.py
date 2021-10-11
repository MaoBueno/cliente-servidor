# Arquitectura cliente servidor
# Mauricio Bueno Osorio
# Entrega I

import json
import zmq
import os
import hashlib
import sys

# BUF_SIZE is totally arbitrary, change for your app!
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
SIZE = 1048576

def megaToSha(megabyte):
    hash_object = hashlib.sha1( megabyte )
    name = hash_object.hexdigest()
    nameAsNum = int(name, 16)
    return nameAsNum



def upload(socket, directorio):
    
    Mbyte = socket.recv_multipart()
    socket.send_string('ok')
    
    hashMb = megaToSha(Mbyte[0])
    nombre = directorio+str(hashMb)
    
    with open(nombre, 'ab') as f:
        f.write(Mbyte[0])

# def download():
#     user = argumentos.get('user')
#     name = argumentos.get('archivo')
#     archivo = open(name, 'rb')
#     s.recv_string()
#     if usuarios.get(user) == None:
#         usuarios[user] = 0
#     posicion = usuarios[user]
#     archivo.seek(posicion)
#     byte = archivo.read(SIZE)
#     usuarios[user] = archivo.tell()
#     s.send_multipart([byte])
#     archivo.close()




if __name__ == "__main__":
    argumentos = {}
    usuarios = {}
    
    numServer = sys.argv[1]
    puerto = 'tcp://127.0.0.{}:800{}'.format(numServer, numServer)
    
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(puerto)
    
    directorio = './serv{}/'.format(numServer)
    print(directorio)
    
    while True: 
        datos = socket.recv_string()
        argumentos = json.loads(datos)

        if argumentos.get('operacion') == "upload":
            socket.send_string('ok')
            upload(socket, directorio)
                
        # elif argumentos.get('operacion') == 'download':
        #     download()