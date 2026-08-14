import time

class WeatherMonitor:

    def __init__(self):
        self.connected = False
        self.safe = False
        self.last_update = None

    def connect(self):
        self.connected = True
        return True

    def disconnect(self):
        self.conencted = False
        return True
    
    def is_connected(self):
        return self.connected

    def update(self):
        self.safe = False
        self.last_update = time.monotonic()

    def is_raining(self):
        raise NotImplementedError('Rain sensor not implemented yet')

    def wind_speed(self):
        raise NotImplementedError('Wind speed sensor not implemented yet')

    def humidity(self):
        raise NotImplementedError('Humidity sensor not implemented yet')