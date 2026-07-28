import socket
from Utilities.Config import *
class MountConnection:

    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port

        self.socket = None
        self.connected = False


    def connect(self):
        if self.connected and self.socket is not None:
            return
        
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(2)
            self.socket.connect((self.host, self.port))
        
            self.socket.sendall(b':U2#')

            self.connected = True
            print('Connected')
        except socket.error as e:
            print(f'Socket error: {e}')
            if self.socket:
                self.socket.close()
                self.socket = None
            self.connected = False
            print('Not connected')
            raise

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None

        self.connected = False
        print('Disconnected')

    def send(self,message):
        if not self.connected or self.socket is None:
            raise RuntimeError('Mount not connected')
        self.socket.sendall(message.encode())

    def receive(self):
        return self.socket.recv(1024).decode()

    def send_receive(self,message):
        if not self.connected:
            raise RuntimeError('Mount not connected')
        try:
            self.send(message)
            return self.receive()
        
        except socket.error:
            self.disconnect()
            raise

        
    

    