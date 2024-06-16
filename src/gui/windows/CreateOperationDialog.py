# -*- coding: utf-8 -*-
"""
Created on June 2024

@author: Ghimciuc Mihail
"""
from logging import Logger

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMainWindow, QWidget, QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton, QComboBox, \
    QTextEdit, QLineEdit, QHBoxLayout, QSpacerItem, QSizePolicy
from calculations.operation import OperationManager
from calculations.vicon_nexus import ViconNexusAPI, Marker
import logging
import inspect


class CreateOperationDialog(QDialog):
    def __init__(self, parent_widget: QWidget, logger: logging.Logger, operation_manager: OperationManager, parent=None):
        self.logger: logging.Logger = logger
        self.logger.info("Initializing CreateOperation Dialog")
        self.operation_manager: OperationManager = operation_manager
        self.markers: dict[str, Marker] = {}

        super().__init__(parent)  # Initialize QDialog

        self.parent_widget: QWidget = parent_widget

        self.layout: QVBoxLayout = QVBoxLayout()
        self.row_dropdown: QHBoxLayout = QHBoxLayout()
        self.row_line_edit: QHBoxLayout = QHBoxLayout()

        self.label: QLabel = QLabel("Create Operation")
        self.dropdown_label: QLabel = QLabel("Operation:")
        self.dropdown_menu: QComboBox = QComboBox(self)

        self.operation_description_label: QLabel = QLabel("Description:")

        self.dynamic_layout: QVBoxLayout = QVBoxLayout()
        self.parameter_dropdowns: list[QComboBox] = []

        self.result_name_label: QLabel = QLabel("Result Name:")
        self.line_edit: QLineEdit = QLineEdit(self)

        self.add_operation_button: QPushButton = QPushButton("Add")

        self.build()
        self.setup_ui()

    def build(self):
        self.dropdown_menu.currentIndexChanged.connect(self.update_interface)
        self.dropdown_menu.addItems(self.operation_manager.available_functions.keys())
        self.add_operation_button.clicked.connect(self.add_operation)

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

        self.layout.addLayout(self.dynamic_layout)

        self.result_name_label.setFont(QFont('Arial', 11))
        self.line_edit.setFont(QFont('Arial', 11))
        self.row_line_edit.addWidget(self.result_name_label)
        self.row_line_edit.addWidget(self.line_edit)

        self.layout.addWidget(self.add_operation_button)

        self.setLayout(self.layout)

    def update_interface(self):
        operation_name = self.dropdown_menu.currentText()
        if operation_name in self.operation_manager.available_functions:
            operation_description = self.operation_manager.available_functions[operation_name]
            self.operation_description_label.setText(operation_description.__doc__)
            self.update_dynamic_layout()

    def update_dynamic_layout(self):
        self.parameter_dropdowns.clear()
        for i in reversed(range(self.dynamic_layout.count())):
            widget_to_remove = self.dynamic_layout.itemAt(i).widget()
            self.dynamic_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        func: FunctionType = self.operation_manager.available_functions[self.dropdown_menu.currentText()]
        params = inspect.getfullargspec(func).args

        for param in params:
            dropdown: QComboBox = QComboBox()
            dropdown.addItems(self.markers)
            self.parameter_dropdowns.append(dropdown)
            self.dynamic_layout.addWidget(dropdown)

    def add_operation(self):
        pass

    def showEvent(self, event):
        super().showEvent(event)
        self.run_on_show()

    def run_on_show(self):
        self.update_interface()
        self.line_edit.setText("")

    @Slot('QVariant')
    def update_markers(self, markers: dict[str, Marker]):
        self.markers = markers
