import conf, logging
from orm import Orm
from hl7 import Hlseven

"""
    Main entrypoint of the NourAures Connector
"""

conf.logging_state()

EXAMENS_ID = 10925 # TODO REMOVE

orm = Orm()
hlseven = Hlseven()

data = orm.get_examen(EXAMENS_ID)
if(data):
    print(list(data))

data = orm.get_patient(EXAMENS_ID)
if(data):
    print(list(data))
