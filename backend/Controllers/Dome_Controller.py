from PySide6.QtCore import QObject, Signal, QTimer

from Utilities.Observatory_Logger import ObservatoryLogger

class DomeController(QObject):

    connection_changed = Signal(bool)
    status_changed = Signal(str)

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

    def is_connected(self):
        return self.dome.is_connected()