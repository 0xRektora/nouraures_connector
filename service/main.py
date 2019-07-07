import conf, logging, datetime, time
from orm import Orm
from hl7 import Hlseven
import sys
"""
    Main entrypoint of the NourAures Connector
"""
TIME = time.time() # Contain the time at the start of the program

logger = conf._init_logger(filehandler=conf.LOG_ALL)


EXAMENS_ID = 10925 # TODO REMOVE
if len(sys.argv) > 1:
    try:
        EXAMENS_ID = sys.argv[1]
        with open("php_call.txt", "a") as f:
            f.writelines(f"System called at {datetime.datetime.now().strftime(conf.DT_FORMAT)} : argv : {sys.argv}\n")
    except:
        logger.critical(f"[+] Can't find the EXAMEN_ID in the arguments passed : {sys.argv} [+]")

EXAMEN_ROW = None # Will contain the examen row
PATIENT_ROW = None # Will contain the patient row
MEDECIN_ROWS = None # Will contain the medeincs rows (intervenant + prescripteur)
TYPES_INTERVENTION_ROW = None # Will contain the medeincs rows (intervenant + prescripteur)

ORM_MSG = None # Will contain the orm message in STR

orm = Orm()
hlseven = Hlseven()

def constructHl7Orm(hlseven, patient, examen, medecin, type_intervention):
    """
        Function that take in param the orm object for patient and examen
        return a fully constructed hl7 object
    """
    # Construct the PID segment
    hlseven.pid.pid_3 = str(patient[0]) + "^^^" + "NourauresConnector" # ID_PATIENT^^^LOGICIEL_GAP
    hlseven.pid.pid_5 = str(patient[2] + "^" + patient[1]) # NOM_PATIENT^PRENOM_PATIENT
    hlseven.pid.pid_7 = str(patient[4].strftime(conf.DT_FORMAT)) # DOB : YYYYMMDD
    hlseven.pid.pid_8 = "M" if str(patient[3]).lower() == "homme" else "F"   # M : MALE / F : FEMALE / O : OTHER / U : UKNOWN

    # Construct the PV1 segment
    hlseven.pv1.pv1_2 = "O" # O : OUTPUT
    hlseven.pv1.pv1_3 = "EXTERNE" # EXTERNE
    # TODO IMPLEMENT
    # hlseven.pv1.pv1_8 = # CODE_RADIOLOGGUE^^^^^^^^^^^^^RPPS
    hlseven.pv1.pv1_44 = str(examen[2].strftime(conf.DT_FORMAT)) # DATE_ADMISSION : YYYYMMDDHHMMSS

    # Construct the ORC segment
    hlseven.orc.orc_1 = "NW" # Order Control NW
    hlseven.orc.orc_3 = str(examen[0]) # Filler Order Number NUMERO_EXAMEN
    hlseven.orc.orc_7 = "^^^"+str(examen[2].strftime(conf.DT_FORMAT)) # ^^^DATE_ADMISSION
    hlseven.orc.orc_9 = str(examen[2].strftime(conf.DT_FORMAT)) # DATE_ADMISSION : YYYYMMDDHHMMSS
    # TODO IMPLEMENT
    #hlseven.orc.orc12 = str(examen[2].strftime(conf.DT_FORMAT)) # CODE_PRESCRIPTEUR^NOM^PRENOM^^^^^^^^^^RPPS

    # Construct the OBR segment
    hlseven.obr.obr_4 = str(type_intervention[0]) + "^" + str(type_intervention[1]) # CODE_EXAMEN^TITRE_EXAMEN
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
    hlseven.obr.obr_24 = "CR" # Diagnostic Serv Sect ID, MODALITE
    hlseven.obr.obr_27 = "^^^" + str(examen[2].strftime(conf.DT_FORMAT)) # ^^^DATE_ADMISSION

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

# We construct the hlseven class with all the information
hlseven = constructHl7Orm(hlseven, PATIENT_ROW, EXAMEN_ROW, MEDECIN_ROWS, TYPES_INTERVENTION_ROW)

# We assign the var with the hl7 message
ORM_MSG = hlseven.to_er7(trailing_children=True)

logger.debug(str(ORM_MSG).encode("utf8"))
logger.info(f"PROCESS FINISHED IN  {time.time() - TIME} seconds \n\n")
