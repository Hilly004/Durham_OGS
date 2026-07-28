import sys

from PySide6.QtWidgets import QApplication


from Hardware.Connections.Mount_Connection import MountConnection
from Hardware.Mount.Mount_Commands import TenMicronMount
from Controllers.Mount_Controller import MountController

from GUI.Pages.Mount_Page import MountPage

from Utilities.Config import *




def main():
    app = QApplication(sys.argv)

    mount_connection = MountConnection(host,port)
    mount = TenMicronMount(mount_connection)
    mount_controller = MountController(mount)
    mount_window = MountPage(mount_controller)

    mount_window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()

