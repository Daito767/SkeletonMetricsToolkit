# -*- coding: utf-8 -*-
"""
Created on June 2024

@author: Ghimciuc Mihail
"""
from logging import Logger

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMainWindow, QWidget, QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton, QComboBox, \
    QTextEdit, QLineEdit, QHBoxLayout, QSpacerItem, QSizePolicy
from calculations.operation import OperationManager
import logging


class CreateOperationDialog(QDialog):
    def __init__(self, parent_widget: QWidget, logger: logging.Logger, operation_manager: OperationManager, parent=None):
        self.logger: logging.Logger = logger
        self.logger.info("Initializing CreateOperation Dialog")
        self.operation_manager: OperationManager = operation_manager

        super().__init__(parent)  # Initialize QDialog

        self.parent_widget: QWidget = parent_widget

        self.layout: QVBoxLayout = QVBoxLayout()
        self.row_dropdown: QHBoxLayout = QHBoxLayout()
        self.row_line_edit: QHBoxLayout = QHBoxLayout()

        self.label: QLabel = QLabel("Create Operation")
        self.dropdown_label: QLabel = QLabel("Operation:")
        self.dropdown_menu: QComboBox = QComboBox(self)

        self.operation_description_label: QLabel = QLabel("Description:")

        self.line_edit_label: QLabel = QLabel("Result Name:")
        self.line_edit: QLineEdit = QLineEdit(self)

        self.build()
        self.setup_ui()

    def build(self):
        self.dropdown_menu.currentIndexChanged.connect(self.update_interface)
        self.dropdown_menu.addItems(self.operation_manager.available_functions.keys())

    def setup_ui(self):
        self.setWindowTitle("Create Operation")

        self.label.setFont(QFont('Arial', 14))
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.label)

        self.layout.addLayout(self.row_dropdown)
        self.layout.addWidget(self.operation_description_label)
        self.layout.addLayout(self.row_line_edit)

        self.dropdown_label.setFont(QFont('Arial', 11))
        self.dropdown_menu.setFont(QFont('Arial', 11))
        self.row_dropdown.addWidget(self.dropdown_label)
        self.row_dropdown.addWidget(self.dropdown_menu)

        self.line_edit_label.setFont(QFont('Arial', 11))
        self.line_edit.setFont(QFont('Arial', 11))
        self.row_line_edit.addWidget(self.line_edit_label)
        self.row_line_edit.addWidget(self.line_edit)

        self.setLayout(self.layout)

    def update_interface(self, index):
        operation_name = self.dropdown_menu.currentText()
        if operation_name in self.operation_manager.available_functions:
            operation_description = self.operation_manager.available_functions[operation_name]
            self.operation_description_label.setText(operation_description.__doc__)

    def showEvent(self, event):
        super().showEvent(event)
        self.run_on_show()

    def run_on_show(self):
        self.line_edit.setText("")
