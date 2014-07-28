'''
Created on May 5, 2014

@author: leen
'''
from boardgame.utils.Game import Game
from boardgame.TexasPoker.TexasPokerRoom import TwoPlayerTexasPokerRoom
from boardgame.TexasPoker.TexasPokerPlayer import TexasPokerPlayerList

class TexasPokerGame(Game):
    
    def __init__(self):
        super(TexasPokerGame, self).__init__()
        """override player_list"""
        self._player_list = TexasPokerPlayerList(self)
        self.get_player = self._player_list.get_player
    
    def get_room(self, room_id):
        room_status = self._room_list.get_room(room_id)
        if room_status:            
            return TwoPlayerTexasPokerRoom(room_status, self)
        return None
        
    def get_random_available_room(self, betting_money=0):
        if not betting_money:
            betting_money = TwoPlayerTexasPokerRoom.INIT_STAKE
        room_status = self._room_list.get_random_available_room(betting_money)        
        if room_status:            
            return TwoPlayerTexasPokerRoom(room_status, self)
        return None
