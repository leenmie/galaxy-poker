import time
import logging
#import cPickle
import json
from twisted.internet import reactor, defer
from twisted.python import log
from MessageProcessor import MessageProcessor
from MessageProcessor import JSONMessageProcessor
from Message import Message
from threading import Thread
from Queue import Empty
LOGGER = logging.getLogger('gamedebug')
class Processor():        
    
    def __init__(self):        
        self._running = True
        
    def process(self):
        pass
            
    def start(self, d = None):        
        if not d:        
            self._running = True
            d = defer.Deferred()
        if self._running:            
            reactor.callLater(0.0001, self.start, d)
            try:
                self.process()
            except:                
                LOGGER.error(' '.join(['Input process error', 'processor.process()']))
                raise
            #time.sleep(0.1)
        return d
    
    def stop(self):
        self._running = False


class InputProcessor(Processor):
    def __init__(self, game):
        Processor.__init__(self)
        self._queue = game.get_input_queue()
        self._game = game
        #self._message_processor = MessageProcessor(game)
        self._message_processor = JSONMessageProcessor(game)
    
    def process(self):
        #print "Process"        
        message = None        
        data = self._queue.receive()
        if data:            
            mm = json.loads(data)
            message = Message(mm['from_user'],mm['body'])
            #print message
        if message:
            try:
                self._message_processor.process(message)
            except:                
                LOGGER.error(' '.join(['Cannot process',str(data)]))
                raise                