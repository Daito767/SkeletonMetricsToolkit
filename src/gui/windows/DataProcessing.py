# -*- coding: utf-8 -*-
"""
Created on June 2024

@author: Ghimciuc Mihail
"""
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, \
    QAbstractItemView, QMessageBox, QDialog, QFileDialog
import logging
import gui.windows.CreateOperationDialog as Dialogs
from calculations.export import ExportManager
from calculations.operation import OperationManager
from calculations.vicon_nexus import ViconNexusAPI, Marker


class DataProcessing(QWidget):
    markers_changed = Signal('QVariant')

    def __init__(self, main_window: QMainWindow, logger: logging.Logger, previous_widget: callable,
                 next_widget: callable, nexus_api: ViconNexusAPI, operation_manager: OperationManager, parent=None):
        self.logger: logging.Logger = logger
        self.logger.info("Initializing DataProcessing")

        super().__init__(parent)  # Initialize QWidget

        self.main_window: QMainWindow = main_window
        self.previous_widget: callable = previous_widget
        self.next_widget: callable = next_widget
        self.subject_name: str = ""

        self.start_frame, self.end_frame = 0, 0
        self.markers: dict[str, Marker] = {}

        self.nexus_api: ViconNexusAPI = nexus_api
        self.operation_manager: OperationManager = operation_manager
        self.export_manager: ExportManager = ExportManager(self.logger)

        self.layout: QVBoxLayout = QVBoxLayout()
        self.label: QLabel = QLabel("Data Processing")
        self.column_layout: QHBoxLayout = QHBoxLayout()

        self.column_1_layout: QVBoxLayout = QVBoxLayout()
        self.column_1_label: QLabel = QLabel("Variables")
        self.variables_list: QListWidget = QListWidget()

        self.column_2_layout: QVBoxLayout = QVBoxLayout()
        self.right_row_layout: QHBoxLayout = QHBoxLayout()
        self.column_2_label: QLabel = QLabel("Operations")
        self.button_add_operation: QPushButton = QPushButton("+")
        self.operations_list: QListWidget = QListWidget()

        self.dialog_create_operation = Dialogs.CreateOperationDialog(self, self.logger, self.operation_manager)

        self.button_export_excel: QPushButton = QPushButton("Export to Excel", self)
        self.button_export_plot: QPushButton = QPushButton("Export to PLOT", self)

        self.build()
        self.setup_ui()

    def build(self):
        self.button_add_operation.clicked.connect(self.show_dialog)

        self.markers_changed.connect(self.dialog_create_operation.update_markers)
        self.dialog_create_operation.operation_added.connect(self.refresh_list_elements)

        self.button_export_excel.clicked.connect(self.export_to_excel)
        self.button_export_plot.clicked.connect(self.export_to_plot)

        self.update_variables()
        self.update_operations()

    def setup_ui(self):
        self.label.setFont(QFont('Arial', 16))
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.label)

        self.column_1_label.setFont(QFont('Arial', 11))
        self.column_1_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.column_1_layout.addWidget(self.column_1_label)

        self.variables_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.variables_list.setFont(QFont('Arial', 12))
        self.variables_list.setStyleSheet("""
                    QListWidget {
                        margin: 10px 20px 10px 20px ;   /* Margin around the button */
                        padding: 10px;  /* Padding inside the button */
                    }
                """)
        self.column_1_layout.addWidget(self.variables_list)

        self.column_2_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.column_2_label.setFont(QFont('Arial', 11))
        self.right_row_layout.addWidget(self.column_2_label)
        self.button_add_operation.setFont(QFont('Arial', 20))
        self.button_add_operation.setStyleSheet("""
                            QPushButton {
                                margin: 0px 50px 0px 100px ;   /* Margin around the button */
                                padding: 2px;  /* Padding inside the button */
                            }
                        """)
        self.right_row_layout.addWidget(self.button_add_operation)
        self.column_2_layout.addLayout(self.right_row_layout)

        self.operations_list.setFont(QFont('Arial', 12))
        self.operations_list.setStyleSheet("""
                    QListWidget {
                        margin: 10px 20px 10px 20px ;   /* Margin around the button */
                        padding: 10px;  /* Padding inside the button */
                    }
                """)
        self.column_2_layout.addWidget(self.operations_list)

        self.column_layout.addLayout(self.column_1_layout)
        self.column_layout.addLayout(self.column_2_layout)
        self.layout.addLayout(self.column_layout)

        self.button_export_excel.setFont(QFont('Arial', 11))
        self.button_export_excel.setStyleSheet("""
                    QPushButton {
                        margin: 0px 50px 0px 50px ;   /* Margin around the button */
                        padding: 5px;  /* Padding inside the button */
                    }
                """)
        self.button_export_plot.setFont(QFont('Arial', 11))
        self.button_export_plot.setStyleSheet("""
                    QPushButton {
                        margin: 0px 50px 0px 50px ;   /* Margin around the button */
                        padding: 5px;  /* Padding inside the button */
                    }
                """)
        self.column_1_layout.addWidget(self.button_export_excel)
        self.column_1_layout.addWidget(self.button_export_plot)
        self.setLayout(self.layout)

    def show_dialog(self):
        self.dialog_create_operation.show()

    def update_variables(self):
        self.variables_list.clear()
        for value in self.operation_manager.storage.keys():
            self.variables_list.addItem(value)

    def update_operations(self):
        for operation in self.operation_manager._operations:
            self.operations_list.addItem(str(operation))

    def get_markers(self) -> dict[str, Marker]:
        return self.markers

    def export_to_excel(self):
        variables: list[str] = [item.text() for item in self.variables_list.selectedItems()]
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;Text Files (*.excel)")
        if file_path:
            result = self.export_manager.export_excel(self.operation_manager.storage, variables, file_path)
            self.export_operation_result(result)

    def export_to_plot(self):
        variables: list[str] = [item.text() for item in self.variables_list.selectedItems()]
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;Text Files (*.excel)")
        if file_path:
            result = self.export_manager.export_plot(self.operation_manager.storage, variables, file_path)
            self.export_operation_result(result)

    def export_operation_result(self, result):
        if result:
            self.main_window.statusBar().showMessage("Exported Successfully!", 3000)
        else:
            self.main_window.statusBar().showMessage("Exported Failed!", 3000)

    @Slot()
    def refresh_list_elements(self):
        self.variables_list.clear()
        self.operations_list.clear()
        self.update_variables()
        self.update_operations()

    @Slot('QVariant')
    def on_markers_changed(self):
        self.markers_changed.emit(self.markers)

    @Slot(str)
    def update_subject(self, subject_name: str):
        self.label.setText(f"{subject_name}: Data Processing")
        self.subject_name = subject_name

        start_frame, end_frame = self.nexus_api.GetTrialRegionOfInterest()
        self.markers: dict[str, Marker] = self.nexus_api.GetMarkers(self.subject_name)

        for marker in self.markers.values():
            self.operation_manager.storage[marker.name] = marker.trajectory

        self.update_variables()
        self.on_markers_changed()
        self.update_variables()
