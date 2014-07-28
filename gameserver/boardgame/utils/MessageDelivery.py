'''
Created on May 17, 2013

@author: leen
'''
import logging
LOGGER = logging.getLogger('gamedebug')

class JSONMessageDelivery():
    def __init__(self, room, game):
        self._room = room
        self._game = game
        
    def _send_output(self, player, message):
        LOGGER.debug('Output: '+str([str(player), message]))
        return self._game.send_JSON_output(player, message)
    
    def _broadcast_output(self, str_msg, commit = False):
        userlist = self._room.get_user_list()
        for player in userlist:
            self._send_output(player, str_msg)
        if commit:
            self._game.commit_output()

    def broadcast_join(self, player):
        #player_instance = self._room.game_get_player(player)
        avatar_id = player.get_avatar()
        nickname = player.get_nickname()
        player_info = {"username": str(player), "avatar": avatar_id, "nickname": nickname}
        message = {"command": 'join', "player": player_info}
        self._broadcast_output(message)
        
    def broadcast_part(self, player):
        player_username = str(player)
        message = {"command": 'part', "player": player_username}
        self._broadcast_output(message, commit=True)
        
    def broadcast_user_list(self):
        userlist = self._room.get_user_list()
        player_list = []
        for player_username in userlist:
            player_instance = self._room.game_get_player(player_username)
            avatar_id = player_instance.get_avatar()
            nickname = player_instance.get_nickname()
            player_status = player_instance.get_status_ready()
            player_info = {"username": player_username, "avatar": avatar_id, "nickname":nickname, "readystatus": player_status}
            player_list.append(player_info)            
        message = {"command": 'userlist', "list": player_list}
        self._broadcast_output(message)
        
    def broadcast_user_status(self):
        userlist = self._room.get_user_list()
        result_list = []
        for player_username in userlist:
            player_instance = self._room.game_get_player(player_username)
            player_status = player_instance.get_status_ready()
            info = {"username": player_username, "status": player_status}
            result_list.append(info)
        message = {"command": 'readylist', "list": result_list}
        self._broadcast_output(message)
    
    def broadcast_user_emotion(self, player, emotion_id):
        message = {"command": 'emotion', "emotion_id": emotion_id, "player": str(player)}
        self._broadcast_output(message)
        
    def broadcast_start_game(self):
        betting_money = self._room._room_status.betting_money
        message = {"command": 'startgame', "betting_money": betting_money}
        self._broadcast_output(message)
    
    def broadcast_stop_game(self):
        message = {"command": 'stopgame'}
        self._broadcast_output(message)
        
    def broadcast_ready(self, player):
        message = {"command": 'ready', "player": str(player)}
        self._broadcast_output(message)
        
    def broadcast_unready(self, player):
        message = {"command": 'unready', "player": str(player)}
        self._broadcast_output(message)
        
    def broadcast_submit(self, player):
        message = {"command": 'submit', "player": str(player)}
        self._broadcast_output(message)
    
    def broadcast_giveup(self, player):
        message = {"command": 'giveup', "player": str(player)}
        self._broadcast_output(message)
    
    def broadcast_finish(self, player):
        message = {"command": 'finish', "player": str(player)}
        self._broadcast_output(message)
    
    def broadcast_imprison(self, player):
        message = {"command": 'imprison', "player": str(player)}
        self._broadcast_output(message)    
        
    def broadcast_special_hand(self, player):
        message = {"command": 'specialhand', "player": str(player)}
        self._broadcast_output(message)
        
    def broadcast_reveal_hands(self, saving_cards):
        message = {"command": 'reveal', "cards": saving_cards}
        self._broadcast_output(message)
        
    def broadcast_transfer_money(self, amount, from_username, to_username):
        message = {"command": 'transfer_money', "from": from_username,
                   "to": to_username, "amount": amount}
        self._broadcast_output(message)
        
    def broadcast_lucky_win(self, player_list):
        message = {"command": 'luckywin', "players": player_list}
        self._broadcast_output(message)
        
    def broadcast_start_round(self):
        message = {"command": 'startround'}
        self._broadcast_output(message)
            
    def broadcast_user_turn(self, player):
        message = {"command": 'turn', "player": str(player)}
        self._broadcast_output(message)
        
    def broadcast_user_pass(self, player):
        message = {"command": 'pass', "player": str(player)}
        self._broadcast_output(message)
        
    def broadcast_user_submit_cards(self, player, cards):
        message = {"command": 'submit', "player": str(player), "cards": cards}
        self._broadcast_output(message)
        
    def broadcast_deal_community_cards(self, cards):
        message = {"command": 'deal_community', "cards": cards}
        self._broadcast_output(message)        
        
    def broadcast_user_imprison(self, player):
        message = {"command": 'imprison', "player": str(player)}
        self._broadcast_output(message)
        
    def broadcast_user_penalty(self, player):
        message = {"command": 'penalty', "player": str(player)}
        self._broadcast_output(message)
        
    def broadcast_tl_winner_list(self, winner_list):
        message = {"command": 'winnerlist', "list": winner_list}
        self._broadcast_output(message)
    
    def broadcast_poker_bet(self, player, amount, action="call"):
        message = {"command": "bet", "player": str(player), "amount": amount, "action": action}
        self._broadcast_output(message)
        
    def broadcast_poker_fold(self, player):
        message = {"command": "fold", "player": str(player)}
        self._broadcast_output(message)
        
    def broadcast_poker_winner(self, player, cards):
        message = {"command": "winner", "player": str(player), "cards": cards}
        self._broadcast_output(message)
        
    def broadcast_poker_stake(self, player, stake):
        message = {"command": "stake", "player": str(player), "stake": stake}                
        self._broadcast_output(message)
        
    def broadcast_poker_stop_match(self):
        message = {"command": "stopmatch"}
        self._broadcast_output(message)
    
    def broadcast_poker_busted_list(self, busted_users):
        message = {"command": "busted", "list": busted_users}
        self._broadcast_output(message)
    
    def send_game_status(self, player, status):
        betting_money = self._room._room_status.betting_money
        message = {"command": 'gamestatus', "status": status, "betting_money": betting_money}
        self._send_output(player, message)
    
    def send_user_money(self, player):
        amount = player.get_money()
        message = {"command": 'money', "amount": amount}
        self._send_output(player, message)
        
    def send_deal_card(self, player, cardset):
        message = {"command": 'deal', "player": str(player), "card_set": cardset}
        self._send_output(player, message)
        
    def send_game_result(self, player, result):
        message = {"command": 'result', "result": result}
        self._send_output(player, message)
        
        