# -*- coding: utf-8 -*-
"""
Created on May 2024

@author: Ghimciuc Ioan
"""

from config import load_config, setup_logging


def main():
    # Setup logging
    setup_logging()

    # Load configuration
    config = load_config()


if __name__ == '__main__':
    main()
