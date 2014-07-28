'''
Created on Jul 15, 2012

@author: leen
'''
import logging
import time
from GenericProcessor import GenericProcessor

LOGGER = logging.getLogger('gamedebug')

class PingProcessor(GenericProcessor):

    def process(self):
        try:
            random_value = int(self._arguments[0])
            time_value = int(self._arguments[1])
            LOGGER.debug(' '.join(['got PING', str(random_value), str(time_value)]))            
            current_time_value = int(time.time())
            self._game.send_output(self._player, ' '.join(['PING', str(random_value), str(current_time_value)]))
            return True
        except:
            return False        
