import conf, logging
from orm import Orm
from hl7 import Hlseven

"""
    Main entrypoint of the NourAures Connector
"""

conf.logging_state()

EXAMENS_ID = 10925 # TODO REMOVE
EXAMEN_ROW = None # Will contain the examen row
PATIENT_ROW = None # Will contain the patient row

orm = Orm()
hlseven = Hlseven()

data = orm.get_examen(EXAMENS_ID)
if(data):
    EXAMEN_ROW = list(data)[0]
    logging.debug(f"[+] EXAMEN_ROW {EXAMEN_ROW} [+]")

data = orm.get_patient(EXAMENS_ID)
if(data):
    PATIENT_ROW = list(data)[0]
    logging.debug(f"[+] PATIENT_ROW {PATIENT_ROW} [+]")
