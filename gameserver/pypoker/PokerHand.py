'''
Created on Apr 15, 2014

@author: leen
'''
import copy
from helper.utils import count_key_in_dict

HIGH_CARD = 0x01
ONE_PAIR = 0x02
TWO_PAIR = 0x03
THREE_OF_A_KIND = 0x04
STRAIGHT = 0x05
FLUSH = 0x06
FULL_HOUSE = 0x07
FOUR_OF_A_KIND = 0x08
STRAIGHT_FLUSH = 0x09

class PokerHand():
    """get a list of cards, return some values in poker
        number of cards should be <=7"""
    def __init__(self, cards):
        if not cards:
            raise Exception("Null poker hand")
        if len(cards) > 7:
            raise Exception("This implementation does not support a hand which have more than 7 cards")        
        self._cards = sorted(cards)
        self.hand = HIGH_CARD
        self.mean_cards = []
        """process cards"""
        self._process()
    
    def _process(self):
        self._calculate_hand_and_count_suit_kind()
        self._get_mean_cards_and_correct_hand_type()
        
    def _calculate_hand_and_count_suit_kind(self):        
        kind_list = {}
        suit_list = {}
        cards = self._cards
        hand = self.hand
        seq = 1
        has_pair = False
        has_3ofakind = False
        """if ace is in the our hand, it must be at highest position"""
        has_ace = (cards[-1].kind == 14)
        last_kind = cards[0].kind        
        _index = 0
        length = len(cards)
        while _index < length:
            _card = cards[_index]
            kind, suit = _card.kind, _card.suit
            count_key_in_dict(kind_list, kind)
            count_key_in_dict(suit_list, suit)            
            if (last_kind != kind) or (_index == length-1):                
                if (kind_list[last_kind] == 2):
                    """
                    if we have a pair, we may have ONE PAIR
                    or TWO PAIR or FULL HOUSE
                    """
                    hand = max(hand, ONE_PAIR)
                    if has_3ofakind:
                        hand = max(hand, FULL_HOUSE)
                    else:
                        if has_pair:
                            hand = max(hand, TWO_PAIR)
                    has_pair = True                
                if (kind_list[last_kind] == 3):
                    """
                    if we have a 3 of a kind, we may have THREE of A KIND
                    or FULL HOUSE
                    """
                    if not has_pair:
                        hand = max(hand, THREE_OF_A_KIND)
                    else:
                        hand = max(hand, FULL_HOUSE)
                    has_pair = True
                    has_3ofakind = True
                if (kind_list[last_kind] >= 4):
                    hand = max(hand, FOUR_OF_A_KIND)                
                if (kind - last_kind == 1):
                    """if we have a sequence"""
                    seq+=1
                    if seq >= 5:
                        hand = max(hand, STRAIGHT)
                    if seq == 4:
                        if kind == 5 and has_ace:
                            hand = max(hand, STRAIGHT)                        
                elif (kind - last_kind > 1):
                    seq = 1
                last_kind = kind
            _index+=1        
        self._kind_list = kind_list
        self._suit_list = suit_list
        self.hand = hand
        
    def _get_mean_cards_and_correct_hand_type(self):
        cards = self._cards
        hand = self.hand
        mean_cards = []
        kind_list = self._kind_list
        suit_list = self._suit_list
        """mean cards quantity are <= 5"""        
        remaining_cards = min(5, len(cards))
        
        def add_to_mean_cards(card_list):            
            mean_cards.extend(card_list)
            remaining = remaining_cards - len(card_list)            
            return remaining
                    
        if hand == HIGH_CARD:
            """get highest cards in value"""
            for _index in range(len(cards)-1, -1, -1):                
                remaining_cards = add_to_mean_cards([cards[_index],])
                if remaining_cards == 0:
                    break
                
        if hand == ONE_PAIR:
            """get highest pair, then highest cards"""
            remaining_pairs = 1
            _index = len(cards) - 1
            while remaining_cards > 0 and _index>=0:
                kind = cards[_index].kind
                if remaining_pairs:
                    if remaining_cards > 2:
                        """we have to leave available slots for a pair"""
                        if kind_list[kind] == 1:
                            remaining_cards = add_to_mean_cards([cards[_index], ])
                    if kind_list[kind] == 2:
                        """we found highest pair, add them to our mean cards"""
                        remaining_cards = add_to_mean_cards([cards[_index], cards[_index-1], ])
                        _index -= 2
                        remaining_pairs -= 1
                        continue
                else:
                    """add remaining cards from high to low"""
                    remaining_cards = add_to_mean_cards([cards[_index], ])
                _index -= 1
        
        if hand == TWO_PAIR:
            remaining_pairs = 2
            _index = len(cards) - 1
            while remaining_cards > 0 and _index>=0:
                kind = cards[_index].kind
                if remaining_pairs:
                    if remaining_cards > remaining_pairs*2:
                        if kind_list[kind] == 1:
                            remaining_cards = add_to_mean_cards([cards[_index], ])
                    if kind_list[kind] == 2:
                        remaining_cards = add_to_mean_cards([cards[_index], cards[_index-1], ])
                        _index -= 2
                        remaining_pairs -= 1
                        continue
                else:
                    remaining_cards = add_to_mean_cards([cards[_index], ])
                _index -= 1
                
        if hand == THREE_OF_A_KIND:
            remaining_three = 1
            _index = len(cards) - 1
            while remaining_cards > 0 and _index>=0:
                kind = cards[_index].kind
                if remaining_three:
                    if remaining_cards > 3:
                        if kind_list[kind] == 1:
                            remaining_cards = add_to_mean_cards([cards[_index], ])
                    if kind_list[kind] == 3:
                        _appending_cards = [cards[_index-i] for i in range(0,3)]
                        remaining_cards = add_to_mean_cards(_appending_cards)
                        _index -= 3
                        remaining_three-=1
                        continue
                else:
                    remaining_cards = add_to_mean_cards([cards[_index], ])
                _index -= 1
                
        if hand == FOUR_OF_A_KIND:
            remaining_four = 1
            _index = len(cards) - 1
            while remaining_cards > 0 and _index>=0:
                #print cards[_index]
                kind = cards[_index].kind
                if remaining_four:
                    if remaining_cards > 4:
                        if kind_list[kind] < 4:
                            remaining_cards = add_to_mean_cards([cards[_index], ])
                    if kind_list[kind] >= 4:
                        _appending_cards = [cards[_index-i] for i in range(0, 4)]
                        remaining_cards = add_to_mean_cards(_appending_cards)
                        _index -= 4
                        remaining_four-=1
                        continue
                else:
                    remaining_cards = add_to_mean_cards([cards[_index], ])
                _index -= 1
                
        if hand == FULL_HOUSE:
            remaining_three = 1
            remaining_pair = 1
            _index = len(cards) - 1
            while remaining_cards > 0 and _index>=0:
                #print cards[_index]
                kind = cards[_index].kind
                if remaining_three:
                    if kind_list[kind] == 3:
                        _appending_cards = [cards[_index-i] for i in range(0,3)]
                        remaining_cards = add_to_mean_cards(_appending_cards)
                        _index-=3
                        remaining_three-=1
                        continue
                    elif kind_list[kind] == 2:
                        if remaining_pair:
                            remaining_cards = add_to_mean_cards([cards[_index], cards[_index-1]])                            
                            _index-=2
                            remaining_pair-=1
                            continue
                else:
                    if remaining_pair:
                        if kind_list[kind] >=2:
                            remaining_cards = add_to_mean_cards([cards[_index], cards[_index-1]])
                            _index-=2
                            remaining_pair-=1
                            continue
                _index -= 1
        
        have_flush = False
        for suit in suit_list.keys():
            if suit_list[suit] >= 5:
                have_flush = True 
                hand = max(hand, FLUSH)
                    #mean_cards = []
                #flush_suit = suit
        if have_flush:
            """straight flush detection"""
            flush_cards = []
            for _index in range(len(cards)):
                suit = cards[_index].suit
                if suit_list[suit] >= 5:
                    flush_cards.append(cards[_index])
            last_kind = flush_cards[-1].kind
            has_ace_in_flush = (last_kind == 14)
            seq = 1
            for _index in range(len(flush_cards)-2,-1,-1):
                kind = flush_cards[_index].kind
                if last_kind - kind == 1:
                    seq +=1
                elif last_kind - kind > 1:
                    seq = 1
                if seq == 5:
                    hand = STRAIGHT_FLUSH
                    mean_cards =[]
                    for k in range(_index, _index+5):
                        mean_cards.insert(0,flush_cards[k])
                    break
                if seq == 4:
                    if kind == 2 and has_ace_in_flush:
                        """Case: A 2 3 4 5"""
                        hand = STRAIGHT_FLUSH
                        mean_cards = []
                        mean_cards.append(flush_cards[-1])
                        for k in range(_index, _index+4):
                            mean_cards.insert(0,flush_cards[k])
                        break
                last_kind = kind
                
        if hand == STRAIGHT:
            mean_cards = []
            seq = 1
            last_kind = cards[-1].kind
            has_ace = last_kind == 14
            for _index in range(len(cards)-2,-1,-1):                
                kind = cards[_index].kind
                if last_kind - kind == 1:
                    seq +=1
                elif last_kind - kind >1:
                    seq = 1
                if seq == 5:
                    mean_cards.insert(0,cards[_index])
                    k = _index+1
                    count_forward = 4
                    prev_kind = kind
                    while count_forward >0:
                        kind2 = cards[k].kind
                        if kind2 - prev_kind == 1:                            
                            mean_cards.insert(0,cards[k])
                            count_forward -=1
                        k+=1
                        prev_kind = kind2
                    break
                if seq == 4:
                    if has_ace and (kind == 2):                    
                        mean_cards.insert(0, cards[-1])
                        mean_cards.insert(0,cards[_index])
                        k = _index+1
                        count_forward = 3
                        prev_kind = kind
                        while count_forward >0:
                            kind2 = cards[k].kind
                            if kind2 - prev_kind == 1:                            
                                mean_cards.insert(0,cards[k])
                                count_forward -=1
                            k+=1
                            prev_kind = kind2
                        break
                last_kind = kind
                                
        if hand == FLUSH:
            mean_cards = []
            remaining_cards = 5
            for _index in range(len(cards)-1,-1,-1):
                suit = cards[_index].suit
                if suit_list[suit] >= 5:
                    mean_cards.append(cards[_index])
                    remaining_cards-=1
                if remaining_cards == 0:
                    break

        self.hand = hand
        mean_cards.sort()
        self.mean_cards = mean_cards
        
    
    def __cmp__(self, other):
        """compare other hand"""
        if self.hand != other.hand:
            return self.hand - other.hand
        else:
            """
            same hand, so sort first, then compare from highest to lowest
            sorting priority: number of a kind, then value
            """                                
            def get_this_cmp_value(card):
                kind = card.kind
                return card.compare_value + (self._kind_list[kind] - 1) * 100

            def get_other_cmp_value(card):
                kind = card.kind
                return card.compare_value + (other._kind_list[kind] - 1) * 100                
            
            this_mean_cards = copy.copy(self.mean_cards)
            other_mean_cards = copy.copy(other.mean_cards)
            this_mean_cards.sort(key=get_this_cmp_value)
            other_mean_cards.sort(key=get_other_cmp_value)
            
            result = 0
            for j in range(len(this_mean_cards)-1,-1,-1):
                thiskind = this_mean_cards[j].kind
                otherkind = other_mean_cards[j].kind
                result = thiskind - otherkind
                if result != 0:
                    break
            return result