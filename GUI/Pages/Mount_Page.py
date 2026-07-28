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

        ##### STATUS #####

        status_box = QGroupBox('Status')
        status_layout = QGridLayout()

        

        self.connection_status = QLabel('Checking...')
        self.right_ascension = QLabel('Checking...')
        self.declination = QLabel('Checking...')

        self.connect_button = QPushButton('Connect')
        self.disconnect_button = QPushButton('Disconnect')
        self.position_button = QPushButton('Get position')

        self.connect_button.clicked.connect(self.controller.connect)
        self.disconnect_button.clicked.connect(self.controller.disconnect)
        self.position_button.clicked.connect(self.controller.update_position)

        status_layout.addWidget(self.connect_button,3,0)
        status_layout.addWidget(self.disconnect_button,3,1)
        status_layout.addWidget(self.position_button,4,0,1,2)

        status_layout.addWidget(QLabel('Connection status:'),2,0)
        status_layout.addWidget(self.connection_status,2,1)

        status_layout.addWidget(QLabel('Right Ascension:'),0,0)
        status_layout.addWidget(self.right_ascension,0,1)

        status_layout.addWidget(QLabel('Declination:'),1,0)
        status_layout.addWidget(self.declination,1,1)

        status_box.setLayout(status_layout)

        layout = QGridLayout()

        layout.addWidget(status_box)


        self.setLayout(layout)

        self.controller.connection_changed.connect(self.update_connection_status)
        self.controller.position_changed.connect(self.update_position)

    def update_connection_status(self, connected):
        if connected:
            self.connection_status.setText('Connected')
        else:
            self.connection_status.setText('Disconnected')

    def update_position(self, position):
        self.right_ascension.setText(position['ra'])
        self.declination.setText(position['dec'])