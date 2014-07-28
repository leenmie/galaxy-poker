'''
Created on Apr 3, 2012

@author: leen
'''
import cProfile
from boardgame.TexasPoker.runner import run_game
import sys
import logging
import logging.config

logging.config.fileConfig('logging.conf')
LOGGER = logging.getLogger('gamedebug')

if __name__ == '__main__':
    #cProfile.run('run_game()','profileoutput')
    try:
        run_game()
    except:
        raise
        LOGGER.error(' '.join(["Unexpected error:", str(sys.exc_info()[0]),
                               str(sys.exc_info()[1]), str(sys.exc_info()[2])]))