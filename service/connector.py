from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint
import conf
"""
    Test class
"""

class Greeter(Protocol):
    def sendMessage(self, msg):
        self.transport.write("MESSAGE %s\n" % msg)

    def dataReceived(self, data):
        print(data.decode("utf8"))
        self.transport.write("0".encode("utf8"))

class GreeterFactory(Factory):
    def buildProtocol(self, addr):
        return Greeter()

def gotProtocol(p):
    p.sendMessage("Hello")
    reactor.callLater(1, p.sendMessage, "This is sent in a second")
    reactor.callLater(2, p.transport.loseConnection)

point = TCP4ClientEndpoint(reactor, conf.SERVER_IP, conf.SERVER_PORT)
d = point.connect(GreeterFactory())
d.addCallback(gotProtocol)
reactor.run()