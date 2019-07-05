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



"""
    Logging setup
"""
# Output files for the different type of logs
LOG_DEBUG = "logs_debug.txt"
LOG_WARNING = "logs_warning.txt"
LOG_CRITICAL = "logs_critical.txt"
LOG_ALL = "logs_all.txt"

# Loggers name to use
LOGGER_ORM = "Orm"
LOGGER_HL7 = "HL7"
LOGGER_ALL = "all"

# The current logging type for the app
LOG_TYPE = logging.DEBUG

def _init_logger(self, logger=LOGGER_ALL, filehandler=LOG_ALL, level_type=logging.debug):
        try:
            logger = logging.getLogger(logger)
            if(filehandler):
                handler = logging.FileHandler(filehandler)

            handler.setLevel(level_type)
            logger.addHandler(handler)
            if(level_type == (logging.debug or logging.critical)):
                logger.format("%(name)s - %(module)s - %(funcName)s - %(levelname)s - %(lineno)s - %(asctime)s - %(message)s")
            else:
                logger.format("%(name)s - %(funcName)s - %(asctime)s - %(message)s")

            return logger
        except Exception as e:
            with open("CRITICAL.txt", "a") as f:
                f.writelines("Critical error happened, logger can't be initialised")
                f.writelines("Error : ", str(e))
