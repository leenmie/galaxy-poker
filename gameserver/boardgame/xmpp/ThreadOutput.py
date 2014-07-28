'''
Created on Mar 1, 2012

@author: leen
'''
from twisted.internet import reactor, defer
from boardgame.utils.Message import Message
#import cPickle
import json
import zmq
from twisted.internet import reactor
from threading import Thread
class ThreadOutput():
    def __init__(self, socket, xmpp):        
        self._socket = socket
        self._xmpp = xmpp
        self._running = True
    
    def start(self, d = None):
        if not d:
            d = defer.Deferred()
            self._running = True
        if self._running:
            socket = self._socket.get_socket()
            poller = zmq.Poller()
            poller.register(socket, zmq.POLLIN)
            xmpp = self._xmpp        
            socks = dict(poller.poll(10))
            if socket in socks and socks[socket] == zmq.POLLIN:
                data = socket.recv()                        
                msg = json.loads(data)
                reactor.callFromThread(xmpp.sendBack, msg)
            reactor.callLater(0.0001, self.start, d)
        return d
    
    def stop(self):
        self._running = False