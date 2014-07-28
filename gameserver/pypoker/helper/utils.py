'''
Created on Apr 15, 2014

@author: leen
'''
def get_card_value(value):
    number_value = (value / 4) + 1
    if number_value < 2:
        """aces"""
        number_value = number_value + 13
    suit_value = value % 4
    return (number_value, suit_value)

def is_pair(card_set):
    if len(card_set) == 2:
        kind1, _ = get_card_value(card_set[0])
        kind2, _ = get_card_value(card_set[1])
        if kind1 == kind2:
            return True
    return False

def is_containing_6_pairs(cards):
    card_set = sorted(cards)    
    length = len(card_set)
    _i = 0
    pair_count = 0
    while _i < length:
        if _i+1 < length:
            if is_pair([card_set[_i], card_set[_i+1]]):
                pair_count +=1
                _i = _i +2
                continue
        _i = _i + 1
    if pair_count == 6:
        return True
    return False

def is_13_unique_cards(cards):
    card_set = sorted(cards)
    correct = True
    for i in range(len(card_set)):
        kind, _ = get_card_value(card_set[i])
        if i+2 != kind:
            correct = False
            break
    return correct

def count_key_in_dict(my_dict, key):
    if key in my_dict:
        my_dict[key] += 1
    else:
        my_dict[key] = 1
    