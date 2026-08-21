from Utilities import *
import serial
import time

class WeatherConnection:

    def __init__(self, weather_port, weather_baudrate):
        self.weather_port = weather_port
        self.weather_baudrate = weather_baudrate
        
        self.serial = None
        self.last_update = None

    def connect(self):
        if self.serial and self.serial.is_open:
            return
        

        self.serial = serial.Serial(
                port = self.weather_port,
                baudrate = self.weather_baudrate,
                bytesize = serial.EIGHTBITS,
                parity = serial.PARITY_NONE,
                stopbits = serial.STOPBITS_ONE,
                timeout = 2,
            )
            
            
    def disconnect(self):
        if self.serial and self.serial.is_open:
            self.serial.close()


    def send_receive(self,command: str) -> str:
        if not self.serial or not self.serial.is_open:
            raise RuntimeError('Weather monitor not connected')
        

    def configure(
        self,
        weather_port: str,
        weather_baudrate: int
    ):
        if (
            self.serial is not None
            and self.serial.is_open
        ):
            raise RuntimeError(
                "Disconnect weather station before "
                "changing connection settings"
            )

        self.weather_port = weather_port
        self.weather_baudrate = weather_baudrate
            
        