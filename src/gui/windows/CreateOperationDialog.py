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
from calculations.operation import OperationManager, Operation
from calculations.vicon_nexus import ViconNexusAPI, Marker
import logging
import inspect


class CreateOperationDialog(QDialog):
    operation_added = Signal()

    def __init__(self, parent_widget: QWidget, logger: logging.Logger, operation_manager: OperationManager, parent=None):
        self.logger: logging.Logger = logger
        self.logger.info("Initializing CreateOperation Dialog")
        self.operation_manager: OperationManager = operation_manager
        self.markers: dict[str, Marker] = {}
        self.operation_function: FunctionType

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
        self.line_edit_result_name: QLineEdit = QLineEdit(self)

        self.layout_button_add: QHBoxLayout = QHBoxLayout()
        self.button_add_operation: QPushButton = QPushButton("Add")
        self.button_add_run_operation: QPushButton = QPushButton("Add and Run")

        self.build()
        self.setup_ui()

    def build(self):
        self.dropdown_menu.currentIndexChanged.connect(self.update_interface)
        self.dropdown_menu.addItems(self.operation_manager.available_functions.keys())
        self.button_add_operation.clicked.connect(self.add_operation)
        self.button_add_run_operation.clicked.connect(self.add_run_operation)

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
        self.line_edit_result_name.setFont(QFont('Arial', 11))
        self.row_line_edit.addWidget(self.result_name_label)
        self.row_line_edit.addWidget(self.line_edit_result_name)

        self.layout_button_add.addWidget(self.button_add_operation)
        self.layout_button_add.addWidget(self.button_add_run_operation)
        self.layout.addLayout(self.layout_button_add)

        self.setLayout(self.layout)

    def update_interface(self):
        operation_name = self.dropdown_menu.currentText()
        if operation_name in self.operation_manager.available_functions:
            operation_description = self.operation_manager.available_functions[operation_name]
            self.operation_description_label.setText(operation_description.__doc__)
            self.update_dynamic_layout()
            self.adjustSize()

    def remove_last_hbox(self):
        while self.dynamic_layout.count():
            item = self.dynamic_layout.itemAt(self.dynamic_layout.count() - 1)

            if item.layout():
                layout = item.layout()

                while layout.count():
                    widget_item = layout.itemAt(0)
                    widget = widget_item.widget()
                    if widget:
                        layout.removeWidget(widget)
                        widget.deleteLater()
                    else:
                        sub_layout = widget_item.layout()
                        self._clear_layout(sub_layout)
                        layout.removeItem(widget_item)

                # Remove the layout itself
                self.dynamic_layout.removeItem(layout)
                del layout

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.itemAt(0)
            widget = item.widget()
            if widget:
                layout.removeWidget(widget)
                widget.deleteLater()
            else:
                sub_layout = item.layout()
                self._clear_layout(sub_layout)
                layout.removeItem(item)

    def update_dynamic_layout(self):
        self.parameter_dropdowns.clear()
        self.remove_last_hbox()

        self.operation_function = self.operation_manager.available_functions[self.dropdown_menu.currentText()]
        params = inspect.getfullargspec(self.operation_function).args

        for param in params:
            row_layout: QHBoxLayout = QHBoxLayout()
            label: QLabel = QLabel(f"{param}:")
            dropdown: QComboBox = QComboBox()
            dropdown.addItems(self.markers)
            row_layout.addWidget(label)
            row_layout.addWidget(dropdown)
            self.parameter_dropdowns.append(dropdown)
            self.dynamic_layout.addLayout(row_layout)

    def create_operation(self) -> Operation | None:
        result_name: str = self.line_edit_result_name.text()
        params: list[str] = [x.currentText() for x in self.parameter_dropdowns]
        if result_name != "":
            operation: Operation = Operation(self.operation_function, result_name, params)
            return operation
        return None

    def add_operation(self):
        operation: Operation = self.create_operation()
        if operation:
            self.operation_manager.add_operation(operation)
            self.on_operation_added()
            self.close()

    def add_run_operation(self):
        operation: Operation = self.create_operation()
        if operation:
            self.operation_manager.add_and_run_operation(operation)
            self.on_operation_added()
            self.close()

    def showEvent(self, event):
        super().showEvent(event)
        self.run_on_show()

    def run_on_show(self):
        self.update_interface()
        self.line_edit_result_name.setText("")

    @Slot()
    def on_operation_added(self):
        self.operation_added.emit()

    @Slot('QVariant')
    def update_markers(self, markers: dict[str, Marker]):
        self.markers = markers
