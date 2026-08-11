import time

class SafetyManager:

    def __init__(self, mount, dome, weather):
        self.weather = weather
        self.mount = mount
        self.dome = dome

    def is_safe(self):
        if not self.weather.is_connected:
            return False
        
        if self.weather.last_update is None:
            return False

        if time.monotonic() - self.weather.last_update >10:
            return False

        if not self.weather.safe:
            return False
        
        if self.dome.has_fault:
            return False
        
        return True

    
    def can_close_dome(self):


    def can_unpark_mount(self):


    def can_start_observing(self):

