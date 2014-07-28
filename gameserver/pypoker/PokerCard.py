'''
Created on Apr 15, 2014

@author: leen
'''
class PokerCard():
    def __init__(self, value):
        """value: [0..51] represent for [A..K]"""
        if value < 0 or value > 51:
            raise Exception("Invalid Poker Value")
        self.value = value        
        self.kind, self.suit = self._get_card_value(value)
        self.compare_value = value
        if self.is_ace():
            self.compare_value += 52        
    
    def is_ace(self):
        return (self.value < 4)

    def _get_card_value(self, value):
        number_value = (value / 4) + 1
        if number_value < 2:
            """aces"""
            number_value = number_value + 13
        suit_value = value % 4
        return (number_value, suit_value)
        
    def __repr__(self):
        _kind = [str(i) for i in range(0, 11)] + ['J', 'Q', 'K', 'A']
        _suit = ['()', '<>', '*', '&']
        result = _kind[self.kind] + _suit[self.suit]
        return result
        
        
    def __cmp__(self, other):
        return self.compare_value - other.compare_value
    