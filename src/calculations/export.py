# -*- coding: utf-8 -*-
"""
Created on May 2024

@author: Ghimciuc Ioan
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import logging


class ExportManager:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.logger.info("Initializing ExportManager")

    def export_excel(self, storage: dict[str, any], data_to_export: list[str], file_path: str):
        try:
            # Filtrare date pentru variabilele specificate
            filtered_storage = {key: storage[key] for key in data_to_export if key in storage}

            # Transformarea datelor într-un format corespunzător pentru Excel
            for key, value in filtered_storage.items():
                if isinstance(value, (list, np.ndarray)) and all(isinstance(i, list) for i in value):
                    # Dacă este o listă de liste, transformăm fiecare listă într-un șir de caractere
                    filtered_storage[key] = [', '.join(map(str, sublist)) for sublist in value]

            df = pd.DataFrame(filtered_storage)
            df.to_excel(file_path, index=False)
            self.logger.info(f"Data exported to {file_path} successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to export data to Excel: {e}")
            return False

    def export_plot(self, storage: dict[str, any], data_to_export: list[str], file_path: str) -> bool:
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
            return True
        except Exception as e:
            self.logger.error(f"Failed to save PDF: {e}")
            return False


if __name__ == "__main__":
    # Utilizare
    logger = logging.getLogger()
    export_manager = ExportManager(logger)

    storage = {
        'variable1': [1, 2, 3, 4, 5],
        'variable2': [2, 3, 4, 5, 6]
    }
    variable_names = ['variable1', 'variable2']

    export_manager.export_excel(storage, variable_names, 'data.xlsx')
    export_manager.export_plot(storage, variable_names, 'plots.pdf')
