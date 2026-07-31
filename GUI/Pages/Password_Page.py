from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout
)

from PySide6.QtCore import Signal, Qt

class PasswordWindow(QWidget):
    authenticated = Signal()

    def __init__(self,auth):
        super().__init__()

        self.auth = auth

        title = QLabel('Login')

        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet('font-size: 20px; font-weight:bold')

        self.user_box = QLineEdit()
        self.user_box.setPlaceholderText('Username')

        self.password_box = QLineEdit()
        self.password_box.setPlaceholderText('Password')

        self.password_box.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_box.returnPressed.connect(self.check_login)

        self.status = QLabel('')
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        login_button = QPushButton('Login')
        login_button.clicked.connect(self.check_login)

        login_panel = QWidget()
        login_panel.setFixedSize(200,130)

        layout = QVBoxLayout(login_panel)
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(self.user_box)
        layout.addWidget(self.password_box)
        layout.addWidget(login_button)
        layout.addWidget(self.status)

        self.setLayout(layout)


    def check_login(self):

        if self.auth.authenticate(
            self.user_box.text(),
            self.password_box.text()
        ):
            self.authenticated.emit()

        else:
            self.status.setText('Incorrect username or password')
            self.password_box.clear()