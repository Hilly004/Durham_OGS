from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QGridLayout,
    QGroupBox,
    QLineEdit
)

from PySide6.QtCore import Qt, QTimer
import time


class MountPage(QWidget):

    def __init__(self,controller, main_window):
        super().__init__()

        self.controller = controller
        self.main_window = main_window

        ##### STATUS #####

        status_box = QGroupBox('Status')
        status_layout = QGridLayout()

        self.connection_status = QLabel('Checking...')
        self.right_ascension = QLabel('Checking...')
        self.declination = QLabel('Checking...')
        self.altitude = QLabel('Checking...')
        self.azimuth = QLabel('Checking...')
        self.park_status = QLabel('')

        self.connection_button = QPushButton('Connect')
        self.connection_button.clicked.connect(self.toggle_connection)
        self.position_button = QPushButton('Get position')
        self.export_button = QPushButton('Export')


        self.position_button.clicked.connect(self.controller.update_position)
        self.position_button.clicked.connect(self.controller.update_position_aa)

        self.export_button.clicked.connect(
            lambda: self.controller.logger.export_to_csv('mount_log.csv'))

        status_layout.addWidget(self.connection_button,5,0,1,2)
        status_layout.addWidget(self.position_button,6,0,1,2)
        status_layout.addWidget(self.export_button,7,0,1,2)

        status_layout.addWidget(QLabel('Connection status:'),2,0)
        status_layout.addWidget(self.connection_status,2,1)

        status_layout.addWidget(QLabel('Right Ascension:'),0,0)
        status_layout.addWidget(self.right_ascension,0,1)

        status_layout.addWidget(QLabel('Declination:'),1,0)
        status_layout.addWidget(self.declination,1,1)

        status_layout.addWidget(QLabel('Altitude:'),3,0)
        status_layout.addWidget(self.altitude,3,1)

        status_layout.addWidget(QLabel('Azimuth:'),4,0)
        status_layout.addWidget(self.azimuth,4,1)

        status_layout.addWidget(self.park_status,8,0,1,2)

        status_box.setLayout(status_layout)

        ##### CONTROL #####

        control_box = QGroupBox('Control')
        control_layout = QGridLayout()

        self.up_button = QPushButton('\u2191') #up arrow
        self.down_button = QPushButton('\u2193') #down arrow
        self.left_button = QPushButton('\u2190') #left arrow
        self.right_button = QPushButton('\u2192') #right arrow

        self.up_button.pressed.connect(self.controller.move_north)
        self.up_button.released.connect(self.controller.stop_north)
        
        self.down_button.pressed.connect(self.controller.move_south)
        self.down_button.released.connect(self.controller.stop_south)

        self.left_button.pressed.connect(self.controller.move_west)
        self.left_button.released.connect(self.controller.stop_west)

        self.right_button.pressed.connect(self.controller.move_east)
        self.right_button.released.connect(self.controller.stop_east)


        self.ra_input = QLineEdit()
        self.dec_input = QLineEdit()
        self.set_target_button = QPushButton('Set target')
        self.slew_button = QPushButton('Slew to target')

        self.ra_input.setPlaceholderText('HH:MM:SS')
        self.dec_input.setPlaceholderText('DD*MM:SS')
        self.set_target_button.clicked.connect(self.set_target)

        self.slew_button.clicked.connect(self.controller.slew_to_target)

        control_layout.addWidget(QLabel('Input right ascension:'),0,0)
        control_layout.addWidget(self.ra_input,0,1)
        control_layout.addWidget(QLabel('Input declination:'),1,0)
        control_layout.addWidget(self.dec_input,1,1)
        control_layout.addWidget(self.set_target_button,2,0)
        control_layout.addWidget(self.slew_button,2,1)

        control_layout.addWidget(QLabel('Manual controls:'),0,3,1,3)
        control_layout.addWidget(self.up_button,1,4) 
        control_layout.addWidget(self.down_button,2,4)
        control_layout.addWidget(self.left_button,2,3)
        control_layout.addWidget(self.right_button,2,5)

        self.park_button = QPushButton('Park mount')
        self.unpark_button = QPushButton('Unpark mount')
        self.slew_to_park_button = QPushButton('Slew to park position')

        self.park_button.clicked.connect(self.controller.set_park_position)
        self.unpark_button.clicked.connect(self.controller.unpark)
        self.slew_to_park_button.clicked.connect(self.controller.slew_to_park)
        
        control_layout.addWidget(self.park_button,3,0)
        control_layout.addWidget(self.unpark_button,3,1)
        control_layout.addWidget(self.slew_to_park_button,4,0,1,2)
        control_box.setLayout(control_layout)

        ##### CAMERA/MAP #####

        cam_box = QGroupBox('Camera')
        cam_layout = QGridLayout()

        self.point_button = QPushButton('Go to pointing page')
        self.point_button.clicked.connect(self.main_window.show_point)

        cam_layout.addWidget(self.point_button)

        cam_box.setLayout(cam_layout)

        layout = QGridLayout()

        layout.addWidget(status_box,0,0,1,1)
        layout.addWidget(control_box,1,0,1,1)
        layout.addWidget(cam_box,0,1,2,2)


        self.setLayout(layout)

        self.controller.connection_changed.connect(self.update_connection_status)
        self.controller.position_changed.connect(self.update_position)
        self.controller.position_aa_changed.connect(self.update_position_aa)
        self.controller.status_changed.connect(self.update_status)
        self.controller.park_changed.connect(self.update_parking)

    def update_connection_status(self, connected):
        if connected:
            self.connection_button.setText('Disconnect')
        else:
            self.connection_button.setText('Connect')

    def toggle_connection(self):
        if self.controller.is_connected(): 
            self.controller.disconnect()
        else:
            self.controller.connect()

    def update_status(self,status):
        self.connection_status.setText(status)

    def update_position(self, position):

        self.right_ascension.setText(position['ra'])
        self.declination.setText(position['dec'])

    def update_position_aa(self,position_aa):
    
        self.altitude.setText(position_aa['alt'])
        self.azimuth.setText(position_aa['az'])

    def set_target(self):
        ra = self.ra_input.text()
        dec = self.dec_input.text()
        self.controller.set_target_ra(ra)
        self.controller.set_target_dec(dec)

    def update_parking(self, parked):
        if parked:
            self.park_status.setText('Parked')
        else:
            self.park_status.setText('')
