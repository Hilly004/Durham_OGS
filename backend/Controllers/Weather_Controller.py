from Utilities.Observatory_Logger import ObservatoryLogger

class WeatherController:

    def __init__(self,monitor):

        self.monitor = monitor
        self.logger = ObservatoryLogger()

    def connect(self):
        try:
            self.monitor.connect()

        except Exception as e:
            self.logger.error(f'Weather monitor connection failed: {e}')
            return False

    def disconnect(self):
        return self.monitor.disconnect()


    @property
    def is_connected(self):
        return self.monitor.is_connected()

    def update(self):
        return self.monitor.update()

    @property
    def last_update(self):
        return self.monitor.last_update

    def safe(self):
        return self.get_status()['safe']
    
    def get_status(self):
        if not self.is_connected:
            return {
                'state': 'unknown',
                'safe': False,
                'reason': 'Weather station disconnected'
            }

        try:
            raining = self.monitor.is_raining()
            wind_speed = self.monitor.wind_speed()
            humidity = self.monitor.humidity()

        except Exception as e:
            self.logger.error(
                f'Unable to read weather conditions: {e}'
            )

            return {
                'state': 'unknown',
                'safe': False,
                'reason': 'Weather data unavailable'
            }

        if raining:
            return {
                'state': 'unsafe',
                'safe': False,
                'reason': 'Rain detected'
            }

        if wind_speed >= 40:
            return {
                'state': 'unsafe',
                'safe': False,
                'reason': 'Wind speed above safety limit'
            }

        if humidity >= 95:
            return {
                'state': 'unsafe',
                'safe': False,
                'reason': 'Humidity above safety limit'
            }

        return {
            'state': 'safe',
            'safe': True,
            'reason': None
        }