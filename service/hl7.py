from hl7apy.core import Message
import logging, conf, datetime
import uuid  # TODO REMOVE
from utils import Singleton


class Hlseven(Message):
    """
    Class that'll take care of the Hlseven messages
    """

    def __init__(self):
        logger = conf._init_logger(logger=conf.LOGGER_HL7)
        logger = logging.getLogger(conf.LOGGER_HL7)
        logger.debug("[-] Hlseven initialized [-]")

        super().__init__()

        self.name = "ORM_O01"

        # Initing all the segment of the HL7 message
        self.init_msh(logger)
        self.init_pid()
        self.init_pv1()
        self.init_orc()
        self.init_obr()

        logger.debug("[+] Hlseven initialized [+]")

    def init_msh(self, logger):
        """
            Function that init the msh headers
        """
        logger.debug("[-] Init MSH [-]")
        self.msh.msh_1 = "|"
        self.msh.msh_3 = "NourauresConnector"
        self.msh.msh_4 = "NourAures"
        self.msh.msh_5 = "EVOLUCARE"
        self.msh.msh_6 = "EVOLUCARE"
        self.msh.msh_7 = datetime.datetime.now().strftime(conf.DT_FORMAT)
        self.msh.msh_9 = "ORM^O01"
        self.msh.msh_10 = str(uuid.uuid4())  # TODO CHANGE LATER
        self.msh.msh_11 = "P"
        self.msh.msh_12 = "2.3.1"
        self.msh.msh_15 = "NE"
        logger.debug("[+] Init MSH [+]")

    def init_pid(self):
        self.add_segment("PID")
        self.pid.pid_11 = "" # Empty to respect the matrix

    def init_pv1(self):
        self.add_segment("PV1")
        self.pv1.pv1_44 = ""

    def init_orc(self):
        self.add_segment("ORC")
        self.orc.orc_13 = ""

    def init_obr(self):
        self.add_segment("OBR")
        self.obr.obr_27 = ""


if __name__ == "__main__":
    import conf
    m = Hlseven()
