# -*- coding: utf-8 -*-
"""
Created on June 2024

@author: Ghimciuc Mihail
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton
import logging


class DataExport(QWidget):
    def __init__(self, main_window: QMainWindow, logger: logging.Logger, previous_widget: callable,
                 next_widget: callable, parent=None):
        super().__init__(parent)  # Initialize QWidget
        self.logger: logging.Logger = logger
        self.main_window: QMainWindow = main_window
        self.previous_widget: callable = previous_widget
        self.next_widget: callable = next_widget
        self.subject_name: str = ""

        self.layout: QVBoxLayout = QVBoxLayout()
        self.label: QLabel = QLabel("Data Exporting")
        self.export_list: QListWidget = QListWidget()
        self.button_next: QPushButton = QPushButton("Export", self)

        self.build()

    def build(self):
        self.label.setFont(QFont('Arial', 16))
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.label)
        self.export_list.setFont(QFont('Arial', 12))
        self.export_list.addItems(["PDF", "EXCEL", "CSV"])
        self.export_list.setStyleSheet("""
                            QListWidget {
                                margin: 10px 100px 10px 100px ;   /* Margin around the button */
                                padding: 10px;  /* Padding inside the button */
                            }
                        """)
        self.layout.addWidget(self.export_list)
        self.button_next.setFont(QFont('Arial', 11))
        self.button_next.setStyleSheet("""
                            QPushButton {
                                margin: 10px 250px 10px 250px ;   /* Margin around the button */
                                padding: 10px;  /* Padding inside the button */
                            }
                        """)
        self.button_next.clicked.connect(self.next_widget)
        self.layout.addWidget(self.button_next)
        self.setLayout(self.layout)

    def update_subject(self, subject_name: str):
        self.label.setText(f"{subject_name}: Data Export")
        self.subject_name = subject_name
