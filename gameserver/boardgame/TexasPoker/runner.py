'''
Created on May 5, 2014

@author: leen
'''
'''
Created on Feb 24, 2012

@author: leen
'''

import logging.config
from boardgame.TexasPoker.TexasPokerGame import TexasPokerGame
from twisted.internet import reactor
#from twisted.python import log

def run_game():
    logging.config.fileConfig('logging.conf')
    #disable logging ?
    logging.disable(0)
    game = TexasPokerGame()
    game.start()
    reactor.run()
    