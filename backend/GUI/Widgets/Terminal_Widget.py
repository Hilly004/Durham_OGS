from PySide6.QtWidgets import QPlainTextEdit,QWidget,QPushButton,QVBoxLayout,QHBoxLayout

class TerminalWidget(QWidget):

    def __init__(self,logger):
        super().__init__()

        self.logger = logger

        self.text = QPlainTextEdit()
        self.setReadOnly(True)
        self.setMaximumHeight(180)

        self.export_button = QPushButton('Export to CSV')

        layout = QVBoxLayout(self)

        header = QHBoxLayout()

        header.addStretch()
        header.addWidget(self.export_button)

        layout.addLayout(header)
        layout.addWidget(self.text)

        logger.message.connect(self.write)

        self.export_button.clicked.connect(
            lambda: logger.export_to_csv('terminal_log.csv')
        )
        
    def write(self,text):
        self.appendPlainText(text)
