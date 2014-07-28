from boardgame.main_config import USE_ROOM_TYPE_LIST, ROOM_TYPE_LIST
from boardgame.processors.GenericProcessor import GenericProcessor
import logging
LOGGER = logging.getLogger('gamedebug')

class JoinProcessor(GenericProcessor):
    
    def _adhoc_check(self, betting_money):
        player_status = self._player.get_player_status()
        total_cash = player_status.total_cash
        required_cash = self._require_cash(betting_money)
        if total_cash < required_cash:
            self._game.send_output(self._player, {'command':'error', 'reason':' NOTENOUGHTOTALGOLD','amount': required_cash})
            return False
        return True
        
    def _require_cash(self, betting_money):
        if betting_money >100 and betting_money <=10e3:
            return 10
        if betting_money >10e3 and betting_money <= 20e3:
            return 20
        if betting_money >20e3 and betting_money <= 50e3:
            return 50
        if betting_money >50e3 and betting_money <= 100e3:
            return 100
        return 0
    
    def process(self):                
        #find all available room, get a random one
        _betting_money = 0
        try:
            _betting_money = int(self._arguments[0])
            #check value betting money
            #TO DO
        except:
            LOGGER.warning('Join invalid argument')
            return False
        if USE_ROOM_TYPE_LIST:
            if _betting_money not in ROOM_TYPE_LIST:
                self._game.send_output(self._player, 'INVALIDROOM')
                return False
        if _betting_money <= 0:
            return False
         
        current_room_id = self._player.get_current_room()
        if current_room_id:
            current_room = self._game.get_room(current_room_id)                
            current_room.part(self._player)            
            
        room = self._game.get_random_available_room(_betting_money, self._player.get_money())
        
        """some restriction before joining room"""
        if self._player.get_money() < _betting_money*3:
            self._game.send_JSON_output(self._player, {'command':'error', 'reason':' NOTENOUGHMONEY'})
            return True
        """no adhoc_check"""
        """
        adhoc_check = self._adhoc_check(_betting_money)
        if not adhoc_check:
            return True
        """
        
        #player join the room
        if room:
            res = room.join(self._player)
            #if res:
            #    self._game.set_route(str(self._player))            
        else:
            #self._game.send_output(self._player, 'JOIN 01')
            return False
        self._player.update_active_time()        
        #self._game.send_output(self._player, 'JOIN 00')        
        return True