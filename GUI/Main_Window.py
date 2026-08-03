from PySide6.QtWidgets import (
    QMainWindow,
    QStackedWidget,
    QPlainTextEdit,
    QWidget,
    QVBoxLayout
)

from PySide6.QtGui import QAction

from GUI.Pages.Mount_Page import MountPage
from GUI.Widgets.Mount.Pointing import PointingWidget
from GUI.Pages.Home_Page import HomePage
from GUI.Pages.Authentication import Authenticator
from GUI.Pages.Password_Page import PasswordWindow
from GUI.Widgets.Terminal_Widget import TerminalWidget

from Utilities.Terminal_Logger import TerminalLogger

class MainWindow(QMainWindow):

    def __init__(self,observatory):
        super().__init__()

        self.observatory = observatory

        self.auth = Authenticator()
        self.terminal = TerminalWidget()
        self.logger = TerminalLogger()

        self.logger.message.connect(self.terminal.write)
        
        self.home_page = HomePage(observatory.mount_controller,self)
        self.mount_page = MountPage(observatory.mount_controller,self)
        self.point_page = PointingWidget(observatory.mount_controller,self)

        self.login_page = PasswordWindow(self.auth)

        self.stack = QStackedWidget()

        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.mount_page)
        self.stack.addWidget(self.point_page)

        self.stack.setCurrentWidget(self.login_page)

        self.login_page.authenticated.connect(self.login_success)

        self.logger.log('Mount connected')

        self.create_menu()

        central = QWidget()

        main_layout = QVBoxLayout(central)

        main_layout.addWidget(self.stack)
        main_layout.addWidget(self.terminal)

        self.setCentralWidget(central)

        
    def show_home(self):
        self.stack.setCurrentWidget(self.home_page)

    def show_mount(self):
        self.stack.setCurrentWidget(self.mount_page)

    def show_point(self):
        self.stack.setCurrentWidget(self.point_page)
    
    def create_menu(self):
        home_button = QAction('Home',self)
        home_button.triggered.connect(
            lambda: self.stack.setCurrentWidget(self.home_page)
        )

        mount_button = QAction('Mount',self)
        mount_button.triggered.connect(
            lambda: self.stack.setCurrentWidget(self.mount_page)
        )
        menu = self.menuBar()

        navigate_menu = menu.addMenu('&Navigate')
        navigate_menu.addAction(home_button)
        navigate_menu.addAction(mount_button)

        self.menuBar().setEnabled(True)

    def login_success(self):
        self.stack.setCurrentWidget(self.home_page)
        self.menuBar().setEnabled(True)

    def closeEvent(self, event):
        self.observatory.shutdown()
        event.accept()

    def append_terminal(self,text):
        self.terminal.appendPlainText(text)
