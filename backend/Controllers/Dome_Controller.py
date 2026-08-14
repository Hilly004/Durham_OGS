from Utilities.Observatory_Logger import ObservatoryLogger

class DomeController:

    def __init__(self,dome):
        self.dome = dome
        self.logger = ObservatoryLogger()

    def connect(self):
        try:
            self.dome.connect()
        except Exception as e:
            self.logger.error(f'Dome connection failed: {e}')
            return False

    def disconnect(self):
        return self.dome.disconnect()

    @property
    def is_connected(self):
        return self.dome.is_connected()
    
    @property
    def is_open(self):
        return self.dome.all_open()

    @property
    def is_moving(self):
        return self.dome.either_motor_running()

    def get_status(self):
        return {
            'connected': self.is_connected,
            'open': self.is_open,
            'moving': self.is_moving,
            'fault': self.has_fault
        }

    def open_dome(self):
        return self.dome.open_dome()

    
    def close_dome(self):
        return self.dome.close_dome()
    

    def open_left(self):
        return self.dome.open_left()
    
    def open_right(self):
        return self.dome.open_right()
    
    def close_left(self):
        return self.dome.close_left()

    def close_right(self):
        return self.dome.close_right()

    @property
    def has_fault(self):
        return self.dome.fault()