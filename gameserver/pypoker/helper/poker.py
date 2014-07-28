'''
Created on Apr 17, 2014

@author: leen
'''
from pypoker.PokerCard import PokerCard
from pypoker.PokerHand import PokerHand

def get_PokerHand_from_list(number_list):
    cards1 = [PokerCard(n) for n in number_list]
    return PokerHand(cards1)
