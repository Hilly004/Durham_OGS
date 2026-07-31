from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QGroupBox, QPushButton,QHBoxLayout


class HomePage(QWidget):

    def __init__(self,controller,main_window):
        super().__init__()

        self.controller = controller
        self.main_window = main_window

        page_box = QGroupBox('')
        page_layout = QGridLayout()

        dashboard_button = QPushButton('Dashboard')
        mount_button = QPushButton('Mount')
        dome_button = QPushButton('Dome')
        weather_button = QPushButton('Weather')
        camera_button = QPushButton('Camera')
        settings_button = QPushButton('Settings')
        logs_button = QPushButton('Logs')

        page_layout.addWidget(dashboard_button)
        page_layout.addWidget(mount_button)
        page_layout.addWidget(dome_button)
        page_layout.addWidget(weather_button)
        page_layout.addWidget(camera_button)
        page_layout.addWidget(settings_button)
        page_layout.addWidget(logs_button)

        page_box.setLayout(page_layout)

        #####

        status_box = QGroupBox('Status')
        status_layout = QGridLayout()

        status_layout.addWidget(QLabel('Connection status:'),0,0)
        status_layout.addWidget(QLabel('Mount:'),1,0)
        status_layout.addWidget(QLabel('Dome:'),2,0)

        self.mount_connection_status = QLabel('')
        self.dome_connection_status = QLabel('')
        
        status_layout.addWidget(self.mount_connection_status,1,1)
        status_layout.addWidget(self.dome_connection_status,2,1)

        status_box.setLayout(status_layout)

        layout = QGridLayout()
        layout.addWidget(page_box,0,0)
        layout.addWidget(status_box,1,0,1,2)
        layout.addWidget(QLabel('Box'),0,1)

        self.setLayout(layout)


        self.update_connection_status
        self.controller.connection_changed.connect(self.update_connection_status)

    def update_connection_status(self,connected):
        if connected:
            self.mount_connection_status.setText('Connected')
            #self.mount_connection_button.setText('Disconnect')
        else:
            self.mount_connection_status.setText('Not connected')
            #self.mount_connection_button.setText('Connect')

    def toggle_connection(self):
        if self.controller.is_connected(): 
            self.controller.disconnect()

        else:
            self.controller.connect()
            
