from pymodbus.client import ModbusTcpClient
from Utilities.Config import *

class DomeConnection:

    def __init__(self,dome_host:str, dome_port: int):
        self.dome_host=dome_host
        self.dome_port=dome_port

        self.client = ModbusTcpClient(
            host=self.dome_host,
            port=self.dome_port
        )

        self.connected=False

    #########################################################################
    #                       Connection
    #########################################################################

    def connect(self):

        if self.connected:
            return True
        
        try:
            self.connected = self.client.connect()

            if self.connected:
                print(f'Connected to {self.dome_host}:{self.dome_port}')
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

    def is_connected(self):
        return self.connected
    
    #########################################################################
    #                       Coils
    #########################################################################

    def write_coil(
            self,
            address: int,
            value: bool,
            device_id: int=1
    ):
        if not self.connected:
            raise ConnectionError('Dome not connected')
        
        result = self.client.write_coil(
            address=address,
            value=value,
            device_id=device_id
        )

        if result.isError():
            raise RuntimeError(f'Failed to write to coil {address}')
        
        return result
    
    def read_coil(
            self,
            address: int,
            device_id: int=1
    ):
        if not self.connected:
            raise ConnectionError('Dome not connected')
        
        result = self.client.read_coils(
            address=address,
            count=1,
            device_id=device_id
        )

        if result.isError():
            raise RuntimeError(f'Failed to reads coil {address}')
        
        return result.bits[0]
    
    
    #########################################################################
    #                       Registers
    #########################################################################

    def read_register(
            self,
            address: int,
            device_id: int=1
    ):
        if not self.connected:
            raise ConnectionError('Dome not connected')
        
        result = self.client.read_holding_registers(
            address=address,
            count=1,
            device_id=device_id
        )

        if result.isError():
            raise RuntimeError(f'Failed to read register {address}')
        
        return result.registers[0]
    

    def write_register(
            self,
            address: int,
            value: int,
            device_id: int = 1
    ):
        if not self.connected:
            raise ConnectionError('Dome not connected')
        
        result = self.client.write_register(
            address=address,
            value=value,
            device_id=device_id
        )

        if result.isError():
            raise RuntimeError(f'Failed to write to register {address}')
        
        return result
    
    def configure(
        self,
        dome_host: str,
        dome_port: int
    ):
        if self.connected:
            raise RuntimeError(
                "Disconnect dome before changing "
                "connection settings"
            )

        self.dome_host = dome_host
        self.dome_port = dome_port

        # Recreate the Modbus client using
        # the new connection settings.
        self.client = ModbusTcpClient(
            host=self.dome_host,
            port=self.dome_port
        )