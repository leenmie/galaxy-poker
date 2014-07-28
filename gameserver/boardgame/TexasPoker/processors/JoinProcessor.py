'''
Created on May 5, 2014

@author: leen
'''
from boardgame.processors.GenericProcessor import GenericProcessor
import logging
LOGGER = logging.getLogger('gamedebug')

class JoinProcessor(GenericProcessor):
    
    def process(self):
        betting_money = 0
        try:
            if "betting_money" in self._arguments:
                betting_money = int(self._arguments["betting_money"])
        except:
            pass
        current_room_id = self._player.get_current_room()
        if current_room_id:
            current_room = self._game.get_room(current_room_id)
            if current_room:                
                current_room.part(self._player)
            
        room = self._game.get_random_available_room(betting_money)
        if room:
            res = room.join(self._player)
        else:
            LOGGER.debug('No available room')
            return False
        self._player.update_active_time()        
        return True