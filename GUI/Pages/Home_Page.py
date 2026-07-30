from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QGroupBox, QPushButton

class HomePage(QWidget):

    def __init__(self,controller,main_window):
        super().__init__()

        self.controller = controller
        self.main_window = main_window

        connection_box = QGroupBox('')
        connection_layout = QGridLayout()

        #self.dome_connection_button = QPushButton()
        self.mount_connection_button = QPushButton('Connect')
        self.mount_connection_button.clicked.connect(self.toggle_connection)

        connection_layout.addWidget(self.mount_connection_button)

        connection_box.setLayout(connection_layout)


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
        layout.addWidget(status_box,1,0)
        layout.addWidget(connection_box,0,0)

        self.setLayout(layout)


        self.update_connection_status
        self.controller.connection_changed.connect(self.update_connection_status)

    def update_connection_status(self,connected):
        if connected:
            self.mount_connection_status.setText('Connected')
        else:
            self.mount_connection_status.setText('Not connected')

    def toggle_connection(self):
        if self.controller.is_connected(): 
            self.controller.disconnect()
            self.mount_connection_button.setText('Connect')
        else:
            self.controller.connect()
            self.mount_connection_button.setText('Disconnect')
