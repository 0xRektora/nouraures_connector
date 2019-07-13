import conf
import utils
import logging
import datetime
import time
from orm import Orm
from hl7 import Hlseven
import sys
import pickle
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
                f"System called at {datetime.datetime.now().strftime(conf.DT_FORMAT)} : argv : {sys.argv}\n")
    except:
        logger.critical(
            f"[+] Can't find the EXAMEN_ID in the arguments passed : {sys.argv} [+]")

# Read the CSV files
EVOLUCARE_MEDECIN = utils.getFile(conf.STATIC_MEDECIN)
EVOLUCARE_TYPES_INTERVENTION = utils.getFile(conf.STATIC_TYPE_INTERVENTION)

EXAMEN_ROW = None  # Will contain the examen row
PATIENT_ROW = None  # Will contain the patient row
# Will contain the medeincs rows (intervenant + prescripteur)
MEDECIN_ROWS = None
# Will contain the medeincs rows (intervenant + prescripteur)
TYPES_INTERVENTION_ROW = None

ORM_MSG = None  # Will contain the orm message in STR

orm = Orm()
hlseven = Hlseven()


def constructHl7Orm(hlseven, patient, examen, medecin, type_intervention, RPPS, CODE_PRESC, dicom_mod):
    """
        Function that take in param the orm object for patient and examen
        return a fully constructed hl7 object
    """
    # Construct the PID segment
    # ID_PATIENT^^^LOGICIEL_GAP
    hlseven.pid.pid_3 = str(patient[0]) + "^^^" + "NourauresConnector"
    # NOM_PATIENT^PRENOM_PATIENT
    hlseven.pid.pid_5 = str(patient[2] + "^" + patient[1])
    hlseven.pid.pid_7 = str(patient[4].strftime(
        conf.DT_FORMAT))  # DOB : YYYYMMDD
    # M : MALE / F : FEMALE / O : OTHER / U : UKNOWN
    hlseven.pid.pid_8 = "M" if str(patient[3]).lower() == "homme" else "F"

    # Construct the PV1 segment
    hlseven.pv1.pv1_2 = "O"  # O : OUTPUT
    hlseven.pv1.pv1_3 = "EXTERNE"  # EXTERNE
    # TODO IMPLEMENT
    # CODE_RADIOLOGGUE^^^^^^^^^^^^^RPPS
    hlseven.pv1.pv1_8 = str(RPPS) + "^^^^^^^^^^^^^RPPS"
    # DATE_ADMISSION : YYYYMMDDHHMMSS
    hlseven.pv1.pv1_44 = str(examen[2].strftime(conf.DT_FORMAT))

    # Construct the ORC segment
    hlseven.orc.orc_1 = "NW"  # Order Control NW
    hlseven.orc.orc_3 = str(examen[0])  # Filler Order Number NUMERO_EXAMEN
    hlseven.orc.orc_7 = "^^^" + \
        str(examen[2].strftime(conf.DT_FORMAT))  # ^^^DATE_ADMISSION
    # DATE_ADMISSION : YYYYMMDDHHMMSS
    hlseven.orc.orc_9 = str(examen[2].strftime(conf.DT_FORMAT))
    # TODO IMPLEMENT
    hlseven.orc.orc12 = str(CODE_PRESC) + "^" + str(medecin[1][1]) + "^" + str(medecin[1][1]) + \
        "^^^^^^^^^^" + \
        str(CODE_PRESC)  # CODE_PRESCRIPTEUR^NOM^PRENOM^^^^^^^^^^RPPS

    # Construct the OBR segment
    # CODE_EXAMEN^TITRE_EXAMEN
    hlseven.obr.obr_4 = str(
        type_intervention[0]) + "^" + str(type_intervention[1])
    """
    MODALITE :
        - CR : RADIO
        - CT : SCANNER
        - MR : IRM
        - XA : ANGIO
        - ES : ENDOSCOPIE
        - US : ECHOGRAPHIE
        - PX : PANORAMIQUE
    """
    hlseven.obr.obr_24 = dicom_mod  # Diagnostic Serv Sect ID, MODALITE
    hlseven.obr.obr_27 = "^^^" + \
        str(examen[2].strftime(conf.DT_FORMAT))  # ^^^DATE_ADMISSION

    return hlseven


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

data = orm.get_medecin(EXAMENS_ID)
if(data):
    MEDECIN_ROWS = (list(data[0]), list(data[1]))
    logger.debug(f"[+] MEDECIN_ROWS {MEDECIN_ROWS} [+]")
logger.debug(f"[+] wtf [+]")

# We map the RPPPS of the current medecin_interv
RPPS = 0
logger.info(f"[+] Getting the RPPS [+]")
try:
    if MEDECIN_ROWS:
        for row in EVOLUCARE_MEDECIN:
            logger.debug(f"[+] {row} [+]")
            if row[1] == MEDECIN_ROWS[0][1] and row[2] == MEDECIN_ROWS[0][2]:
                logger.debug(f"[+] {row[3]} [+]")
                RPPS = row[3]
                logger.debug(f"[+] {RPPS} [+]")
    logger.debug(f"[+] RPPS {RPPS} [+]")
except Exception as e:
    logger.critical(f"[-] CRITICAL ERROR OCCURED : {e} [-]")

# We map the RPPPS of the current medecin_presc, if it does't exist put nothing
CODE_PRESC = 0
logger.info(f"[+] Getting the CODE_PRESC [+]")
try:
    if MEDECIN_ROWS:
        for row in EVOLUCARE_MEDECIN:
            if row[1] == MEDECIN_ROWS[1][1] and row[2] == MEDECIN_ROWS[1][2]:
                CODE_PRESC = row[3]
    logger.debug(f"[+] CODE_PRESC {CODE_PRESC} [+]")
except Exception as e:
    logger.critical(f"[-] CRITICAL ERROR OCCURED : {e} [-]")

try:
    logger.info("[+] Executing main thread [+]")
    if MEDECIN_ROWS:
        # We get the dicom_mod
        dicom_mod = EVOLUCARE_TYPES_INTERVENTION[TYPES_INTERVENTION_ROW[0]][4]
        logger.debug(f"[+] dicom_mod {dicom_mod} [+]")

        logger.info("[+] Constructing the HL7 message [+]")
        # We construct the hlseven class with all the information
        hlseven = constructHl7Orm(hlseven, PATIENT_ROW, EXAMEN_ROW,
                                MEDECIN_ROWS, TYPES_INTERVENTION_ROW, RPPS, CODE_PRESC, dicom_mod)

        # We assign the var with the hl7 message
        ORM_MSG = hlseven.to_er7(trailing_children=True)

        logger.debug(str(ORM_MSG).encode("utf8"))

        # TODO implement server
        # logger.info("[+] Initializing the server [+]")
        logger.info(f"PROCESS FINISHED IN  {time.time() - TIME} seconds \n\n")
    else:
        logger.critical("[-] Critical error, the medecin intervenent was not found [-]")
        logger.info(f"PROCESS FINISHED IN  {time.time() - TIME} seconds \n\n")
except Exception as e:
    logger.critical("[-] Critical error occured while executing main thread [-]")
    logger.critical(f"[-] ERROR : {e} [-]")
    logger.info(f"PROCESS FINISHED IN  {time.time() - TIME} seconds \n\n")
