from PySide6.QtCore import QObject, Signal, QTimer
from Utilities.Observatory_Logger import ObservatoryLogger

class WeatherController(QObject):

    status_changed = Signal(str)
    connection_changed = Signal(bool)

    def __init__(self,monitor):
        super().__init__()

        self.monitor = monitor
        self.logger = ObservatoryLogger()

    def connect(self):
        self.status_changed.emit('Connecting...')
        try:
            self.monitor.connect()
            self.connection_changed.emit(True)

        except Exception as e:
            self.connection_changed.emit(False)
