# -*- coding: utf-8 -*-
"""
Created on June 2024

@author: Ghimciuc Mihail
"""
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import QMainWindow, QTextEdit, QToolBar, QWidget, QStackedWidget, QComboBox, QLabel, QListWidget, \
    QPushButton, QHBoxLayout, QVBoxLayout, QAbstractItemView
import logging
import gui.windows.SubjectSelection as SubjectSelection
import gui.windows.DataProcessing as DataProcessing
import gui.windows.DataExport as DataExport


class MainWindow(QMainWindow):
    def __init__(self, logger: logging.Logger, config: dict, parent=None):
        super().__init__(parent)  # Initialize QMainWindow
        self.logger: logging.Logger = logger
        self.config = config
        self.setWindowTitle("Dynamic Interface Example")

        # Create the stacked widget
        self.stacked_widget = QStackedWidget()

        self.subject_selection = SubjectSelection.SubjectSelection(self, self.logger, lambda: self.switch_interface(1))
        self.data_processing = DataProcessing.DataProcessing(self, self.logger, lambda: self.switch_interface(0),
                                                             lambda: self.switch_interface(2))
        self.data_export = DataExport.DataExport(self, self.logger, lambda: self.switch_interface(1),
                                                 lambda: self.switch_interface(0))
        self.subject_selection.connect_update_callbacks([self.data_processing.update_subject,
                                                         self.data_export.update_subject])

        # Add the interfaces to the stacked widget
        self.stacked_widget.addWidget(self.subject_selection)
        self.stacked_widget.addWidget(self.data_processing)
        self.stacked_widget.addWidget(self.data_export)

        # Layout to hold the combobox and stacked widget
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.build()

    def build(self):
        self.setWindowTitle(self.config['window']['title'])
        self.setGeometry(100, 100, self.config['window']['width'], self.config['window']['height'])

        # Set up status bar
        self.statusBar().showMessage('Ready')

    def switch_interface(self, index):
        self.stacked_widget.setCurrentIndex(index)