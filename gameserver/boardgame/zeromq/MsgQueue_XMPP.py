'''
Created on Mar 1, 2012

@author: leen
'''
import zmq
from boardgame.main_config import MSGQUEUE_XMPP_PORT

#MSGQUEUE_XMPP_PORT = 5000

class MsgQueue_XMPP():
    def __init__(self, running_port = MSGQUEUE_XMPP_PORT):
        self.__context = zmq.Context()
        self._socket = self.__context.socket(zmq.DEALER)
        bind_str = 'tcp://*:' + str(running_port)
        self._socket.bind(bind_str)

    def get_socket(self):
        return self._socket
    
    def receive(self):
        return self._socket.recv()
    
    def send(self, msg):
        return self._socket.send(msg)
    
def test():
    queue = MsgQueue_XMPP()

if __name__ == '__main__':
    test()