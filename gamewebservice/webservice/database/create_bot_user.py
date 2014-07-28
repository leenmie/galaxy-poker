'''
Created on Oct 7, 2012

@author: leen
'''
import random
from webservice.tools.utils import random_string_generator

NAME_LENGTH_RANGE = xrange(5, 12)

class RandomName():
    """
    This class generate random names from data in a input file.
    """
    def __init__(self, data_filename):
        """
        need a data text file 
        """
        f = open(data_filename, 'r')
        self._data = f.read()
        f.close()
        self._generate_grammar(self._data)
        
        
    def _generate_grammar(self, data):
        """
        generate a grammar from a input string
        """
        words = data.split()
        print len(words)
        self._first_letter = []
        self._next_letter = {}
        for w in words:
            if w:
                if w[0] not in self._first_letter:
                    self._first_letter.append(w[0])
                for _i in xrange(0, len(w)-1):
                    _char = w[_i]
                    if _char not in self._next_letter:
                        self._next_letter[_char] = [w[_i+1]]
                    else:
                        self._next_letter[_char].append(w[_i+1])
    
    
    def generate_name(self):
        """
        generate a random name
        """
        result = ''
        name_len = random.choice(NAME_LENGTH_RANGE)
        first_char = random.choice(self._first_letter)
        result = result + first_char
        cur_char = first_char
        for _ in range(0,name_len-1):
            next_char = random.choice(self._next_letter[cur_char])
            result = result + next_char
            cur_char = next_char
        return result

if __name__ == '__main__':
    list_name = []
    randomname = RandomName('name_latin.txt')
    for _ in range(1000):
        while True:
            _name = randomname.generate_name()
            if _name not in list_name:
                list_name.append(_name)
                break
    f_out = open('userlist.txt','w')
    for _name in list_name:
        _password = random_string_generator(20)
        f_out.write(_name + ' ' + _password + '\n')
    f_out.close()
        