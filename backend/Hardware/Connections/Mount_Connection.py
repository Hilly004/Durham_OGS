import socket
import threading

class MountConnection:

    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port

        self.socket = None
        self.connected = False

        self.command_lock = threading.RLock()

    def configure(
        self,
        host: str,
        port: int
    ):

        if self.connected:

            raise RuntimeError(
                (
                    "Disconnect mount before "
                    "changing connection settings"
                )
            )

        self.host = host
        self.port = port

    def connect(self):
        if self.connected and self.socket is not None:
            return
        
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.socket.connect((self.host, self.port))

            self.connected = True

            self.socket.sendall(b':U2#')

            response = self.send_receive(":GVP#",terminator="#")

            if (not response or response == '#'):
                raise ConnectionError(
                    'Mount did not return a valid product name'
                )
            
            print(f'Connected to mount: {response.rstrip('#')}')

        except Exception:
            self.disconnect()
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
                self.disconnect()
                raise ConnectionError('Mount connection closed')

            response += chunk

            if terminator is None:
                return response

            if terminator in response:
                return response

    def send_receive(
        self,
        message,
        terminator
    ):

        if not self.connected:
            raise RuntimeError(
                'Mount not connected'
            )

        try:

            with self.command_lock:

                self.send(message)

                return self.receive(
                    terminator
                )


        except socket.timeout:
            self.disconnect()
            # A timeout does not necessarily mean
            # the TCP connection has been lost.
            raise TimeoutError(
                f'Mount response timeout for command: {message}'
            )


        except (
            ConnectionError,
            BrokenPipeError,
            ConnectionResetError,
            OSError
        ):

            self.disconnect()

            raise
