# -*- coding: utf-8 -*-
"""
Created on May 2024

@author: Ghimciuc Ioan
"""

import logging
import sys

from PySide6.QtWidgets import QApplication

from config import load_config, setup_logging
from gui.windows.MainWindow import MainWindow
from calculations.vicon_nexus import ViconNexusAPI, Marker


def main():
    setup_logging()
    config = load_config()

    logger = logging.getLogger('my_app')
    logger.info("Application started")

    nexus_api = ViconNexusAPI()
    subject_names: list[str] = nexus_api.GetSubjectNames()
    markers: dict[str, Marker] = nexus_api.GetMarkers(subject_names[0])

    app = QApplication(sys.argv)

    main_window = MainWindow(logger, config)
    main_window.show()

    code: int = app.exec()
    logger.info(f"Application stopped with code '{code}'")
    sys.exit(code)


if __name__ == '__main__':
    main()
