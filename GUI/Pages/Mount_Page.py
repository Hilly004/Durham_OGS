from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QGridLayout,
    QGroupBox,
    QLineEdit
)

from PySide6.QtCore import Qt, QTimer

class MountPage(QWidget):

    def __init__(self,controller):
        super().__init__()

        self.controller = controller

        self.controller.connection_changed.connect(self.update_connection)
        

        self.connection_label = QLabel('Checking...')
        self.ra_label = QLabel('Checking...')
        self.dec_label = QLabel('Checking...')
        self.status_label = QLabel('Ready')

        self.refresh_button = QPushButton('Refresh')
        self.connect_button = QPushButton('Connect')

        self.refresh_button.clicked.connect(self.controller.refresh)

        self.connect_button.clicked.connect(self.controller.connect)

        status_box = QGroupBox('Status')
        status_layout = QGridLayout()
        status_layout.addWidget(QLabel('Connection status:'),0,0)
        status_layout.addWidget(self.connection_label,0,1)
        status_layout.addWidget(QLabel('Right ascension:'),1,0)
        status_layout.addWidget(self.ra_label,1,1)
        status_layout.addWidget(QLabel('Declination:'),2,0)
        status_layout.addWidget(self.dec_label,2,1)
        status_layout.addWidget(self.refresh_button,3,0,1,2)
        status_layout.addWidget(self.connect_button,4,0,1,2)

        status_box.setLayout(status_layout)


        main_layout = QGridLayout(self)
        main_layout.addWidget(status_box,0,0)
    

    def update_connection(self,connected):
        print('update_connection:', connected)
        if connected:
            self.connection_label.setText('Connected')
        else:
            self.connection_label.setText('Disconnected')

    def update_position(self, position):
        self.ra_label.setText(str(position['ra']))
        self.dec_label.setText(str(position['dec']))
        
    def update_status(self,status):
        self.status_label.setText(status)
