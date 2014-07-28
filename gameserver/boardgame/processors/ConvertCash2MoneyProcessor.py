'''
Created on Oct 2, 2012

@author: leen
'''
from GenericProcessor import GenericProcessor
import json

class ConvertCash2MoneyProcessor():

    def __init__(self, game, player, arguments):
        self._game = game
        self._player = game.get_player(player)
        self._arguments = arguments
    
    def process(self):
        try:
            cash_amount = int(self._arguments[0])        
            playerstatus = self._player.get_player_status()
            if cash_amount > playerstatus.cash or cash_amount<=0:
                return False
            else:
                user_db = self._game.get_database()
                converted = user_db.convert_cash_to_money(str(self._player), cash_amount)
                if converted:
                    self._player.pull_player_status()
                    self._game.send_output(self._player, ' '.join(['MONEY',str(self._player.get_player_status().money)]))
                    return True
                else:
                    return False
        except:
            return False
        return False
        