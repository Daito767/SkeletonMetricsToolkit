import time

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QTextEdit, QToolBar
import logging


class MainWindow(QMainWindow):
    def __init__(self, logger: logging.Logger, config: dict, parent=None):
        super().__init__(parent)  # Initialize QMainWindow
        self.logger: logging.Logger = logger
        self.config = config
        self.build()

    def build(self):
        self.setWindowTitle(self.config['window']['title'])
        self.setGeometry(100, 100, self.config['window']['width'], self.config['window']['height'])

        # Set up central widget
        central_widget = QTextEdit()
        self.setCentralWidget(central_widget)

        # Set up menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        open_action = QAction('Open', self)
        file_menu.addAction(open_action)

        save_action = QAction('Save', self)
        file_menu.addAction(save_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Set up toolbar
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        toolbar.addAction(open_action)
        toolbar.addAction(save_action)

        # Set up status bar
        self.statusBar().showMessage('Ready')
