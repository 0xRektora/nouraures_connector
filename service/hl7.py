from hl7apy.core import Message
import logging
import uuid  # TODO REMOVE
from utils import Singleton


class Hlseven(Message, Singleton):
    """
    Class that'll take care of the Hlseven messages
    """

    def __init__(self):

        logging.debug("[-] Hlseven initialized [-]")
        super().__init__()
        self.name = "ORM_01"
        self.init_msh()
        self.init_pid()
        self.init_pv1()
        self.init_orc()
        self.init_obr()

        logging.debug("[+] Hlseven initialized [+]")

    def init_msh(self):
        """
            Function that init the msh headers
        """
        logging.debug("[-] Init MSH [-]")
        self.msh.msh_1 = "|"
        self.msh.msh_3 = "NourauresConnector"
        self.msh.msh_4 = "NourAures"
        self.msh.msh_5 = "EVOLUCARE"
        self.msh.msh_6 = "EVOLUCARE"
        self.msh.msh_7 = "YYYYMMDDHHMMSS"
        self.msh.msh_9 = "ORM^O01"
        self.msh.msh_10 = str(uuid.uuid4())  # TODO CHANGE LATER
        self.msh.msh_11 = "P"
        self.msh.msh_12 = "2.3.1"
        self.msh.msh_15 = "NE"
        logging.debug("[+] Init MSH [+]")

    def init_pid(self):
        self.add_segment("PID")

    def init_pv1(self):
        self.add_segment("PV1")

    def init_orc(self):
        self.add_segment("ORC")

    def init_obr(self):
        self.add_segment("OBR")


if __name__ == "__main__":
    import conf
    logger = conf._init_logger(logger=conf.LOGGER_HL7, filehandler=False)
    m = Hlseven()
    logging.debug("\n"+m.to_er7(trailing_children=True))
