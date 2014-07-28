'''
Created on Mar 12, 2012

@author: leen
'''
from GenericProcessor import GenericProcessor
import json

class InfoProcessor():

    def __init__(self, game, player, arguments):
        self._game = game
        self._player = game.get_player(player)
        #self._arguments = arguments
    
    def process(self):        
        playerstatus = self._player.get_player_status()
        result = {'command': 'INFO',
                  'data': 
                    {'avatar': playerstatus.avatar,
                    'money': playerstatus.money,
                    'cash': playerstatus.cash,
                    'total_cash': playerstatus.total_cash,                                    
                    },
                  }        
        #result = json.dumps(data, separators=(',', ':'))
        self._game.send_JSON_output(self._player, result)
        return True
        