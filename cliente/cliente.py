# Arquitectura cliente servidor
# Mauricio Bueno Osorio
# Entrega II

import zmq      # Provee la comunocación a través de sockets
import sys
import json
import hashlib


SIZE = 1048576


def strToSha(string):
    hash_object = hashlib.sha1(string.encode())
    name = hash_object.hexdigest()
    nameAsNum = int(name, 16)
    return nameAsNum

def megaToSha(megabyte):
    hash_object = hashlib.sha1( megabyte )
    name = hash_object.hexdigest()
    nameAsNum = int( name, 16 )
    return nameAsNum

class Range:
    def __init__(self,lb,ub):
        self.lb = lb
        self.ub = ub
    
    def isFirst(self):
        return self.lb > self.ub
    
    def member(self, id):
        if self.isFirst():
            return (id >= self.lb and id < 1<<160) or (id >= 0 and id < self.ub )
        else:
            return id >= self.lb and id < self.ub
    
    def toStr(self):
        if self.isFirst():
            return '[' + str(self.lb) + ' , 2^160) U [' + '0 , ' +  str(self.ub) + ')'
        else:
            return '[' + str (self.lb) + ' , ' + str(self.ub) + ')'
        

def upload(argumentos, ranges, servidores):
    nombre = argumentos.get('archivo')
    index = nombre.split('.')[0]
    index = index+'.index'
    
    with open (nombre, 'rb') as f:
        with open (index, 'a') as index:
            index.write(nombre+'\n')
            Mbyte = f.read(SIZE)
            
            while True:
                if (not len (Mbyte)):
                    break
                
                hashMb = megaToSha(Mbyte)
                
                for range in ranges:
                    if range.member(hashMb):
                        
                        index.write(str(hashMb)+'\n')
                        datos = json.dumps(argumentos)
                        socket = servidores.get(range.lb)
                        
                        socket.send_string(datos)
                        socket.recv_string()
                        socket.send_multipart([Mbyte])
                        socket.recv_string()
                        
                        Mbyte = f.read(SIZE)
                        break

def download(argumentos, ranges, servidores):
    with open (argumentos.get('archivo'), 'r') as index:
        nombre = index.readline()
        nombre2 = nombre.split('\n')[0]
        
        with open ('download-'+nombre2, 'ab') as f:
                while True:
                    hashMb = index.readline()
                    print(hashMb)
                    
                    if (len(hashMb)== 0):
                        break
                    
                    hashMb = int(hashMb)
                    for range in ranges:
                        if range.member(hashMb):
                            socket = servidores.get(range.lb)
                            argumentos['archivo'] = hashMb
                            
                            datos = json.dumps(argumentos)
                            socket.send_string(datos)
                            
                            byte = socket.recv_multipart()
                            
                            f.write(byte[0])
                            break




if __name__ == "__main__":
    
    argumentos = {
    'user':sys.argv[1], 
    'operacion':sys.argv[2],
    'archivo': sys.argv[3] if sys.argv[2] != 'list' else 0
}
    
    nombreServidores = ['serv1', 'serv2', 'serv3', 'serv4', 'serv5']
    servidores = [] 
    
    for num in range(1,6):
        context = zmq.Context()
        socket = context.socket( zmq.REQ )
        socket.connect( 'tcp://127.0.0.{}:800{}'.format(num, num))
        servidores.append(socket)
    
    shaServidores = []
    socketServidores = {}

    for num in range(5):
        sha_one = strToSha(nombreServidores[num])
        shaServidores.append( sha_one )
        socketServidores[sha_one] = servidores[num]
    
    shaServidores.sort()
    ranges = []
    
    for n in range(len(shaServidores)-1):
        lb = shaServidores[n]
        ub = shaServidores[n+1]
        ranges.append( Range( lb,ub ) )
    ranges.append(Range(shaServidores[4],shaServidores[0]))
    
    
    if argumentos.get('operacion') == "upload":
        upload(argumentos, ranges, socketServidores)
                
    elif argumentos.get('operacion') == 'download':
        download(argumentos, ranges, socketServidores)
    
    else:
        print ("No existe operacion")