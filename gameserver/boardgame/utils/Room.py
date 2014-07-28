import random
import uuid
import logging
import copy
from boardgame.utils.Deck import Deck
from boardgame.utils.Player import STATUS_READY, STATUS_UNREADY
from boardgame.utils.MessageDelivery import JSONMessageDelivery
from boardgame.main_config import TLROOM_CONFIG_ANONYMOUS
from itertools import cycle
#import numpy


LOGGER = logging.getLogger('gamedebug')
STATUS_WAITING = 0x00
STATUS_PLAYING = 0x01

class RoomStatus():
    """
    room status record
    """
    def __init__(self, room_id = None):
        if not room_id:
            room_id = uuid.uuid4().hex        
        self.id = room_id         
        self.betting_money = None        
        self.playing_status = STATUS_WAITING
        self.deck = None
        self.user_list = []
        self.MAX_PLAYER = 4
        self.current_player = None
        self.last_winner = None
        self.last_card_set = None
        self.winner_list = []
        self.user_playing_list = []
        self.user_round_list =[]
        self.saving_cards = []
        self.saving_all_cards = []
        self.debug = False
        self.configuration = None
        """poker"""
        self.current_bet = 0
        self.pot_contribution = dict()
        self.player_stakes = dict()
        self.player_round_bet = dict()
        self.player_actions = dict()
        self.dealer = None
        self.big_blind = None
        self.big_blind_amount = 0

class BaseRoom(object):
    MAX_PLAYER = 2
    
    game_get_player = None    
    def __init__(self, room_status, game):        
        self._room_status = room_status
        self._room_status.MAX_PLAYER = self.MAX_PLAYER
        self._game = game
        self.game_get_player = self._game.get_player
        self._msg_delivery = JSONMessageDelivery(self, game)
        #self._send_output = self._game.send_output            
                            
    def get_room_status(self):
        return self._room_status
        
    def __str__(self):
        return str(self._room_status.id)
    
    def _get_next_user(self, username):
        """
        find next user in user_list
        """
        cycle_userlist = cycle(self._room_status.user_list)
        found_user = None
        for _ in range(len(self._room_status.user_list)):
            tmp_user = cycle_userlist.next()
            if tmp_user == username:
                found_user = tmp_user
                break
        if found_user:
            next_user = cycle_userlist.next()
            return next_user        
        return None                        
            
    def is_available(self):        
        return (len(self._room_status.user_list) < self.MAX_PLAYER)
    
    def _is_ready_all(self):
        res = True
        userlist = self._room_status.user_list
        for player_username in userlist:
            #player = self._game.get_player(player_username)
            player = self.game_get_player(player_username)
            if not player.is_ready():
                res = False
                break        
        return (res and (len(userlist)>1))
    
    def get_user_list(self):
        return self._room_status.user_list

    def get_betting_money(self):
        return self._room_status.betting_money

    def get_current_player(self):
        return self._room_status.current_player
    
    def get_playing_status(self):
        return self._room_status.playing_status
    
    def get_id(self):
        return self._room_status.id
    
    def update_time_all(self):
        for _tmp_name in self._room_status.user_list:
            _tmp_player = self.game_get_player(_tmp_name)
            _tmp_player.update_active_time()            
    
    def _give_up(self, player):
        pass
    
    def close(self):
        pass
    

class Room(BaseRoom):
    """
    room instance
    """
    MAX_PLAYER = 4
    
    def join(self,player):
        user_list = self._room_status.user_list        
        if len(user_list) >= self.MAX_PLAYER:
            return False
        else:
            player_username = str(player)            
            user_list.append(player_username)
            player.set_current_room(self._room_status.id)
            LOGGER.debug(str(player) + ' join '+str(self))
            self._msg_delivery.broadcast_join(player)
            self._msg_delivery.send_game_status(player, self._room_status.playing_status)
            self._msg_delivery.broadcast_user_list()
            self._msg_delivery.broadcast_user_status()
            player.update_active_time()
            #self._game.commit_output()
            return True
    
    def part(self,player):
        player_username = str(player)
        playing_status = self._room_status.playing_status
        user_list = self._room_status.user_list
        if player_username in user_list:
            #player give up current game
            #self.update_time_all()
            if playing_status == STATUS_WAITING:
                for _name in user_list:
                    _tmp_player = self.game_get_player(_name)
                    if _tmp_player.is_ready():
                        _tmp_player.update_active_time()
                        self.unready(_tmp_player)                                
            
            if playing_status == STATUS_PLAYING:
                self._give_up(player)
                self.update_time_all()
            if self._room_status.last_winner == player_username:
                self._room_status.last_winner = self._get_next_user(self._room_status.last_winner)
                if not self._room_status.last_winner:
                    LOGGER.debug('get_next_user error!')
            #self._broadcast_output(' '.join(['PART',str(player)]))
            self._msg_delivery.broadcast_part(player)
            player.update_unready_status() 
            user_list.remove(player_username)                            
            #print self._user_list
            player.set_current_room(None)
            player.clear_card_set()
            LOGGER.debug(str(player) + ' part '+str(self))
            if not user_list:
                self._game.close_room(self._room_status.id)            
            #confusing herereee !!!
            self._msg_delivery.broadcast_user_list()
            #self._broadcast_user_list()
            player.update_active_time()
            return True            
        return False
    
    def emotion(self, player, e_id):
        player_username = str(player)
        userlist = self._room_status.user_list
        if player_username in userlist:
            self._msg_delivery.broadcast_user_emotion(player, e_id)
                
    def debug_only_set_deck(self, deck):
        self._room_status.deck = deck
        self._room_status.debug = True
            
    def start_game(self):        
        self._room_status.playing_status = STATUS_PLAYING
        self.update_time_all()
        LOGGER.debug(str(self) + ' started a game.')
        userlist = self._room_status.user_list
        for player_username in userlist:
            player = self.game_get_player(player_username)
            if player:
                player.update_unready_status()
                player.clear_card_set()
        self._msg_delivery.broadcast_start_game()    
        #init deck
        if not self._room_status.debug:
            self._room_status.deck = Deck()
        del self._room_status.saving_all_cards[:]                    
    
    def stop_game(self):
        self._room_status.playing_status = STATUS_WAITING
        self._room_status.debug = False
        self._msg_delivery.broadcast_stop_game()        
        LOGGER.debug(str(self) + ' stopped a game.')
    
    def ready(self, player):
        player_username = str(player)
        userlist = self._room_status.user_list
        if player_username in userlist:
            player.update_ready_status()
            LOGGER.debug(str(player)+ ' is ready')
            self._msg_delivery.broadcast_ready(player)
            player.update_active_time()
            if self._is_ready_all() and self._room_status.playing_status == STATUS_WAITING:
                self.start_game()
            
    def unready(self, player):
        player_username = str(player)
        userlist = self._room_status.user_list
        if player_username in userlist:
            player.update_unready_status()
            LOGGER.debug(str(player)+ ' is unready')
            self._msg_delivery.broadcast_unready(player)
            player.update_active_time()
        
    def unready_all(self):
        userlist = self._room_status.user_list
        for player_username in userlist:
            player = self.game_get_player(player_username)
            self.unready(player)
            