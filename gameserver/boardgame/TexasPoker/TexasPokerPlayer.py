'''
Created on May 9, 2014

@author: leen
'''
import time

from boardgame.utils.Player import PlayerList
from boardgame.utils.Room import STATUS_PLAYING, STATUS_WAITING

MAX_IDLE_TIME_GAME = 35
MAX_IDLE_TIME_CONNECTION = 5 * 60

import logging
LOGGER = logging.getLogger('gamedebug')

class TexasPokerPlayerList(PlayerList):
    
    def clean_up_player(self):
        """
        Clean all inactive players
        """
        #LOGGER.debug('Total user: {}'.format(len(self._player_list)))
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
                        if (room.get_playing_status() >= STATUS_PLAYING) and (room.get_current_player() == playerstatus.username):                                                                                 
                            room.part(_player)
                        elif (room.get_playing_status() == STATUS_WAITING):
                            user_list = room.get_room_status().user_list
                            if len(user_list) >= 2:
                                room.part(_player)                                                
                if delta_time > MAX_IDLE_TIME_CONNECTION:
                    current_room_id = playerstatus.current_room
                    if current_room_id:
                        room = self._game.get_room(current_room_id)
                        room.part(_player)                    
                    del self._player_list[key]
                    LOGGER.debug('Player '+ playerstatus.username +' has quit the game.')
