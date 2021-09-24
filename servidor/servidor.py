import zmq
import os

import hashlib

# BUF_SIZE is totally arbitrary, change for your app!
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
SIZE = 1048576


context = zmq.Context()

s = context.socket(zmq.REP)
s.bind('tcp://*:8001')

while True: 

    user = s.recv_string()
    s.send_string('')
    operacion = s.recv_string()
    s.send_string('')

    if operacion == "upload":
        archivo= s.recv_string()
        s.send_string('')
        with open(archivo, 'ab') as f:
            byte = s.recv_multipart()
            f.write(byte[0])
            s.send_string('')
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
    elif operacion == 'sharelink':
        archivo= s.recv_string()
        md5 = hashlib.md5()
        with open (archivo, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)
            link = md5.hexdigest()
            s.send_string(link)
    elif operacion == 'downloadlink':
        link= s.recv_string()
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
                s.recv_string()
                with open (archivo, 'rb') as f:
                    byte = f.read()
                    s.send_multipart([byte])
    