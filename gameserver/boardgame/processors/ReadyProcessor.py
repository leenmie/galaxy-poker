'''
Created on Feb 22, 2012

@author: leen
'''
import logging
from GenericProcessor import GenericProcessor

LOGGER = logging.getLogger('gamedebug')

class ReadyProcessor(GenericProcessor):

    def process(self):        
        current_room_id = self._player.get_current_room()
        current_room = self._game.get_room(current_room_id)
        if current_room:
            self._game.send_output(self._player, 'READY 00')
            current_room.ready(self._player)
            #self._player.update_active_time()          
            return True
        else:
            self._game.send_output(self._player, 'READY 01')
            return False