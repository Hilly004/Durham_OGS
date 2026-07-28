import socket
from Utilities.Config import *
class MountConnection:

    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port

        self.socket = None
        self.connected = False

    def connect(self):

        try:
            self.socket = socket.socket(socket.AF_INET,
                                         socket.SOCK_STREAM)
            
            self.socket.settimeout(2)

            self.socket.connect(
                (self.host,self.port)
            )

            self.connected = True
            self.socket.sendall(b':U2#')
            print('Socket connected:',self.connected)

        except socket.error as e:
            print(e)
            self.connected = False

            raise

    def disconnect(self):

        if self.socket:
            self.socket.close()
            self.socket = None
        self.connected = False

    def is_connected(self):
        print('MountConnection.connected =', self.connected)
        return self.connected
    
    def send(self,message):

        if not self.connected:
            raise RuntimeError('Mount not connected')
        
        try:
            self.socket.sendall(
                message.encode()
            )

        except socket.error:
            self.connected = False
            raise

    def send_receive(self,message):

        if not self.connected:
            raise RuntimeError('Mount not connected')
        
        try:
            self.socket.sendall(
                message.encode()
            )

            data = self.socket.recv(1024)

            return data.decode()
    
        except socket.error:
            self.connected = False
            raise

        
    

    