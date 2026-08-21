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

    def send_receive(
        self,
        message,
        terminator='#'
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

    def send_command_char(
        self,
        command: str
    ):

        if not self.is_connected():

            raise ConnectionError(
                "Mount not connected"
            )


        with self.lock:

            try:

                self.socket.sendall(
                    command.encode(
                        "ascii"
                    )
                )


                response = (
                    self.socket.recv(1)
                )


                if not response:

                    raise TimeoutError(
                        (
                            "Mount response timeout "
                            f"for command: {command}"
                        )
                    )


                return (
                    response
                    .decode(
                        "ascii",
                        errors="ignore"
                    )
                )


            except TimeoutError:

                raise


            except Exception as e:

                raise RuntimeError(
                    (
                        "Mount command failed "
                        f"{command}: {e}"
                    )
                ) from e
    

    def send_receive_byte(
        self,
        message: str
    ):

        if not self.connected:
            raise ConnectionError(
                "Mount not connected"
            )

        try:

            self.socket.sendall(
                message.encode()
            )

            response = (
                self.socket
                .recv(1)
                .decode()
            )

            return response

        except TimeoutError:

            raise TimeoutError(
                f"Mount response timeout "
                f"for command: {message}"
            )