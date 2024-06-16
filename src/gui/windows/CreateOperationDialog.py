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
import logging


class CreateOperationDialog(QDialog):
    def __init__(self, parent_widget: QWidget, logger: logging.Logger, parent=None):
        self.logger: logging.Logger = logger
        self.logger.info("Initializing CreateOperation Dialog")

        super().__init__(parent)  # Initialize QDialog

        self.parent_widget: QWidget = parent_widget

        self.layout: QVBoxLayout = QVBoxLayout()
        self.row_dropdown: QHBoxLayout = QHBoxLayout()
        self.row_line_edit: QHBoxLayout = QHBoxLayout()

        self.label: QLabel = QLabel("Create Operation")
        self.dropdown_label: QLabel = QLabel("Operation:")
        self.dropdown_menu: QComboBox = QComboBox(self)
        self.line_edit_label: QLabel = QLabel("Operation Name:")
        self.line_edit: QLineEdit = QLineEdit(self)

        self.build()

    def build(self):
        self.setWindowTitle("Create Operation")

        self.label.setFont(QFont('Arial', 14))
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.label)

        self.layout.addLayout(self.row_dropdown)
        self.layout.addLayout(self.row_line_edit)

        self.dropdown_label.setFont(QFont('Arial', 11))
        self.dropdown_menu.setFont(QFont('Arial', 11))
        self.dropdown_menu.addItems(["Create Operation", "Delete Operation"])
        self.row_dropdown.addWidget(self.dropdown_label)
        self.row_dropdown.addWidget(self.dropdown_menu)

        self.line_edit_label.setFont(QFont('Arial', 11))
        self.line_edit.setFont(QFont('Arial', 11))
        self.row_line_edit.addWidget(self.line_edit_label)
        self.row_line_edit.addWidget(self.line_edit)

        self.setLayout(self.layout)

