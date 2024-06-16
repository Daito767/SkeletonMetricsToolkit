# -*- coding: utf-8 -*-
"""
Created on June 2024

@author: Ghimciuc Mihail
"""
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton
import logging


class SubjectSelection(QWidget):
    def __init__(self, main_window: QMainWindow, logger: logging.Logger, next_widget: callable, parent=None):
        super().__init__(parent)  # Initialize QWidget
        self.logger: logging.Logger = logger
        self.main_window: QMainWindow = main_window
        self.next_widget: function = next_widget
        self.subject_name: str = "N/A"
        self.update_callbacks: list[callable] = []

        self.layout: QVBoxLayout = QVBoxLayout()
        self.label: QLabel = QLabel("Select Subject")
        self.subjects_list: QListWidget = QListWidget()
        self.button_next: QPushButton = QPushButton("Select subject", self)

        self.build()

    def build(self):
        self.label.setFont(QFont('Arial', 16))
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.subjects_list.setFont(QFont('Arial', 12))
        self.subjects_list.setStyleSheet("""
                    QListWidget {
                        margin: 10px 50px 10px 50px ;   /* Margin around the button */
                        padding: 10px;  /* Padding inside the button */
                    }
                """)
        self.subjects_list.addItems(["Vasiliy Anatolyevich", "Alexei Shapochnik", "Dimitrii Strelybov"])

        self.button_next.setFont(QFont('Arial', 11))
        self.button_next.setStyleSheet("""
                    QPushButton {
                        margin: 10px 250px 10px 250px ;   /* Margin around the button */
                        padding: 10px;  /* Padding inside the button */
                    }
                """)
        self.button_next.clicked.connect(self.select_subject)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.subjects_list)
        self.layout.addWidget(self.button_next)
        self.setLayout(self.layout)

    def select_subject(self):
        if len(self.subjects_list.selectedItems()) > 0:
            self.subject_name = self.subjects_list.selectedItems()[0].text()
            self.call_update_callbacks()
            self.main_window.statusBar().showMessage(f'Subject: {self.subject_name}', 3000)
            self.next_widget()
        else:
            self.main_window.statusBar().showMessage('Select a subject!', 3000)

    def connect_update_callbacks(self, callback: list[callable]):
        self.update_callbacks.extend(callback)

    def call_update_callbacks(self):
        for callback in self.update_callbacks:
            callback(self.subject_name)
