'''
Created on Apr 3, 2012

@author: leen
'''
from twisted.internet import reactor
from boardgame.zeromq.Device_XMPP2Game import Device_XMPP2Game
import cProfile
import sys
import logging
import logging.config

logging.config.fileConfig('logging.conf')
LOGGER = logging.getLogger('devicedebug')

def run_device():
    try:
        device = Device_XMPP2Game()
        device.start()
        reactor.run()
#        print 'Device start ...'
    except KeyboardInterrupt:
        device.stop()

if __name__ == '__main__':
    #cProfile.run('run_device()','profdevoutput')
    try:
        run_device()
    except:
        LOGGER.error(' '.join(["Unexpected error:", str(sys.exc_info()[0]),
                               str(sys.exc_info()[1]), str(sys.exc_info()[2])])) 
        raise
