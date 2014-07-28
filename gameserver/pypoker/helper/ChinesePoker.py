'''
Created on Apr 15, 2014

@author: leen
'''
import copy
from helper.utils import get_card_value

def is_front_flush(card_set):
    if len(card_set) != 3:
        raise Exception("This function only works with front set.")
    cards = copy.copy(card_set)
    is_flush = True
    _, suit = get_card_value(cards[0])
    for i in range(1,3):
        _, ss = get_card_value(cards[i])
        if ss != suit:
            is_flush = False
            break    
    return is_flush

def is_front_straight(card_set):
    if len(card_set) != 3:
        raise Exception("This function only works with front set.")
    cards = copy.copy(card_set)
    cards.sort()    
    is_straight = True
    kind, _ = get_card_value(cards[0])
    for i in range(1,3):
        k, _ = get_card_value(cards[i])
        kind+=1
        if k!= kind:
            is_straight = False
            break
    return is_straight
