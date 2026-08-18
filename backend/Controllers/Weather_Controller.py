class WeatherController:

    def __init__(self,monitor,logger):

        self.monitor = monitor
        self.logger = logger
        
        # None = use real weather
        # True = force safe
        # False = force unsafe
        self._safety_override = True

    def set_safety_override(self, value: bool | None):
        self._safety_override = value

        if value is True:
            self.logger.warning(
                "Weather safety override enabled: FORCE SAFE",
                source="WEATHER"
            )

        elif value is False:
            self.logger.warning(
                "Weather safety override enabled: FORCE UNSAFE",
                source="WEATHER"
            )

        else:
            self.logger.info(
                "Weather safety override disabled",
                source="WEATHER"
            )


    def get_safety_override(self):
        return self._safety_override

    
    def connect(self):

        try:
            connected = self.monitor.connect()

            if not connected:
                self.logger.error(
                    "Weather station connection failed",
                    source="WEATHER"
                )
                return False

            if not self.monitor.is_connected():
                self.logger.error(
                    "Weather station connection failed",
                    source="WEATHER"
                )
                return False

            self.logger.success(
                "Weather station connected",
                source="WEATHER"
            )

            return True

        except Exception as e:

            self.logger.error(
                f"Weather station connection failed: {e}",
                source="WEATHER"
            )

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
        if self._safety_override is not None:
            return self._safety_override
        
        return self.get_status()['safe']
    
    def get_status(self):

        actual_safe = self.monitor.safe
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