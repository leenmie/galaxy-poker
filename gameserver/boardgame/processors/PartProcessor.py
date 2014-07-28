'''
Created on Feb 21, 2012

@author: leen
'''
import logging
from GenericProcessor import GenericProcessor

LOGGER = logging.getLogger('gamedebug')

class PartProcessor(GenericProcessor):
    '''
    classdocs
    '''
    def process(self):        
        current_room_id = self._player.get_current_room()
        if current_room_id:
            current_room = self._game.get_room(current_room_id)
            res = current_room.part(self._player)
            #if res:
            #    self._game.del_route(str(self._player))
            if not res:
                LOGGER.error(str(self._player) + ' can not part room '+ str(current_room))
                self._game.send_output(self._player, 'PART 01')                
                return False
                
        else:
            LOGGER.warning(str(self._player) + ' is not in any room')
            self._game.send_output(self._player, 'PART 02')
            return False        
        self._player.update_active_time()
        self._game.send_output(self._player, 'PART 00')
        return True