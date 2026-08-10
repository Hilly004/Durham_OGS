class SafetyManager:

    def __init__(self, mount, dome, weather):
        self.weather = weather
        self.mount = mount
        self.dome = dome

    def is_safe(self):
        if not self.weather.connected:
            return False

        if not self.weather.safe:
            return False
        
        if self.dome.has_fault:
            return False
        
        return True

    def open_safe(self):
        return (
            not self.weather.is_raining()
            and self.weather.wind_speed() < 40
            and self.weather.humidity() <95
        )