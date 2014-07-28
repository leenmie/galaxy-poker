'''
Created on Feb 21, 2012

@author: leen
'''

class GenericProcessor(object):
    '''
    Generic Processor
    '''
    def __init__(self, game, player, arguments):
        self._game = game
        self._player = game.get_player(player)    
        self._arguments = arguments
        if not self._player:
            raise Exception('Can not find player')
    
    def process(self):
        pass