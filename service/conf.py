"""
Simple configuration file for debugging and saving constants
"""
import logging, sys


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