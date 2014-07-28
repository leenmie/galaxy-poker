'''
Created on Apr 4, 2012

@author: leen
'''
import json
class Command(object):
    '''
    Command object
    '''
    def __init__(self, code, param):
        self._code = code
        self._param = param
        
    def __repr__(self):
        json_dict = {'code':self._code,
                     'params': self._param}
        return json.dumps(json_dict)
    
if __name__ == '__main__':
    command = Command('hello', [1,2,3,4,5])
    print command