from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QGridLayout,
    QGroupBox,
    QLineEdit
)

class PointingWidget(QWidget):

    def __init__(self,controller,main_window):
        super().__init__()

        self.controller = controller


        set_aa_box = QGroupBox('Set alt and az')
        set_aa_layout = QGridLayout()

        self.alt_input = QLineEdit()
        self.az_input = QLineEdit()
        self.enter_button = QPushButton('Enter')
        self.track_button = QPushButton('Track')
        self.status_button = QPushButton('Get tracking status')
        self.stop_button = QPushButton('Stop tracking')

        set_aa_layout.addWidget(QLabel('Input target altitude:'),0,0)
        set_aa_layout.addWidget(self.alt_input,0,1)
        set_aa_layout.addWidget(QLabel('Input target azimuth:'),1,0)
        set_aa_layout.addWidget(self.az_input,1,1)
        set_aa_layout.addWidget(self.enter_button,2,0,1,2)
        set_aa_layout.addWidget(self.track_button,3,0,1,2)
        set_aa_layout.addWidget(self.status_button,4,0,1,2)
        set_aa_layout.addWidget(self.stop_button,5,0,1,2)


        self.enter_button.clicked.connect(self.set_aa_target)
        self.track_button.clicked.connect(self.track)
        self.status_button.clicked.connect(self.status)
        self.stop_button.clicked.connect(self.controller.stop_tracking)

        set_aa_box.setLayout(set_aa_layout)

        layout = QGridLayout()

        layout.addWidget(set_aa_box)

        self.setLayout(layout)

    def set_aa_target(self):
        alt = self.alt_input.text()
        az = self.az_input.text()
        self.controller.set_target_altitude(alt)
        self.controller.set_target_azimuth(az)

    def track(self):
        self.controller.get_target_ra()
        self.controller.get_target_dec()
        self.controller.slew_to_target()

    def status(self):
        print(self.controller.get_tracking_status())