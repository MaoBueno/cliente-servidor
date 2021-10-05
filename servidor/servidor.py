# Arquitectura cliente servidor
# Mauricio Bueno Osorio
# Entrega I

import json
import zmq
import os

import hashlib

# BUF_SIZE is totally arbitrary, change for your app!
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
SIZE = 1048576


context = zmq.Context()

s = context.socket(zmq.REP)
s.bind('tcp://*:8001')

argumentos = {}
usuarios = {}

def upload():
    with open(argumentos.get('archivo'), 'ab') as f:
        byte = s.recv_multipart()
        f.write(byte[0])
        s.send_string('')

def download():
    user = argumentos.get('user')
    name = argumentos.get('archivo')
    archivo = open(name, 'rb')
    s.recv_string()
    if usuarios.get(user) == None:
        usuarios[user] = 0
    posicion = usuarios[user]
    archivo.seek(posicion)
    byte = archivo.read(SIZE)
    usuarios[user] = archivo.tell()
    s.send_multipart([byte])
    archivo.close()

def list():
    s.recv_string()
    s.send_string("\n".join(os.listdir('.')))

def sharelink():
    s.recv_string()
    md5 = hashlib.md5()
    with open (argumentos.get('archivo'), 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
        link = md5.hexdigest()
        s.send_string(link)

def downloadlink():
    s.recv_string()
    link= argumentos.get('archivo')
    archivos = os.listdir('.')
    for archivo in archivos:
        md5 = hashlib.md5()
        with open (archivo, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)
        
        if link == md5.hexdigest():
            s.send_string(archivo)
            break

if __name__ == "__main__":
    while True: 
        datos = s.recv_json()
        argumentos = json.loads(datos)
        s.send_string('')

        if argumentos.get('operacion') == "upload":
            upload()
                
        elif argumentos.get('operacion') == 'download':
            download()
                
        elif argumentos.get('operacion') =='list':
            list()
            
        elif argumentos.get('operacion') == 'sharelink':
            sharelink()
                
        elif argumentos.get('operacion') == 'downloadlink':
            downloadlink()