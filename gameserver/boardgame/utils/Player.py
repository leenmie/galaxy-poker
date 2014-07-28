import time
import datetime
#import copy
import logging
import re
import boardgame.utils.Room
from boardgame.main_config import DEFAULT_FREE_MONEY, DEFAULT_FREE_MONEY_TIME

"""guestxxxxxx"""
REGEX_GUEST_USERNAME = re.compile('^(guest)')
LOGGER = logging.getLogger('gamedebug')
STATUS_UNREADY = 0x00
STATUS_READY = 0x01
STATUS_SUBMITTED = 0x02

MAX_IDLE_TIME_GAME = 30
MAX_IDLE_TIME_CONNECTION = 300
FREE_MONEY = DEFAULT_FREE_MONEY
FREE_MONEY_TIME_OUT = DEFAULT_FREE_MONEY_TIME

class PlayerList():
    
    def __init__(self, game):
        self._player_list = dict()        
        self._game = game
        self._database = self._game.get_database()
        self._guest_database = self._game.get_guest_database() 
            
    def _get_player_by_name(self, str_name):
        if self._player_list.has_key(str_name):
            player = self._player_list[str_name]
            return player
        return None
    
    def get_player(self, str_name):
        """
        always return a player instance, create if not exist
        """        
        #str_name = username.split('@')[0]
        player = self._get_player_by_name(str_name)
        player_database = self._database
        if REGEX_GUEST_USERNAME.match(str_name):
            player_database = self._guest_database
        if not player:
            is_exist = player_database.exist_user(str_name)
            LOGGER.debug('Finding user {}'.format(str_name))            
            if not is_exist:
                return None
            playerstatus = PlayerStatus(str_name)
            player = Player(playerstatus, self._game)
            self._player_list[str_name] = player
            LOGGER.debug('Add user {}'.format(str_name))                            
            self.give_free_money(str_name)                
        return player        
    
    def get_player_(self, str_name):
        """
        return a player instance, None if not exist
        """
        player = self._get_player_by_name(str_name)
        """
        should we need some authorization here???
        """
        if not player:
            is_exist = self._database.exist_user(str_name)
            LOGGER.debug('Finding user {}'.format(str_name))
            if not is_exist:
                player = None
            else:
                playerstatus = PlayerStatus(str_name)
                player = Player(playerstatus, self._game)
                self._player_list[str_name] = player                            
                self.give_free_money(str_name)                
        return player

    def give_free_money(self, username):
        if REGEX_GUEST_USERNAME.match(username):
            """only registered user have free money"""
            return
        _player = self._get_player_by_name(username)
        if _player:
            _player_status = _player.get_player_status()
            free_money_last_update = _player_status.free_money_last_update
            if not free_money_last_update: 
                free_money_last_update = self._database.get_user_free_money_last_update(username)
            if free_money_last_update:
                current_time = datetime.datetime.utcnow()
                if (current_time - free_money_last_update).total_seconds() >= FREE_MONEY_TIME_OUT:
                    result = self._database.give_free_money(username, FREE_MONEY, FREE_MONEY_TIME_OUT)
                    if result:                    
                        _player_status.money = FREE_MONEY
                        _player_status.free_money_last_update = current_time
                        LOGGER.debug('Give free money {0} to {1}'.format(FREE_MONEY, username))
            else:
                LOGGER.error('Cannot get free money update time.')
                return
    
    def clean_up_player(self):
        """
        Clean all inactive players
        """
        #LOGGER.debug('Clean up player')
        STATUS_PLAYING = boardgame.utils.Room.STATUS_PLAYING
        STATUS_WAITING = boardgame.utils.Room.STATUS_WAITING  
        keys = self._player_list.keys()
        for key in keys:      
            _player = self._player_list[key]
            if _player:
                current_time = time.time()
                playerstatus = _player.get_player_status()
                delta_time = current_time - playerstatus.active_time
                if (delta_time > MAX_IDLE_TIME_GAME) and (delta_time < MAX_IDLE_TIME_CONNECTION):
                    current_room_id = playerstatus.current_room
                    if current_room_id:
                        room = self._game.get_room(current_room_id)
                        if not room:
                            LOGGER.error(' '.join(['This player',str(_player),'hold record',current_room_id,'which is not existed.']))
                            continue
                        if (room.get_playing_status() == STATUS_PLAYING) and (room.get_current_player() == playerstatus.username):                                                                                 
                            room.part(_player)
                        elif (room.get_playing_status() == STATUS_WAITING) and (playerstatus.status == STATUS_UNREADY):
                            room.part(_player)                                                
                if delta_time > MAX_IDLE_TIME_CONNECTION:
                    current_room_id = playerstatus.current_room
                    if current_room_id:
                        room = self._game.get_room(current_room_id)
                        room.part(_player)                    
                    del self._player_list[key]
                    LOGGER.debug('Player '+ playerstatus.username +' has quit the game.')
                    

