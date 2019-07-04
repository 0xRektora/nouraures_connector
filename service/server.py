from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor


class Echo(Protocol):

    def connectionMade(self):
        print("connected")
        self.transport.write("okk".encode("utf-8"))

    def connectionLost(self, reason):
        print("connection lost")

    def dataReceived(self, data):
        self.transport.write(data)

class EchoFactory(Factory):
    def buildProtocol(self, addr):
        return Echo()

endpoint = TCP4ServerEndpoint(reactor, 8888)
endpoint.listen(EchoFactory())
reactor.run()