from PySide6.QtCore import QObject, Signal, QTimer

from Utilities.Observatory_Logger import ObservatoryLogger

class DomeController:

    connection_changed = Signal(bool)
    status_changed = Signal(str)
    left_changed = Signal(str)
    right_changed = Signal(str)

    def __init__(self,dome):
        super().__init__()

        self.dome = dome
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

    @property
    def is_connected(self):
        return self.dome.is_connected()
    
    @property
    def is_open(self):
        return self.dome.all_open

    @property
    def is_moving(self):
        return self.dome.either_motor_running

    def get_status(self):
        return {
            'connected': self.is_connected,
            'open': self.is_open,
            'moving': self.is_moving,
            'fault': self.has_fault
        }

    def open_dome(self):
        self.status_changed.emit('Dome opening...')
        self.dome.open_dome()

    
    def close_dome(self):
        self.status_changed.emit('Dome closing...')
        self.dome.close_dome()
    

    def open_left(self):
        self.status_changed.emit('Left side opening...')
        self.dome.open_left()
    
    def open_right(self):
        self.status_changed.emit('Right side opening...')
        self.dome.open_right()
    
    def close_left(self):
        self.status_changed.emit('Left side closing')
        self.dome.close_left()

    def close_right(self):
        self.status_changed.emit('Right side closing')
        self.dome.close_right()

    @property
    def has_fault(self):
        return self.dome.fault()