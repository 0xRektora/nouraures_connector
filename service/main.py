import conf
import utils
import logging
import datetime
import time
from orm import Orm
from hl7 import Hlseven
import sys
import pickle
import server
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

"""
    Main entrypoint of the NourAures Connector
"""
TIME = time.time()  # Contain the time at the start of the program

logger = conf._init_logger(filehandler=conf.LOG_ALL)
logger = logging.getLogger(conf.LOGGER_ALL)
logger.propagate = False  # disable stdout


EXAMENS_ID = 10925  # TODO REMOVE
if len(sys.argv) > 1:
    try:
        EXAMENS_ID = sys.argv[1]
        conf.STATIC_MEDECIN = "/data/medecins.csv"
        conf.STATIC_TYPE_INTERVENTION = "/data/types_intervention.csv"
        with open("php_call.txt", "a") as f:
            f.writelines(
                f"System called at {datetime.datetime.now().strftime('%Y/%m/%d')} : argv : {sys.argv}\n")
    except:
        logger.critical(
            f"[+] Can't find the EXAMEN_ID in the arguments passed : {sys.argv} [+]")

try:
    # Read the CSV files
    EVOLUCARE_MEDECIN = utils.getFile(conf.STATIC_MEDECIN)
    EVOLUCARE_TYPES_INTERVENTION = utils.getFile(conf.STATIC_TYPE_INTERVENTION)
except Exception as e:
    logger.critical(
        "[-] Cannot init EVOLUCARE_MEDECIN and EVOLUCARE_TYPES_INTERVENTION [-]")
    logger.critical(f"[-] ERROR : {e} [-]")


EXAMEN_ROW = None  # Will contain the examen row
PATIENT_ROW = None  # Will contain the patient row
# Will contain the medeincs rows (intervenant + prescripteur)
MEDECIN_ROWS = None
# Will contain the medeincs rows (intervenant + prescripteur)
TYPES_INTERVENTION_ROW = None

ORM_MSG = None  # Will contain the orm message in STR

try:
    orm = Orm()
    hlseven = Hlseven()
except Exception as e:
    logger.critical("[-] Cannot init orm and hlseven [-]")
    logger.critical(f"[-] ERROR : {e} [-]")


data = orm.get_examen(EXAMENS_ID)
if(data):
    EXAMEN_ROW = list(data)[0]
    logger.debug(f"[+] EXAMEN_ROW {EXAMEN_ROW} [+]")

data = orm.get_patient(EXAMENS_ID)
if(data):
    PATIENT_ROW = list(data)[0]
    logger.debug(f"[+] PATIENT_ROW {PATIENT_ROW} [+]")

data = orm.get_types_intervention(EXAMENS_ID)
if(data):
    TYPES_INTERVENTION_ROW = list(data)[0]
    logger.debug(f"[+] TYPES_INTERVENTION_ROW {TYPES_INTERVENTION_ROW} [+]")

# Check if the type intervention is in type_intervention csv
if list(filter(lambda x: str(x[0]) == str(TYPES_INTERVENTION_ROW[0]), EVOLUCARE_TYPES_INTERVENTION)):
    logger.info(f"[+] {TYPES_INTERVENTION_ROW[0]} found, continuing operations. [+]")
else:
    logger.info(f"[+] {TYPES_INTERVENTION_ROW[0]} not resolved into {conf.STATIC_TYPE_INTERVENTION} [+]")

data = orm.get_medecin(EXAMENS_ID)
if(data):
    MEDECIN_ROWS = (list(data[0]), list(data[1]))
    logger.debug(f"[+] MEDECIN_ROWS {MEDECIN_ROWS} [+]")


# We map the RPPS of the current medecin_interv
RPPS = 0
logger.info(f"[+] Getting the RPPS [+]")
try:
    if MEDECIN_ROWS is not None and MEDECIN_ROWS[0]:
        logger.debug(f"[+] MEDECIN_ROW {MEDECIN_ROWS[0]} [+]")
        for row in EVOLUCARE_MEDECIN:
            logger.debug(f"[+] {row} [+]")
            if row[1] == MEDECIN_ROWS[0][1] and row[2] == MEDECIN_ROWS[0][2]:
                logger.debug(f"[+] {row[3]} [+]")
                RPPS = row[3]
                logger.debug(f"[+] {RPPS} [+]")
    logger.debug(f"[+] RPPS {RPPS} [+]")
except Exception as e:
    logger.critical(e)

# We map the RPPS of the current medecin_presc, if it does't exist put the RPPS
CODE_PRESC = 0
logger.info(f"[+] Getting the CODE_PRESC [+]")
try:
    if MEDECIN_ROWS is not None and MEDECIN_ROWS[1]:
        for row in EVOLUCARE_MEDECIN:
            if row[1] == MEDECIN_ROWS[1][1] and row[2] == MEDECIN_ROWS[1][2]:
                CODE_PRESC = row[3]
    else:
        CODE_PRESC = RPPS
    logger.debug(f"[+] CODE_PRESC {CODE_PRESC} [+]")
except Exception as e:
    logger.critical(e)

try:
    logger.info("[+] Executing main thread [+]")
    # TODO remove
    safe = True # testing purposes
    if RPPS or safe:
        # We get the dicom_mod
        dicom_mod = EVOLUCARE_TYPES_INTERVENTION[TYPES_INTERVENTION_ROW[0]][4]
        logger.debug(f"[+] dicom_mod {dicom_mod} [+]")

        logger.info("[+] Constructing the HL7 message [+]")
        # We construct the hlseven class with all the information
        hlseven = utils.constructHl7Orm(hlseven, PATIENT_ROW, EXAMEN_ROW,
                                        MEDECIN_ROWS, TYPES_INTERVENTION_ROW, RPPS, CODE_PRESC, dicom_mod)

        # We assign the var with the hl7 message
        ORM_MSG = hlseven.to_er7()

        logger.debug(str(ORM_MSG).encode("utf8"))

        logger.info("[+] Initializing the server [+]")

        # TODO uncomment
        # # Launching the server
        # orm = Orm()
        # endpoint = TCP4ServerEndpoint(reactor, conf.SERVER_PORT)
        # endpoint.listen(server.HlsevenFactory(hlseven, orm))
        # logger.info(f"[+] Running the server [+]")
        # reactor.run()  # pylint: disable=no-member

        logger.info(f"PROCESS FINISHED IN  {time.time() - TIME} seconds \n\n")
    else:
        logger.critical(
            "[-] Critical error, the medecin intervenent was not found [-]")
        logger.info(f"PROCESS FINISHED IN  {time.time() - TIME} seconds \n\n")
except Exception as e:
    logger.critical(
        "[-] Critical error occured while executing main thread [-]")
    logger.critical(f"[-] ERROR : {e} [-]")
    logger.info(f"PROCESS FINISHED IN  {time.time() - TIME} seconds \n\n")
