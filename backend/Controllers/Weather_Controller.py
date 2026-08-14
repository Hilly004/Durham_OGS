from Utilities.Observatory_Logger import ObservatoryLogger

class WeatherController:

    def __init__(self,monitor):

        self.monitor = monitor
        self.logger = ObservatoryLogger()

    def connect(self):
        try:
            self.monitor.connect()

        except Exception as e:
            print(f'Weather monitor connection failed: {e}')
            return False

    def disconnect(self):
        return self.monitor.disconnect()


    @property
    def is_connected(self):
        return self.monitor.is_connected()

    def safe(self):
        if not self.is_connected:
            return False
        try:
            raining=self.monitor.is_raining()
            wind_speed=self.monitor.wind_speed()
            humidity=self.monitor.humidity()
        
        except Exception as e:
            print(f'Unable to determine weather safety: {e}')
            return False

        return(
            not raining
            and wind_speed<40
            and humidity<95
        )