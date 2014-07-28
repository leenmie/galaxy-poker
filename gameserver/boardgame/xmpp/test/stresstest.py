'''
Created on Jul 26, 2012

@author: leen
'''
import logging
import random, time
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
#from sleekxmpp.plugins import PluginManager
dnspython = None

COUNT = 20000
class EchoBot(ClientXMPP):
    
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
        #self.plugin.disable('feature_bind')
        #self.plugin.disable('feature_mechanisms')
        #self.plugin.disable('feature_session')
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self._count = 0
        self._begin_time = None
    def test_send(self):
        for _ in range(COUNT):            
            self.send_message(mto='game.ubuntu',
                              #mbody=' '.join(['ping',str(random.randint(0,100000)), str(int(time.time()))]),
                              mbody='join 100',
                              mtype='chat')
                              
            """                                                  
            self.send_message(mto='tienlen.xmpp.cacafefe.com',
                              #mbody=' '.join(['ping',str(random.randint(0,100000)), str(int(time.time()))]),
                              mbody='join 100',
                              mtype='chat')                    
            """

    def session_start(self, event):
        #self.send_presence()
        #self.get_roster()        
        pass
     
    def message(self, msg):        
        if self._count == 0:
            self._begin_time = time.time()
        if 'JOIN' in msg['body']:            
            self._count += 1
            #logging.debug('Count: '+str(self._count))        
            if self._count == COUNT:
                #print 'Complete count at', time.time()
                delta = time.time() - self._begin_time
                print 'Processing time: ', delta, 'seconds'
                print 'Processing speed: ', COUNT/delta, 'per second'
                self._count = 0
    

if __name__ == '__main__':
    # Ideally use optparse or argparse to get JID,
    # password, and log level.

    logging.basicConfig(level=logging.WARNING,
                        format='%(levelname)-8s %(message)s')

    xmpp = EchoBot('test100@ubuntu', '123456')
    xmpp.connect(address=('localhost',5222))
    before_t = time.time()
    print 'Begin time at', time.time()
    xmpp.process(block=False)
    xmpp.send_presence()
    xmpp.test_send()
    delta_t = time.time() - before_t
    print 'Speed: ', COUNT / delta_t
    