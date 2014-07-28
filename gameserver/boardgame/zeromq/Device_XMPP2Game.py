'''
Created on Mar 1, 2012

@author: leen
'''
import zmq
import json

import random
import time
import twisted.internet.error
from twisted.internet import reactor, defer
from boardgame.utils.Message import Message
from boardgame.main_config import MSGQUEUE_XMPP_BIND_STRING, MSGQUEUE_GAME_BIND_STRING_OUTBOUND, MSGQUEUE_GAME_BIND_STRING_INBOUND
import logging
import logging.config

logging.config.fileConfig('logging.conf')
LOGGER = logging.getLogger('devicedebug')

"""TODO: JSON"""

class Device_XMPP2Game():
    def __init__(self):                
        self.__context = zmq.Context()
        self._socketxmpp = self.__context.socket(zmq.DEALER)
        self._socketgame = self.__context.socket(zmq.PULL)
        self._socketgame_sends = []
        for c_string in MSGQUEUE_GAME_BIND_STRING_INBOUND:            
            _socket_send = self.__context.socket(zmq.PUSH)
            _socket_send.connect(c_string)
            self._socketgame_sends.append(_socket_send)        
        for connect_str in MSGQUEUE_XMPP_BIND_STRING:
            #connect_str = 'tcp://' + host + ':' + str(MSGQUEUE_XMPP_PORT)
            self._socketxmpp.connect(connect_str)
        for connect_str in MSGQUEUE_GAME_BIND_STRING_OUTBOUND:
            #connect_str = 'tcp://' + host + ':' + str(MSGQUEUE_GAME_PORT_OUTBOUND)
            self._socketgame.connect(connect_str)
        self._poller = zmq.Poller()
        self._poller.register(self._socketxmpp,zmq.POLLIN)
        self._poller.register(self._socketgame,zmq.POLLIN)
#       if not NO_DATABASE:
#           self._router_connecter = MemcacheConnector()
        self._routing_table = dict()
        self._running = True
        self._message_count_recv = 0
        self._begin_time_recv = None
        self._message_count_send = 0
        self._begin_time_send = None

        
    def _find_connection_str(self, msg):
        message = json.loads(msg)
        username = message['from_user']
        routing = None
        if self._routing_table.has_key(username):
            routing = self._socketgame_sends[self._routing_table[username]]
        #get routing from database
#        if not routing and not NO_DATABASE:
#            routing = self._router_connecter.get(username)
        #if routing:
        #    print routing
        if not routing:
            countn = len(MSGQUEUE_GAME_BIND_STRING_INBOUND)
            indx = random.randint(0,countn-1)
            routing = self._socketgame_sends[indx]
            self._routing_table[username] = indx
            #print 'Add routing for', username
#            if not NO_DATABASE:
#                self._router_connecter.set(username, routing)
        #print routing
        return routing
    
    def _process_ouput_msg(self, msg):
        message = json.loads(msg)
        body_data = message['body']
        username = message['from_user']
        body_data_parts = body_data.split()
        try:
            msg_code = body_data_parts[0]
            if msg_code == 'PART':
                username_inpart = body_data_parts[1]
                if username == username_inpart:
                    if self._routing_table.has_key(username):
                        del self._routing_table[username]
                        #print 'Clear routing for', username            
        except:
            pass
        #if body_data == 'PART 00':
                #print 'Clear routing for', username
    
    def start(self, d=None):
        if not d:
            d = defer.Deferred()
            self._running = True
        if self._running:            
            socks = dict(self._poller.poll())   
            #send msg to game
            if self._socketxmpp in socks and socks[self._socketxmpp] == zmq.POLLIN:
                if self._message_count_recv == 0:
                    self._begin_time_recv = time.time()
                msg = self._socketxmpp.recv()
                _socket_send = self._find_connection_str(msg) 
                _socket_send.send(msg)
                #print msg                                
                self._message_count_recv += 1
                if self._message_count_recv == 10000:
                    delta_time = time.time() - self._begin_time_recv
                    LOGGER.debug(' '.join(['Received 10000 messages in [', str(delta_time), ']seconds.']))
                    self._message_count_recv = 0
                    self._begin_time_recv = time.time()
                #print 'Send', msg                
            if self._socketgame in socks and socks[self._socketgame] == zmq.POLLIN:
                if self._message_count_send == 0:
                    self._begin_time_send = time.time()                
                
                msg = self._socketgame.recv()
                self._process_ouput_msg(msg)                                
                self._socketxmpp.send(msg)
                
                self._message_count_send += 1
                if self._message_count_send == 10000:
                    delta_time = time.time() - self._begin_time_send
                    LOGGER.debug(' '.join(['Sent 10000 messages in [', str(delta_time), ']seconds.']))
                    self._message_count_send = 0
                    self._begin_time_send = time.time()
                
            reactor.callLater(0.0001, self.start, d)
        return d
            
    def stop(self):
        try:
            self._running = False
            #self._router_connecter.close()
            reactor.stop()
        except twisted.internet.error.ReactorNotRunning:
            pass
        except:
            raise

if __name__ == "__main__":
    try:        
        device = Device_XMPP2Game()
        device.start()
        reactor.run()
        #print 'Device start ...'
    except KeyboardInterrupt:
        device.stop()
