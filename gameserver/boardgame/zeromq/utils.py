'''
Created on Mar 1, 2012

@author: leen
'''

import cPickle
from boardgame.utils.Message import Message

def find_destination_game_host(msg):
    message = cPickle.loads(msg)
    from_user = message.get_from_user()
    #from_user = clean_username(from_user)
    print from_user    
    return 'localhost'