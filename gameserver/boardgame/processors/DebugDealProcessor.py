'''
Created on Jun 9, 2012

@author: leen
'''
import logging
from GenericProcessor import GenericProcessor
from boardgame.utils.Deck import Deck

LOGGER = logging.getLogger('gamedebug')

class DebugDealProcessor(GenericProcessor):

    def process(self):        
        current_room_id = self._player.get_current_room()
        current_room = self._game.get_room(current_room_id)
        if current_room:
            cards_parsing = []
            try:
                for arg in self._arguments:
                    value = int(arg)
                    if value in range(0,52):
                        cards_parsing.append(value)
                    else:
                        raise(Exception('Invalid card\'s value'))
                if len(cards_parsing) != 52:
                    raise(Exception('Invalid deck length'))
                deck = Deck()
                deck.set_card_list(cards_parsing)
                current_room.debug_only_set_deck(deck)
                self._game.send_output(self._player, 'DEBUGDEAL 00')                
            except:
                self._game.send_output(self._player, 'DEBUGDEAL 02')            
                return False            
            #current_room.ready(self._player)           
            return True
        else:
            self._game.send_output(self._player, 'DEBUGDEAL 01')
            return False