"""
Simple configuration file for debugging and saving constants
"""
import logging, sys

"""
    Date and time format
"""

DT_FORMAT = "%Y%m%d%H%M%S"

"""
    orm.py

    Database infos
"""
DB_ADRESS = "localhost"
DB_NAME ="nouraures"
DB_USER = "root"
DB_PASSWORD = ""



def logging_state():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')