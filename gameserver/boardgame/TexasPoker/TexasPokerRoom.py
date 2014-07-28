'''
Created on May 5, 2014

@author: leen
'''
import copy
from boardgame.utils.Room import Room, STATUS_WAITING, STATUS_PLAYING
from boardgame.utils.Deck import Deck
#from pypoker.PokerCard import PokerCard
#from pypoker.PokerHand import PokerHand
from pypoker.helper.poker import get_PokerHand_from_list
from itertools import cycle
import logging
LOGGER = logging.getLogger('gamedebug')

ACTION_CHECK = 0x01
ACTION_CALL = 0x02
ACTION_RAISE = 0x03
ACTION_FOLD = 0x04
ACTION_COMPLETED = 0x00

STATUS_PREFLOP = 0x100
STATUS_FLOP = 0x101
STATUS_TURN = 0x102
STATUS_RIVER = 0x103
STATUS_SHOWDOWN = 0x104

def get_card_value(value):
        number_value = (value / 4) + 1
        suit_value = value % 4
        return (number_value, suit_value)

def str_tl_value(value):
    number, kind = get_card_value(value)
    skind_list = ['Bi','Ch','Ro','Co']
    skind = skind_list[kind]
    snumber_list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    snumber = snumber_list[number-1]
    res = snumber + '_'+skind + '_'+ '[' + str(value) + ']'
    return res

def str_tl_list(cards):
    res = ' '.join([str_tl_value(c) for c in cards])
    return res

