# -*- coding: utf-8 -*-
"""
Created on June 2024

@author: Ghimciuc Mihail
"""
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, \
    QAbstractItemView, QMessageBox, QDialog
import logging
import gui.windows.CreateOperationDialog as Dialogs


class DataProcessing(QWidget):
    def __init__(self, main_window: QMainWindow, logger: logging.Logger, previous_widget: callable,
                 next_widget: callable, parent=None):
        super().__init__(parent)  # Initialize QWidget
        self.logger: logging.Logger = logger
        self.main_window: QMainWindow = main_window
        self.previous_widget: callable = previous_widget
        self.next_widget: callable = next_widget
        self.subject_name: str = ""

        self.layout: QVBoxLayout = QVBoxLayout()
        self.label: QLabel = QLabel("Data Processing")
        self.column_layout: QHBoxLayout = QHBoxLayout()

        self.column_1_layout: QVBoxLayout = QVBoxLayout()
        self.column_1_label: QLabel = QLabel("Variables")
        self.variables_list: QListWidget = QListWidget()

        self.column_2_layout: QVBoxLayout = QVBoxLayout()
        self.right_row_layout: QHBoxLayout = QHBoxLayout()
        self.column_2_label: QLabel = QLabel("Operations")
        self.right_button: QPushButton = QPushButton("+")
        self.operations_list: QListWidget = QListWidget()

        self.right_create_operation: QDialog = Dialogs.CreateOperationDialog(self, self.logger)

        self.button_next: QPushButton = QPushButton("Next", self)

        self.build()

    def build(self):
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
                        margin: 10px 50px 10px 50px ;   /* Margin around the button */
                        padding: 10px;  /* Padding inside the button */
                    }
                """)
        self.variables_list.addItems(["leg", "arm", "torso", "head"])
        self.column_1_layout.addWidget(self.variables_list)

        self.column_2_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.column_2_label.setFont(QFont('Arial', 11))
        self.right_row_layout.addWidget(self.column_2_label)
        self.right_button.setFont(QFont('Arial', 20))
        self.right_button.setStyleSheet("""
                            QPushButton {
                                margin: 0px 50px 0px 100px ;   /* Margin around the button */
                                padding: 2px;  /* Padding inside the button */
                            }
                        """)
        self.right_button.clicked.connect(self.show_dialog)     # TODO: Add function
        self.right_row_layout.addWidget(self.right_button)
        self.column_2_layout.addLayout(self.right_row_layout)

        self.operations_list.setFont(QFont('Arial', 12))
        self.operations_list.setStyleSheet("""
                    QListWidget {
                        margin: 10px 50px 10px 50px ;   /* Margin around the button */
                        padding: 10px;  /* Padding inside the button */
                    }
                """)
        self.operations_list.addItems(["fix", "change", "heal", "repair"])
        self.column_2_layout.addWidget(self.operations_list)

        self.column_layout.addLayout(self.column_1_layout)
        self.column_layout.addLayout(self.column_2_layout)
        self.layout.addLayout(self.column_layout)

        self.button_next.setFont(QFont('Arial', 11))
        self.button_next.setStyleSheet("""
                    QPushButton {
                        margin: 10px 100px 10px 500px ;   /* Margin around the button */
                        padding: 10px;  /* Padding inside the button */
                    }
                """)
        self.button_next.clicked.connect(self.next_widget)
        self.layout.addWidget(self.button_next)

        self.setLayout(self.layout)

    def show_dialog(self):
        self.right_create_operation.show()

    def update_subject(self, subject_name: str):
        self.label.setText(f"{subject_name}: Data Processing")
        self.subject_name = subject_name