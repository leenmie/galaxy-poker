'''
Created on Mar 12, 2012

@author: leen
'''
STATUS_UNREADY = 00
STATUS_READY = 01

class ModelPlayerBasic():
    
    def __init__(self):
        self.username = None
        #self.status = STATUS_UNREADY
        self.active_money = None
        self.deposit_money = None
        #self.card_set = SimplePointCardList()
        #self.current_room = None
        