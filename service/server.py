from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
import conf, logging

class HlsevenProtocol(Protocol):
    def __init__(self, factory):
        self.logger = conf._init_logger(logger=conf.LOGGER_SERVER)
        self.logger = logging.getLogger(conf.LOGGER_SERVER)

        self.logger.info("[+] Initilizing Server [+]")
        self.factory = factory
        self.ack_try = 5 # Number of time trying to receive the right ACK
        self.logger.info(f"[+] Listening on {self.factory.addr} [+]")

    def connectionMade(self):
        """
            Fire up the sendHlseven function when connection is made
        """
        self.logger.info("[+] Connection made [+]")
        self.sendHlseven()

    def connectionLost(self, reason):
        """
            Fire up when the connection is lost
        """
        self.logger.info(f"[+] Connection lost reason : {reason} [+]")

    def dataReceived(self, data):
        """
            Fire up when data is received
        """
        # TODO Check for the ACK
        data = self.decodeData(data)
        self.logger.info(f"[+] data received [+]")
        self.logger.info(f"{data}")
        if(data):
            self.logger.info("[+] Cutting connection, job finished [+]")
            self.transport.abortConnection()
        else:
            if self.ack_try == 0:
                self.logger.critical(f"[-] 0 attempts remained, errors occured, aborting connection [-]")
                self.transport.abortConnection()
            self.ack_try -= 1
            self.logger.warning(f"[-] ACK may not be what expected, {self.ack_try} attempts remained [-]")

    def sendHlseven(self):
        """
            Method called to send the HL7 message
            turn into a er7 string encoded in byte with utf8 encoding
        """
        self.logger.info("[+] Sending the Hl7 object [+]")
        self.logger.debug(f"{self.factory.hl7}")

        self.transport.write(self.encodeData(self.factory.hl7.to_er7(trailing_children=True)))

    def encodeData(self, data):
        return str(data).encode("utf8")

    def decodeData(self, data):
        return str(data.decode("utf8"))


class HlsevenFactory(Factory):
    """
        The factory class of the Hlseven server
    """
    def __init__(self, hl7):
        self.hl7 = hl7

    def buildProtocol(self, addr):
        self.addr = addr
        return HlsevenProtocol(self)

if __name__ == "__main__":
    import hl7
    hl = hl7.Hlseven()
    endpoint = TCP4ServerEndpoint(reactor, conf.SERVER_PORT)
    endpoint.listen(HlsevenFactory(hl))
    print("Running server")
    reactor.run() #pylint: disable=no-member