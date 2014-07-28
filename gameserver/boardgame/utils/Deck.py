'''
Created on Feb 22, 2012

@author: leen
'''
import random
import copy
#lfrom boardgame.utils.SimplePointCard import SimplePointCard
from collections import deque


DECK_LENGTH = 52

class Deck(object):    
    def __init__(self):
        self._card_list = deque(range(0,DECK_LENGTH))
        self.reset()
        
    def reset(self):        
        #shuffle        
        fullcard = range(0,DECK_LENGTH)
        #use a secure random number generator
        sysrandom = random.SystemRandom()
        sysrandom.shuffle(fullcard) 
        self._card_list = deque(fullcard)
    
    #use for debug purpose only            
    def set_card_list(self, cards):
        self._card_list = deque(cards)
        
    def get_card(self):
        if self._card_list:
            return self._card_list.popleft()
        else:
            return None