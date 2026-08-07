from PySide6.QtCore import QObject, Signal, QTimer

from Utilities.Observatory_Logger import ObservatoryLogger

class DomeController(QObject):

    connection_changed = Signal(bool)
    status_changed = Signal(str)
    left_changed = Signal(str)
    right_changed = Signal(str)

    def __init__(self,dome,safety):
        super().__init__()

        self.dome = dome
        self.safety = safety
        self.logger = ObservatoryLogger()

    def connect(self):
        try:
            self.status_changed.emit('Connecting...')
            self.dome.connect()
            self.connection_changed.emit(True)
            self.status_changed.emit('Dome connected')

        except Exception as e:
            self.connection_changed.emit(False)
            self.status_changed.emit(f'Connection failed: {e}')

    def disconnect(self):
        self.status_changed.emit('Disconnecting...')
        self.dome.disconnect()
        self.connection_changed.emit(False)
        self.status_changed.emit('Dome not connected')

    def is_connected(self):
        return self.dome.is_connected()
    




    def open_dome(self, force=False):
        if not force and not self.safety.open_safe():
            self.status_changed.emit('Unsafe conditions - dome will not open')
            return False
        
        self.dome.open_dome()
        return True
    
    def close_dome(self):
        self.dome.close_dome()
    

    def open_left(self, force=False):
        if not force and not self.safety.open_safe():
            self.status_changed.emit('Unsafe conditions - dome will not open')
            return False
        
        self.dome.open_left()
        return True
    
    def open_right(self, force=False):
        if not force and not self.safety.open_safe():
            self.status_changed.emit('Unsafe conditions - dome will not open')
            return False

        self.dome.open_right()
        return True
    
    def close_left(self):
        self.dome.close_dome()

    def close_right(self):
        self.dome.close_right()

    