import logging
import logging.config

import yaml


def load_config(filepath='../config/main_config.yaml'):
    with open(filepath, 'r') as file:
        config = yaml.safe_load(file)
    return config

def setup_logging(default_path='../config/logging_config.yaml', default_level=logging.INFO):
    with open(default_path, 'r') as file:
        config = yaml.safe_load(file)
    logging.config.dictConfig(config)
