#import cPickle
import json
import logging
from boardgame.utils.Room import Room
from boardgame.utils.RoomList import RoomList
from boardgame.utils.Player import Player, PlayerList
from boardgame.utils.Message import Message
from boardgame.utils.GameProcessor import InputProcessor
#from boardgame.models.couchbase_connector import CouchBaseConnector, MemcacheConnector
from boardgame.zeromq.MsgQueue_Game import MsgQueue_Game
from boardgame.utils.MongoConnector import Mongo_UserInfo_Connector, Mongo_Guest_UserInfo_Connector
from twisted.internet import reactor, defer
from boardgame.main_config import USE_TIMEOUT, TAX_RATE

LOGGER = logging.getLogger('gamedebug')

CLEAN_UP_TIME = 5

class Game(object):
    
    def __init__(self):
        self._database = Mongo_UserInfo_Connector()
        self._guest_database = Mongo_Guest_UserInfo_Connector()        
        self._room_list = RoomList(self)                        
        self._msg_queue = MsgQueue_Game()
        self._thread_input = None
        self._thread_output = None
        self._running = False
        self._cached_message = dict()
        self._player_list = PlayerList(self)        
        self.get_player = self._player_list.get_player                
    
    def get_database(self):
        return self._database
    
    def get_guest_database(self):
        return self._guest_database
            
    def get_player_money(self, username):
        pass
    
    def get_player_vip_money(self, username):
        pass
        
    def get_room(self, room_id):
        room_status = self._room_list.get_room(room_id)
        if room_status:            
            return Room(room_status, self)
        return None
    
    def get_random_available_room(self, betting_money, limit_money=None):
        room = self._room_list.get_random_available_room(betting_money, limit_money)
        if room:            
            return Room(room, self)
        return None        

    def close_room(self, room_id):
        self._room_list.close_room(room_id)
    
    def update_room(self, room_status):        
        self._room_list.update_room(room_status)
    
    def get_room_list(self):        
        return self._room_list    
    
    def get_input_queue(self):
        return self._msg_queue
    
    def get_output_queue(self):
        return self._msg_queue
    
    def send_output(self, player, str_message, commit=False):
        if self._running:
            username = str(player)
            if self._cached_message.has_key(username):
                self._cached_message[username].append(str_message)
            else:
                self._cached_message[username] = [str_message,]            
            if commit:
                self.commit_output()
        else:
            pass
            #print 'Output is not running.'
    def send_JSON_output(self, player, json_message, commit=False):
        """accept a dict as a json message and convert to json string, then send"""
        str_message = json.dumps(json_message)
        if self._running:
            username = str(player)
            if self._cached_message.has_key(username):
                self._cached_message[username].append(str_message)
            else:
                self._cached_message[username] = [str_message,]            
            if commit:
                self.commit_output()
        else:
            pass    
    
    def commit_output(self):
        for key in self._cached_message.keys():
            message_body = '\n'.join(self._cached_message[key])
            msg = {"from_user":key, "body":message_body}
            data = json.dumps(msg)
            self._msg_queue.send(data) 
        self._cached_message = dict()
        
    def transfer_money(self, amount, from_username, to_username):    
        from_player = self.get_player(from_username)
        to_player = self.get_player(to_username)
        amount_transfer = 0
        if from_player and to_player:
            from_player_current_money = from_player.get_money()
            to_player_current_money = to_player.get_money()
            if amount <= from_player_current_money:
                amount_transfer = amount
            else:
                amount_transfer = from_player_current_money #all his remaining money
                LOGGER.warning(' '.join(['Not enough money to transfer from',from_username,'to',to_username]))
            from_player_new_money = from_player_current_money - amount_transfer
            to_player_new_money = to_player_current_money + amount_transfer - (amount_transfer * TAX_RATE)
            from_player.update_money(from_player_new_money)
            to_player.update_money(to_player_new_money)
            #self._broadcast_output(' '.join(['TRANSFER', str(amount_transfer), from_username,to_username]))
            LOGGER.debug(' '.join(['TRANSFER', str(amount_transfer), 'from', from_username,'to',to_username]))
        return amount_transfer
                
    def start(self):
        self._running = True
        th_input = InputProcessor(self)
        th_input.start()
        self._thread_input = th_input        
        #clean up process
        if USE_TIMEOUT:
            self.start_clean_up()        
        
    def start_clean_up(self, d = None):
        if not d:                    
            d = defer.Deferred()
        if self._running:
            self.clean_up_user()            
            reactor.callLater(CLEAN_UP_TIME, self.start_clean_up, d)            
        return d
                
    def clean_up_user(self):
        self._player_list.clean_up_player()
    
    def stop(self):
        if self._thread_input: self._thread_input.stop()
        self._msg_queue.stop()
        self._running = False
