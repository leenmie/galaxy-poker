'''
Created on May 5, 2014

@author: leen
'''
import random
from boardgame.utils.Room import RoomStatus

import logging
LOGGER = logging.getLogger('gamedebug')

class RoomList():
    """
    store all room status
    """    
    def __init__(self, game):
        self._room_list = dict()
        self._room_list_betting = dict()
        self._game = game
        
    def get_room(self, room_id):
        room = None
        if self._room_list.has_key(room_id):
            room = self._room_list[room_id]            
            #return room
        return room
    
    def new_room(self, betting_money):
        room_status = RoomStatus()
        room_status.betting_money = betting_money        
        if betting_money < 0:
            return None        
        self.add_room(room_status)
        LOGGER.debug('New room '+ str(room_status.id))        
        return room_status
    
    def add_room(self,room_status):        
        self._room_list[room_status.id] = room_status
        if self._room_list_betting.has_key(room_status.betting_money):
            self._room_list_betting[room_status.betting_money].append(room_status)
        else:
            self._room_list_betting[room_status.betting_money] = [room_status,]
        
    def close_room(self,room_id):
        if self._room_list.has_key(room_id):
            room_status = self._room_list[room_id]
            if self._room_list_betting.has_key(room_status.betting_money):
                listroom_betting = self._room_list_betting[room_status.betting_money]
                found = -1
                for _i in range(len(listroom_betting)):
                    if listroom_betting[_i].id == room_id:
                        found = _i
                        break
                if found >= 0:
                    del self._room_list_betting[room_status.betting_money][found]
                    if len(self._room_list_betting[room_status.betting_money]) == 0:
                        del self._room_list_betting[room_status.betting_money]
                    LOGGER.debug('Delete [{}] room.'.format(room_status.betting_money))
            else:
                LOGGER.error('Room [{}],id={} is not found to close'.format(room_status.betting_money,room_id))                                        
            del self._room_list[room_id]
            LOGGER.debug('Room {} closed.'.format(room_id))
        else:
            LOGGER.error('Room {} is not found to close'.format(room_id))
    
    def get_list(self):
        return self._room_list
    
    def get_game(self):
        return self._game    
    
    def get_random_available_room(self, betting_money, limit_money=None):
        room = None
        if betting_money <0:
            return None
        if limit_money:
            if limit_money < betting_money*3:
                return None
        if self._room_list_betting.has_key(betting_money):
            available_list = []
            for _r in self._room_list_betting[betting_money]:
                if self._is_available_room(_r):
                    available_list.append(_r)
            if available_list:                
                room = random.SystemRandom().choice(available_list)
            else:
                room = self.new_room(betting_money)
        else:
            room = self.new_room(betting_money)
        return room
         
    def update_room(self, room_status):
        if self._room_list.has_key(room_status.id):
            self._room_list[room_status.id] = room_status
    
    def _is_available_room(self, room_status):
        if len(room_status.user_list) < room_status.MAX_PLAYER:
            return True
        return False
