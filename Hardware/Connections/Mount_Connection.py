import socket

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

        except socket.error:
            if self.socket:
                self.socket.close()
                self.socket = None
            self.connected = False
            raise

    def disconnect(self):

        if self.socket:
            self.socket.close()
            self.socket = None
        self.connected = False


    def check_connection(self):
        return self.connected


    def send(self,message):

        if not self.connected:
            raise RuntimeError('Mount not connected')
        
        command = ':U2#'

        self.socket.sendall(
            command.encode()
        )

        self.socket.sendall(
            message.encode()
        )

    def send_receive(self,message):

        if not self.connected:
            raise RuntimeError('Mount not connected')
        
        command = ':U2#'

        self.socket.sendall(
            command.encode()
        )

        self.socket.sendall(
            message.encode()
        )

        data = self.socket.recv(1024)

        return data.decode()