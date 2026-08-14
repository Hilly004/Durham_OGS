import socket
import threading

from Utilities.Config import *
class MountConnection:

    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port

        self.socket = None
        self.connected = False

        self.command_lock = threading.Lock()


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

    def receive(self, terminator='#'):
        if not self.connected or self.socket is None:
            raise RuntimeError('Mount not connected')

        response = ''

        while True:
            chunk = self.socket.recv(1024).decode()

            if not chunk:
                raise ConnectionError('Mount connection closed')

            response += chunk

            if terminator is None:
                return response

            if terminator in response:
                return response

    def send_receive(self,message, terminator='#'):
        if not self.connected:
            raise RuntimeError('Mount not connected')
        try:
            with self.command_lock:
                self.send(message)
                return self.receive(terminator)
        
        except socket.error:
            self.disconnect()
            raise

        
    

    