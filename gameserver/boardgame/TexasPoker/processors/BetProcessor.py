'''
Created on May 6, 2014

@author: leen
'''
'''
Created on May 5, 2014

@author: leen
'''
from boardgame.processors.GenericProcessor import GenericProcessor
import logging
LOGGER = logging.getLogger('gamedebug')

class BetProcessor(GenericProcessor):
    
    def process(self):
        action = self._arguments['action']
        money = 0
        if 'amount' in self._arguments:
            try:
                money = int(self._arguments['amount'])
            except:
                raise
        current_room_id = self._player.get_current_room()
        current_room = self._game.get_room(current_room_id)
        if action not in ['raise', 'call', 'check', 'fold']:
            return False
        current_room.action_bet(action, self._player, money)
        return True