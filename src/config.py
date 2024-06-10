import logging
import logging.config
import os

import yaml


def load_config(filepath: str = '../config/main_config.yaml') -> dict:
    with open(filepath, 'r') as file:
        config = yaml.safe_load(file)
    return config


def create_log_folder(log_folder: str):
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)


def setup_logging(default_path: str = '../config/logging_config.yaml', default_level: int = logging.INFO):
    with open(default_path, 'r') as file:
        config = yaml.safe_load(file)

    # Extract the log folder path from the config
    log_folder: str = ''
    for handler in config.get('handlers', {}).values():
        if 'filename' in handler:
            log_folder = os.path.dirname(handler['filename'])
            break

    if not os.path.exists(log_folder):
        create_log_folder(log_folder)

    logging.config.dictConfig(config)
