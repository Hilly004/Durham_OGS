import sys

from PySide6.QtWidgets import QApplication


from factory import build_observatory

from GUI.Main_Window import MainWindow

from Utilities.Config import *

from Utilities.Observatory_Logger import ObservatoryLogger



def main():
    app = QApplication(sys.argv)

    observatory = build_observatory()

    logger = ObservatoryLogger()

    window = MainWindow(observatory)
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()

