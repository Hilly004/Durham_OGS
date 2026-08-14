import time

class SafetyManager:

    def __init__(self, mount, dome, weather):
        self.weather = weather
        self.mount = mount
        self.dome = dome

    def get_status(self):
        if self.weather.last_update is None:
            return {
                'safe': False,
                'reason': 'Weather data unavailable'
            }

        if time.monotonic() - self.weather.last_update > 10:
            return {
                'safe': False,
                'reason': 'Weather data stale'
            }

        weather_status = self.weather.get_status()

        if not weather_status['safe']:
            return {
                'safe': False,
                'reason': weather_status['reason']
            }

        if self.dome.has_fault:
            return {
                'safe': False,
                'reason': 'Dome fault detected'
            }

        return {
            'safe': True,
            'reason': None
        }
    

    def is_safe(self):
        return self.get_status()['safe']
    
    def can_close_dome(self):
        return True

    def can_unpark_mount(self):
        return self.is_safe()

    def can_start_observing(self):
        return self.is_safe()

