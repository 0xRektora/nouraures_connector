"""
Simple configuration file for debugging and saving constants
"""
import logging, sys, os

"""
    Date and time format
"""
DT_FORMAT = "%Y%m%d%H%M%S"

"""
    Full actual path
"""
FULL_PATH = os.getcwd()

"""
    Static files data folder
"""

STATIC_MEDECIN = "/service/data/medecins.csv"
STATIC_TYPE_INTERVENTION = "/service/data/types_intervention.csv"


"""
    orm.py

    Database infos
"""
DB_ADRESS = "localhost"
DB_NAME ="nouraures"
DB_USER = "root"
DB_PASSWORD = ""

"""
    server.py

    Server infos
"""

SERVER_IP = "localhost"
SERVER_PORT = 8888

"""
    Logging setup
"""
# Output files for the different type of logs
LOG_INFO = "logs_info.txt"
LOG_DEBUG = "logs_debug.txt"
LOG_WARNING = "logs_warning.txt"
LOG_CRITICAL = "logs_critical.txt"
LOG_ALL = "logs_all.txt"

# Loggers name to use
LOGGER_ORM = "Orm"
LOGGER_HL7 = "HL7"
LOGGER_UTILS = "Utils"
LOGGER_SERVER = "Server"
LOGGER_ALL = "all"

# The current logging type for the app
LOG_TYPE = logging.DEBUG

def _init_logger(logger=LOGGER_ALL, filehandler=LOG_ALL, level_type=LOG_TYPE):
        try:
            # Init variables
            logger = logging.getLogger(logger)
            logger.propagate = False # remove stdout
            handler = None
            formatter = None

            # Check to redirect to a file or sys.stdout
            if filehandler:
                handler = logging.FileHandler(filehandler)
            elif filehandler == None:
                handler = logging.StreamHandler(sys.stdout)
            else :
                handler = logging.FileHandler(LOG_ALL)

            # Check the logging type to set a formatter
            if level_type == logging.DEBUG or level_type >= logging.WARNING:
                formatter = logging.Formatter("%(name)s - %(funcName)s - %(levelname)s - %(lineno)s - %(asctime)s - %(message)s")
            else:
                formatter = logging.Formatter("%(name)s - %(funcName)s - %(asctime)s - %(message)s")

            # Set the handler and bind it to the logger
            handler.setFormatter(formatter)
            logger.setLevel(level_type)
            logger.addHandler(handler)

            return logger
        except Exception as e:
            with open("CRITICAL.txt", "a") as f:
                f.writelines("Critical error happened, logger can't be initialised\n")
                f.writelines("Error : " + str(e) + "\n")
