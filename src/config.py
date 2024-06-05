import yaml


def load_config(filepath='config/settings.yaml'):
    with open(filepath, 'r') as file:
        config = yaml.safe_load(file)
    return config