class TwoPlayerTexasPokerRoom(Room):
    """The rule is limit hold'em head 2 head.
    When only two players remain, special 'head-to-head' or 'heads up' rules are enforced 
    and the blinds are posted differently.
    The person with the dealer button posts the small blind,
    while his/her opponent places the big blind.
    The dealer acts first before the flop. 
    After the flop, the dealer acts last and continues to do so for the remainder of the hand.    
    In limit hold 'em, bets and raises during the first two rounds of betting 
    (pre-flop and flop) must be equal to the big blind; 
    this amount is called the small bet. 
    In the next two rounds of betting (turn and river), 
    bets and raises must be equal to twice the big blind; 
    this amount is called the big bet. 
    """
    MAX_PLAYER = 2
    MINIMUM_BET = 10
    INIT_STAKE = 100
    
    def __init__(self, room_status, game):  
        super(TwoPlayerTexasPokerRoom, self).__init__(room_status, game)               
        self.user_playing_list = self._room_status.user_playing_list
        self.user_round_list = self._room_status.user_round_list
        if not self._room_status.big_blind_amount:
            self._room_status.big_blind_amount = self.MINIMUM_BET
        if not self._room_status.betting_money:
            self._room_status.betting_money = self.INIT_STAKE            
        #self._pot = 0
        
    def start_game(self):
        super(TwoPlayerTexasPokerRoom, self).start_game()
        self._room_status.user_playing_list = copy.copy(self._room_status.user_list)
        self._room_status.user_round_list = copy.copy(self._room_status.user_list)
        self.user_playing_list = self._room_status.user_playing_list
        self.user_round_list = self._room_status.user_round_list               
        self._init_player_stakes()
        self._preflop_round()
        
    def _preflop_round(self):
        LOGGER.debug('Preflop round')        
        self._room_status.user_playing_list = copy.copy(self._room_status.user_list)
        self._room_status.user_round_list = copy.copy(self._room_status.user_list)
        self.user_playing_list = self._room_status.user_playing_list
        self.user_round_list = self._room_status.user_round_list
        for player_name in self._room_status.user_playing_list:
            player = self._game.get_player(player_name)
            player.clear_card_set()
        self._room_status.playing_status = STATUS_PREFLOP
        #self._room_status.pot_contribution = dict()
        self._room_status.deck = Deck()
        self._init_pot_contribution()
        self._setup_position()
        self._init_player_round_bet()
        self._blind_bet()
        self._deal_preflop()        
        self._get_first_act_player()
        
    def _flop_round(self):
        self._room_status.playing_status = STATUS_FLOP
        self._deal_flop()
        
    def _turn_round(self):
        self._room_status.playing_status = STATUS_TURN
        self._deal_turn()
        
    def _river_round(self):
        self._room_status.playing_status = STATUS_RIVER
        self._deal_river()
        
    def _next_round(self):        
        status = self._room_status.playing_status
        if status not in [STATUS_PREFLOP, STATUS_FLOP, STATUS_TURN, STATUS_RIVER]:
            return
        if status == STATUS_PREFLOP:
            self._flop_round()
        elif status == STATUS_FLOP:
            self._turn_round()
        elif status == STATUS_TURN:
            self._river_round()
        elif status == STATUS_RIVER:
            self._show_down()
        self._init_player_round_bet()
        if not self._is_complete_round():
            self._get_first_act_player()
        else:
            self._next_round()
        self._action_if_game_finish()
        
    def _deal_preflop(self):
        LOGGER.debug('Deal Pre-flop')
        self._room_status.saving_cards = []
        player_username = self._get_next_playing_user(self._room_status.dealer)
        for _ in range(len(self.user_playing_list)*2):
            card = self._room_status.deck.get_card()
            player = self._game.get_player(player_username)
            player.receive_card(card)
            player_username = self._get_next_playing_user(player_username)
                    
        for player_username in self._room_status.user_playing_list:
            player = self._game.get_player(player_username)
            #player.get_card_set().sort()
            LOGGER.debug(str(player) + ' received '+ str_tl_list(player.get_card_set())) 
            self._msg_delivery.send_deal_card(player, player.get_card_set())
    
    def _deal_flop(self):
        cards = [self._room_status.deck.get_card() for _ in range(3)]
        self._msg_delivery.broadcast_deal_community_cards(cards)
        self._room_status.saving_cards += cards
        
    def _deal_turn(self):
        cards = [self._room_status.deck.get_card(),]
        self._msg_delivery.broadcast_deal_community_cards(cards)
        self._room_status.saving_cards += cards
    
    def _deal_river(self):
        return self._deal_turn()
    
    def _show_down(self):
        self._room_status.playing_status = STATUS_SHOWDOWN
        for player_name in self._room_status.user_round_list:
            player = self._game.get_player(player_name)
            self._msg_delivery.broadcast_user_submit_cards(player, player.get_card_set())
    
    def _get_first_act_player(self):
        if self._room_status.playing_status == STATUS_PREFLOP:
            if len(self.user_playing_list) == 2:
                self._room_status.current_player = self._room_status.dealer
            elif len(self.user_playing_list) > 2:
                player = self._get_next_playing_user(self._room_status.big_blind, is_active = True)
                self._room_status.current_player = player
            self.broad_cast_current_player()
        elif self._room_status.playing_status in [STATUS_FLOP, STATUS_TURN, STATUS_RIVER]:
            player = self._get_next_playing_user(self._room_status.dealer, is_active = True)
            self._room_status.current_player = player
            self.broad_cast_current_player()
    
    def action_bet(self, action, player, bet_money=None):
        result = False
        if action == "raise":
            result = self.raise_bet(player, bet_money)
        elif action == "call":
            result = self.call_bet(player)
        elif action == "check":
            result = self.check_bet(player)
        elif action == "fold":
            result = self.fold_hand(player)
        if result:
            player.update_active_time()
            if self._is_complete_round():
                if self._is_complete_game():
                    self._action_if_game_finish()
                else:
                    self._next_round()
        
    def raise_bet(self, player, bet_money):
        """limit hold'em rule"""
        player_name = str(player)
        if player_name != self._room_status.current_player:
            return False
        bet_money = self._check_fixed_limit_raise_rule(player_name, bet_money)
        if bet_money:
            self._room_status.player_round_bet[player_name] += bet_money
            self._room_status.pot_contribution[player_name] += bet_money
            self._room_status.player_stakes[player_name] -= bet_money
            self._room_status.current_bet = self._room_status.player_round_bet[player_name]
            self._msg_delivery.broadcast_poker_bet(player_name, bet_money, action="raise")
            self._room_status.player_actions[player_name] = "raise"
            self._switch_to_next_player(player_name)
            return True
        return False
    
    def _check_fixed_limit_raise_rule(self, player, bet_money):        
        if (self._room_status.playing_status == STATUS_PREFLOP) \
            or (self._room_status.playing_status == STATUS_FLOP):
            player_bet_round = self._room_status.player_round_bet[player] + bet_money
            diff_amount = player_bet_round - self._room_status.current_bet
            amount = min(self._room_status.player_stakes[player], self._room_status.big_blind_amount)
            if diff_amount == amount:
                return min(bet_money, self._room_status.player_stakes[player])
        if (self._room_status.playing_status == STATUS_TURN) \
            or (self._room_status.playing_status == STATUS_RIVER):
            player_bet_round = self._room_status.player_round_bet[player] + bet_money
            diff_amount = player_bet_round - self._room_status.current_bet
            amount = min(self._room_status.player_stakes[player], self._room_status.big_blind_amount * 2)
            if diff_amount == amount:
                return min(bet_money, self._room_status.player_stakes[player])
        return 0
    
    def call_bet(self, player):        
        player_name = str(player)
        if player_name != self._room_status.current_player:
            return False
        diff_amount = self._room_status.current_bet - self._room_status.player_round_bet[player_name]
        diff_amount = min(diff_amount, self._room_status.player_stakes[player_name])
        if diff_amount > 0:
            self._room_status.player_round_bet[player_name] += diff_amount
            self._room_status.pot_contribution[player_name] += diff_amount
            self._room_status.player_stakes[player_name] -= diff_amount
            self._msg_delivery.broadcast_poker_bet(player_name, diff_amount, action="call")
            self._room_status.player_actions[player_name] = "call"
            self._switch_to_next_player(player_name)
            return True
        return False
    
    def check_bet(self, player):
        player_name = str(player)
        if player_name != self._room_status.current_player:
            return False
        if self._room_status.current_bet == None:
            self._room_status.player_round_bet[player_name] = 0
            self._msg_delivery.broadcast_poker_bet(player_name, 0, action="check")
            self._room_status.player_actions[player_name] = "check"
            self._switch_to_next_player(player_name)
            return True
        else:
            if (self._room_status.player_round_bet[player_name] == self._room_status.current_bet):                
                self._msg_delivery.broadcast_poker_bet(player_name, 0, action="check")
                self._room_status.player_actions[player_name] = "check"
                self._switch_to_next_player(player_name)
                return True
        return False
    
    def fold_hand(self, player):
        player_name = str(player)
        if player_name in self.user_round_list:
            self._msg_delivery.broadcast_poker_fold(player_name)            
            if player_name == self._room_status.current_player:
                if len(self.user_round_list)>2:
                    self._switch_to_next_player(player_name)
            self.user_round_list.remove(player_name)
            self._room_status.player_actions[player_name] = "fold"
            #self._action_if_game_finish()
            return True
        return False
    
    def broad_cast_current_player(self):
        self._msg_delivery.broadcast_user_turn(self._room_status.current_player)
    
    def _switch_to_next_player(self, player_name):
        if not self._is_complete_round():
            self._room_status.current_player = self._get_next_playing_user(player_name, is_active=True)
            self.broad_cast_current_player()
        
    def _is_complete_game(self):
        return len(self.user_round_list) <= 1 or self._room_status.playing_status == STATUS_SHOWDOWN    
    
    def _is_complete_round(self):
        """all players fold, round complete obviously"""
        if len(self.user_round_list)<=1:
            return True
        """check whether all players are all-in"""
        count = 0
        all_in = False
        for player in self.user_round_list:
            if self._is_all_in(player):
                count +=1
        if count >= len(self.user_round_list)-1:
            all_in = True
            for player in self.user_round_list:
                if not self._is_all_in(player):
                    if self._room_status.player_round_bet[player] < self._room_status.current_bet:
                        all_in = False
                        break
            return all_in
        """check whether big blind in preflop round has bet"""
        #if self._room_status.playing_status == STATUS_PREFLOP:
        #    if self._room_status.player_actions[self._room_status.big_blind] == None:
        #        return False
        """check whether everybody has action"""
        for player in self.user_round_list:
            if self._room_status.player_actions[player] == None:
                return False            
            
        """check whether all players is calling same amount"""
        a_money = self._room_status.player_round_bet[self.user_round_list[0]]
        if a_money == None:
            return False        
        is_same = True
        for player in self.user_round_list:
            if (a_money != self._room_status.player_round_bet[player]):
                if not self._is_all_in(player):
                    is_same = False
                    break          
        return is_same
    
    def _is_all_player_same_bet(self):
        same = True
        a_money = self._room_status.player_round_bet[self.user_round_list[0]]
        for player in self.user_round_list:
            if (a_money != self._room_status.player_round_bet[player]):
                same = False
                break
        return same     
    
    def _is_all_in(self, player):
        return (self._room_status.player_stakes[player] <= 0)
        #return self._room_status.player_round_bet[player] >= self._room_status.player_stakes[player]
                
    def _get_pot(self):
        pot = 0
        for player in self._room_status.pot_contribution:
            pot += self._room_status.pot_contribution[player]
        self._pot = pot
        return pot
    
    def _blind_bet(self):
        self._room_status.player_stakes = self._room_status.player_stakes
        small_blind_amount = min(self._room_status.big_blind_amount / 2, self._room_status.player_stakes[self._small_blind])
        self._room_status.pot_contribution[self._small_blind] = small_blind_amount            
        self._room_status.player_round_bet[self._small_blind] = small_blind_amount
        self._room_status.player_stakes[self._small_blind] -= small_blind_amount
        self._msg_delivery.broadcast_poker_bet(self._small_blind, small_blind_amount, action="small_blind")
        
        big_blind_amount = min(self._room_status.big_blind_amount, self._room_status.player_stakes[self._room_status.big_blind])
        self._room_status.pot_contribution[self._room_status.big_blind] = big_blind_amount
        self._room_status.player_round_bet[self._room_status.big_blind] = big_blind_amount
        self._room_status.player_stakes[self._room_status.big_blind] -= big_blind_amount
        self._msg_delivery.broadcast_poker_bet(self._room_status.big_blind, big_blind_amount, action="big_blind")
        
        self._room_status.current_bet = max(small_blind_amount, big_blind_amount)    
        
    def _init_pot_contribution(self):
        self._room_status.pot_contribution = dict()
        for player in self.user_round_list:
            self._room_status.pot_contribution[player] = 0        
            
    def _init_player_round_bet(self):
        self._room_status.player_round_bet = dict()
        self._room_status.player_actions = dict()
        for player in self.user_round_list:
            self._room_status.player_round_bet[player] = 0
            self._room_status.player_actions[player] = None
        self._room_status.current_bet = 0    
        
    def _init_player_stakes(self):
        self._room_status.player_stakes = dict()
        self._room_status.player_actions = dict()
        for player in self.user_playing_list:
            self._room_status.player_stakes[player] = self._room_status.betting_money
            self._room_status.player_actions[player] = None
        self._broad_cast_stakes()
        LOGGER.debug(' '.join(['Init player stakes', str(self._room_status.betting_money)]))
    
    def _setup_position(self):
        self._setup_dealer()
        self._setup_small_blind()
        self._setup_big_blind()
    
    def _setup_dealer(self):
        if not self._room_status.dealer:
            dealer = self.user_playing_list[0]
        else:
            dealer = self._get_next_playing_user(self._room_status.dealer)
        self._room_status.dealer = dealer
        self._room_status.dealer = dealer
        return dealer    
    
    def _setup_big_blind(self):
        self._room_status.big_blind = self._get_next_playing_user(self._small_blind)        
        return self._room_status.big_blind
    
    def _setup_small_blind(self):
        if len(self.user_playing_list) == 2:
            self._small_blind = self._room_status.dealer
        elif len(self.user_playing_list) > 2:
            self._small_blind = self._get_next_playing_user(self._room_status.dealer)
        return self._small_blind
    
    def _get_next_playing_user(self, username, is_active=False):
        cycle_userlist = cycle(self._room_status.user_playing_list)
        found_user = None
        for _ in range(len(self._room_status.user_playing_list)):
            tmp_user = cycle_userlist.next()
            if tmp_user == username:
                    found_user = tmp_user
                    break
        if found_user:
            for _ in range(len(self._room_status.user_playing_list)):
                next_user = cycle_userlist.next()
                if not is_active:
                    return next_user
                else:
                    if next_user in self._room_status.user_round_list:
                        return next_user        
        return None
    
    def _action_if_game_finish(self):
        if self._is_complete_game():
            #for player in self._room_status.user_playing_list:
            winners = []            
            if len(self._room_status.user_round_list) == 1:
                winner = self._room_status.user_round_list[0]
                winners.append(winner)
            elif len(self._room_status.user_round_list) >= 2:
                poker_hands = dict()
                player_name = self._room_status.user_round_list[0]
                cards = self._game.get_player(player_name).get_card_set()
                max_hand = get_PokerHand_from_list(cards + self._room_status.saving_cards)
                poker_hands[player_name] = max_hand
                
                for player in self._room_status.user_round_list[1:]:
                    cards = self._game.get_player(player).get_card_set()
                    poker_hand = get_PokerHand_from_list(cards + self._room_status.saving_cards)
                    poker_hands[player] = poker_hand
                    max_hand = max(max_hand, poker_hand)
                    
                for player in poker_hands:
                    poker_hand = poker_hands[player]
                    if poker_hand == max_hand:
                        winners.append(player)
                    print player, poker_hand.mean_cards
            if winners:
                """this game only has 2 players, we will implement >2 players in the future"""
                total_pot = self._get_pot()
                if len(winners) == 1:
                    winner = winners[0]
                    self._room_status.player_stakes[winner] += min(total_pot, self._room_status.pot_contribution[winner]*2)
                    if self._room_status.playing_status == STATUS_SHOWDOWN:
                        mean_cards = [card.value for card in poker_hands[winner].mean_cards]
                        self._msg_delivery.broadcast_poker_winner(winner, mean_cards)                    
                elif len(winners) == 2:
                    """return money"""
                    for winner in winners:
                        self._room_status.player_stakes[winner] += self._room_status.pot_contribution[winner]
                        if self._room_status.playing_status == STATUS_SHOWDOWN:
                            mean_cards = [card.value for card in poker_hands[winner].mean_cards]
                            self._msg_delivery.broadcast_poker_winner(winner, mean_cards)
            self._broad_cast_stakes()
            LOGGER.debug('Completed a game.')
            #print self._room_status.pot_contribution
            #print self._room_status.player_stakes
            """give all player 10 seconds extra time"""
            for player_username in self._room_status.user_list:
                player = self._game.get_player(player_username)
                if player:
                    player.delay_active_time(10)
            if not self._is_eliminated():
                """continue game"""
                self._preflop_round()
                #self.stop_game()
                #self.start_game()
            else:
                self.stop_match()
    
    def _broad_cast_stakes(self):
        for player in self._room_status.user_playing_list:
            self._msg_delivery.broadcast_poker_stake(player, self._room_status.player_stakes[player])            
    
    def _is_eliminated(self):
        for player in self._room_status.user_playing_list:
            if self._room_status.player_stakes[player] <= 0:
                return True
        return False
    
    def join(self, player):
        """auto start game if there are 2 players in room"""
        if super(TwoPlayerTexasPokerRoom, self).join(player):
            if len(self._room_status.user_list) == self.MAX_PLAYER:
                self.start_game()
    
    def stop_match(self):
        self.stop_game()
        busted = []
        for player in self._room_status.user_playing_list:
            if self._room_status.player_stakes[player] <= 0:
                busted.append(player)
        self._msg_delivery.broadcast_poker_busted_list(busted)
        self._msg_delivery.broadcast_poker_stop_match()
    
    def part(self,player):
        player_username = str(player)
        playing_status = self._room_status.playing_status
        user_list = self._room_status.user_list
        if player_username in user_list:
            if playing_status == STATUS_WAITING:
                for _name in user_list:
                    _tmp_player = self.game_get_player(_name)
                    if _tmp_player.is_ready():
                        _tmp_player.update_active_time()
                        self.unready(_tmp_player)                                
            
            if playing_status >= STATUS_PLAYING:
                self._give_up(player)
                self.update_time_all()
            self._msg_delivery.broadcast_part(player)
            player.update_unready_status() 
            user_list.remove(player_username)                            
            player.set_current_room(None)
            player.clear_card_set()
            LOGGER.debug(str(player) + ' part '+str(self))
            if not user_list:
                self._game.close_room(self._room_status.id)            
            self._msg_delivery.broadcast_user_list()
            player.update_active_time()
            return True            
        return False
        
    def _give_up(self, player):
        player_username = str(player)
        if player_username in self._room_status.user_round_list:
            self._room_status.user_round_list.remove(player_username)
        self._room_status.player_stakes[player_username] = 0
        self._action_if_game_finish()
    