class SafetyManager:

    def open_safe(self):
        return (
            not self.weather.is_raining()
            and self.weather.wind_speed() < 40
            and self.weather.humidity() <95
        )