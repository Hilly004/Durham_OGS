from pymodbus.client import ModbusTcpClient
from Utilities.Config import *

class DomeConnection:

    def __init__(self, dome_host:str, dome_port:int):
        self.dome_host = dome_host
        self.dome_port = dome_port

        self.client = ModbusTcpClient(self.dome_host,self.dome_port)

        self.connected = False

    def connect(self):
        if self.connected:
            return
        
        try:
            self.client.connect()
            
            if self.connected:
                print('Connnected')
            else:
                print('Unable to connect')

            return self.connected

        except Exception as e:
            print(f'Connection error: {e}')
            self.connected = False
            return False
    
    def disconnect(self):
        if self.connected:
            self.client.close()
            self.connected = False
            print('Disconnected')

    def send(self,msg):
        if self.connected:
            self.client.send(msg)
        else:
            print('Domne not connected')

    def receive(self,msg):
        if self.connected:
            self.client.recv(msg)
        else:
            print('Dome not connected')

    def send_recv(self,msg):
        if self.connected:
            self.connect(msg)
            self.receive(msg)
        else:
            print('Dome not connected')

    