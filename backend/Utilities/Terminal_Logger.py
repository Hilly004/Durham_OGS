from PySide6.QtCore import QObject, Signal
from datetime import datetime
import csv

class TerminalLogger(QObject):
    message = Signal(str)

    def __init__(self,logger):
        super().__init__()
        self.messages = []

    def log(self,text):

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.messages.append((timestamp, text))

        self.message.emit(f'[{timestamp}] {text}')
