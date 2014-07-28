'''
Created on Mar 1, 2012

@author: leen
'''
import zmq
from boardgame.main_config import MSGQUEUE_GAME_PORT_INBOUND, MSGQUEUE_GAME_PORT_OUTBOUND
#MSGQUEUE_GAME_PORT_INBOUND = 5001
#MSGQUEUE_GAME_PORT_OUTBOUND = 5002

class MsgQueue_Game():
    
    def __init__(self, inbound_port = MSGQUEUE_GAME_PORT_INBOUND, outbound_port = MSGQUEUE_GAME_PORT_OUTBOUND):
        self.__context = zmq.Context()
        #inbound
        self._socketinbound = self.__context.socket(zmq.PULL)
        bind_str = 'tcp://*:' + str(inbound_port)        
        self._socketinbound.bind(bind_str)        
        
        #outbound
        self._socketoutbound = self.__context.socket(zmq.PUSH)
        bind_str = 'tcp://*:' + str(outbound_port)
        self._socketoutbound.bind(bind_str)
        self._poller = zmq.Poller()
        self._poller.register(self._socketinbound,zmq.POLLIN)
        
        import socket
        self._inbound_bind_str = ''.join(['tcp://',socket.gethostname(),':',str(inbound_port)])
        
    def get_inbound_bind_str(self):
        return self._inbound_bind_str        
        
    def get_socket_inbound(self):
        return self._socketinbound
    
    def get_socket_outbound(self):
        return self._socketoutbound
    
    def receive(self):        
        msg = None
        socks = dict(self._poller.poll(100))                        
        if self._socketinbound in socks and socks[self._socketinbound] == zmq.POLLIN:
            #print msg
            msg = self._socketinbound.recv()                        
        return msg
    
    def send(self, msg):
        return self._socketoutbound.send(msg)
    
    def stop(self):
        self._socketinbound.close()
        self._socketoutbound.close()
    
if __name__ == "__main__": 
    queue_game = MsgQueue_Game()
    print queue_game.get_inbound_bind_str()    
    