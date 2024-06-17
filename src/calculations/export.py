# -*- coding: utf-8 -*-
"""
Created on May 2024

@author: Ghimciuc Ioan
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import logging


class ExportManager:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.logger.info("Initializing ExportManager")

    def export_to_excel(self, storage: dict[str, any], data_to_export: list[str], file_path: str):
        try:
            # Filtrare date pentru variabilele specificate
            filtered_storage = {key: storage[key] for key in data_to_export if key in storage}
            df = pd.DataFrame(filtered_storage)
            df.to_excel(file_path, index=False)
            self.logger.info(f"Data exported to {file_path} successfully.")
        except Exception as e:
            self.logger.error(f"Failed to export data to Excel: {e}")

    def export_plot_variable(self, storage: dict[str, any], data_to_export: list[str], file_path: str):
        try:
            with PdfPages(file_path) as pdf:
                for variable_name in data_to_export:
                    data = storage.get(variable_name)
                    if data is None or not isinstance(data, (list, pd.Series)):
                        self.logger.error(f"Variable '{variable_name}' is not suitable for plotting or does not exist.")
                        continue

                    plt.figure()
                    plt.plot(data)
                    plt.title(f"Plot of {variable_name}")
                    plt.xlabel('Index')
                    plt.ylabel(variable_name)
                    pdf.savefig()
                    plt.close()
                    self.logger.info(f"Plot of '{variable_name}' added to PDF.")
            self.logger.info(f"PDF with plots saved to {file_path} successfully.")
        except Exception as e:
            self.logger.error(f"Failed to save PDF: {e}")


if __name__ == "__main__":
    # Utilizare
    logger = logging.getLogger()
    export_manager = ExportManager(logger)

    storage = {
        'variable1': [1, 2, 3, 4, 5],
        'variable2': [2, 3, 4, 5, 6]
    }
    variable_names = ['variable1', 'variable2']

    export_manager.export_to_excel(storage, variable_names, 'data.xlsx')
    export_manager.export_plot_variable(storage, variable_names, 'plots.pdf')