class PlayerStatus():
    def __init__(self, username):
        self.username = username
        self.status = STATUS_UNREADY
        self.card_set = [] #fix here
        self.current_room = None
        self.active_time = time.time()
        self.money = -1
        self.cash = -1
        self.total_cash = -1
        self.avatar = 0
        self.free_money_last_update = None
        self.nickname = ""
        self.ping_current_value = None
        self.last_ping = time.time()

class Player():    
    def __init__(self, playerstatus, game):
        self._playerstatus = playerstatus
        self._game = game
        self._database = self._game.get_database()
        if REGEX_GUEST_USERNAME.match(playerstatus.username):
            self._database = self._game.get_guest_database()
        self.pull_player_status()
    
    def pull_player_status(self):
        """
        update user's information from database
        """
        userinfo = self._database.exist_user(self._playerstatus.username)
        if userinfo:
            self._playerstatus.money = int(userinfo['money'])
            self._playerstatus.cash = int(userinfo['cash'])
            self._playerstatus.avatar = int(userinfo['avatar'])
            self._playerstatus.total_cash = int(userinfo['total_cash'])
            self._playerstatus.nickname = userinfo["nickname"]
        
    def get_player_status(self):
        self.pull_player_status()
        return self._playerstatus
            
    def get_avatar(self):
        return self._playerstatus.avatar
    
    def set_avatar(self, iAvatar):
        if isinstance(iAvatar, int):
            self._playerstatus.avatar = iAvatar
            self._database.update_user_avatar(self._playerstatus.username, iAvatar)
    
    def __str__(self):
        return self._playerstatus.username
    
    def parse_model(self, model):
        #self._username = model.username
        self._active_money = model.active_money
        self._deposit_money = model.deposit_money
        
    def get_money(self):
        return self._playerstatus.money
    
    def update_money(self, amount):
        amount = int(amount)
        result = False
        updated = None
        for _ in range(5):
            updated = self._database.update_user_money(self._playerstatus.username, self._playerstatus.money, amount)
            if updated:
                self._playerstatus.money = amount
                result = True
                break
        if updated == None:
            LOGGER.error('Cannot update money')
            raise(Exception('Cannot update money'))
        return result
    
    def get_current_room(self):
        return self._playerstatus.current_room        
    
    def set_current_room(self, room):
        self._playerstatus.current_room = room        
        
    def get_active_time(self):
        return self._playerstatus.active_time
    
    def get_status_ready(self):
        return self._playerstatus.status
    
    def update_active_time(self):
        self._playerstatus.active_time = time.time()
        
    def delay_active_time(self, seconds):
        """give player extra time"""
        self._playerstatus.active_time = time.time() + seconds
        
    def update_ready_status(self):
        self._playerstatus.status = STATUS_READY        
        
    def update_unready_status(self):
        self._playerstatus.status = STATUS_UNREADY
        
    def update_submitted_status(self):
        self._playerstatus.status = STATUS_SUBMITTED        
        
    def clear_card_set(self):
        del (self._playerstatus.card_set)[:]
        
    def receive_card(self, card):
        self._playerstatus.card_set.append(card)
        
    
    def remove_cards(self, cards):
        for card in cards:
            self._playerstatus.card_set.remove(card)
    
    def get_card_set(self):
        return self._playerstatus.card_set    
    
    def get_nickname(self):
        return self._playerstatus.nickname
        
    def is_ready(self):
        return (self._playerstatus.status == STATUS_READY)
    
if __name__=="__main__":
    count = 500000
    pl = PlayerList(None)
    cur = time.time()
    for _ in range(count):
        pl.get_player('test'+str(_))
    delta = time.time() - cur
    print 'Add speed:' ,count/delta
    cur = time.time()
    for _ in range(count):
        pl.get_player('test'+str(_))
    delta = time.time() - cur
    print 'Get speed:' ,count/delta