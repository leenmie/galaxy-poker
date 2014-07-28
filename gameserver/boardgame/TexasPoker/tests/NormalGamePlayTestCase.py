'''
Created on May 6, 2014

@author: leen
'''
import unittest
import time
import logging.config
import json
from boardgame.TexasPoker.TexasPokerGame import TexasPokerGame 
from boardgame.utils.Message import Message
from boardgame.utils.MessageProcessor import JSONMessageProcessor
from boardgame.utils.Deck import Deck

def mix_card_set(cardset_list):
    """assuming cardsets have same length"""
    result_set = []
    for i in range(0, len(cardset_list[0])):
        for cardset in cardset_list:
            result_set.append(cardset[i])
    return result_set
        
class NormalGamePlayTestCase(unittest.TestCase):
    
    def setUp(self):
        self._game = TexasPokerGame()
        #self._game.start()            
    def tearDown(self):
        self._game.stop()
        time.sleep(0.1)
    
    def _process_message(self, username, command):
        message = Message(username,command)
        proc = JSONMessageProcessor(self._game)
        res = proc.process(message)
        self.assertTrue(res)
    
    def test_play_finish_1_game(self):
        username1 = 'onlylinh1'
        username2 = 'onlylinh2'
        #username3 = 'onlylinh3'
        #username4 = 'onlylinh4'
        
        command = {"command":'join', "arguments":[]}
        command_str = json.dumps(command)        
        self._process_message(username1, command_str)        
        self._process_message(username2, command_str)    
        
        command = {"command":'ready', "arguments":[]}
        command_str = json.dumps(command)        
        self._process_message(username1, command_str)        
        self._process_message(username2, command_str)  
                      
        command = {"command": 'bet', "arguments": {"action": "call"}}
        command_str = json.dumps(command)
        self._process_message(username1, command_str)
        command = {"command": 'bet', "arguments": {"action": "check"}}
        command_str = json.dumps(command)        
        self._process_message(username2, command_str)
        
        command = {"command": 'bet', "arguments": {"action": "check"}}
        command_str = json.dumps(command)
        self._process_message(username2, command_str)
        command = {"command": 'bet', "arguments": {"action": "check"}}
        command_str = json.dumps(command)
        self._process_message(username1, command_str)
        
        command = {"command": 'bet', "arguments": {"action": "check"}}
        command_str = json.dumps(command)
        self._process_message(username2, command_str)
        command = {"command": 'bet', "arguments": {"action": "check"}}
        command_str = json.dumps(command)
        self._process_message(username1, command_str)
        
        command = {"command": 'bet', "arguments": {"action": "check"}}
        command_str = json.dumps(command)
        self._process_message(username2, command_str)        
        command = {"command": 'bet', "arguments": {"action": "check"}}
        command_str = json.dumps(command)
        self._process_message(username1, command_str)

    def test_play_fold_1_game(self):
        username1 = 'onlylinh1'
        username2 = 'onlylinh2'
        #username3 = 'onlylinh3'
        #username4 = 'onlylinh4'
        
        command = {"command":'join', "arguments":[]}
        command_str = json.dumps(command)        
        self._process_message(username1, command_str)        
        self._process_message(username2, command_str)    
        
        command = {"command":'ready', "arguments":[]}
        command_str = json.dumps(command)        
        self._process_message(username1, command_str)        
        self._process_message(username2, command_str)  
                      
        command = {"command": 'bet', "arguments": {"action": "fold"}}
        command_str = json.dumps(command)
        self._process_message(username1, command_str)
        #command = {"command": 'bet', "arguments": {"action": "check"}}
        #command_str = json.dumps(command)        
        #self._process_message(username2, command_str)
        
    def test_play_raise_1_game(self):
        username1 = 'onlylinh1'
        username2 = 'onlylinh2'
        
        command = {"command":'join', "arguments":[]}
        command_str = json.dumps(command)        
        self._process_message(username1, command_str)        
        self._process_message(username2, command_str)    
        
        """command = {"command":'ready', "arguments":[]}
        command_str = json.dumps(command)        
        self._process_message(username1, command_str)        
        self._process_message(username2, command_str)  """
                      
        command = {"command": 'bet', "arguments": {"action": "raise", "amount": 15}}
        command_str = json.dumps(command)
        self._process_message(username1, command_str)
        
        command = {"command": 'bet', "arguments": {"action": "call"}}
        command_str = json.dumps(command)        
        self._process_message(username2, command_str)
        
        command = {"command": 'bet', "arguments": {"action": "raise", "amount": 10}}
        command_str = json.dumps(command)        
        self._process_message(username2, command_str)
        
        command = {"command": 'bet', "arguments": {"action": "raise", "amount": 20}}
        command_str = json.dumps(command)        
        self._process_message(username1, command_str)
        
        command = {"command": 'bet', "arguments": {"action": "call"}}
        command_str = json.dumps(command)        
        self._process_message(username2, command_str)
        
        command = {"command": 'bet', "arguments": {"action": "raise", "amount": 20}}
        command_str = json.dumps(command)        
        self._process_message(username2, command_str)
        
        command = {"command": 'bet', "arguments": {"action": "call"}}
        command_str = json.dumps(command)        
        self._process_message(username1, command_str)
        
        command = {"command": 'bet', "arguments": {"action": "fold"}}
        command_str = json.dumps(command)        
        self._process_message(username2, command_str)
        
        command = {"command": 'bet', "arguments": {"action": "raise", "amount": 15}}
        command_str = json.dumps(command)        
        self._process_message(username2, command_str)
        
        command = {"command": 'bet', "arguments": {"action": "raise", "amount": 20}}
        command_str = json.dumps(command)        
        self._process_message(username1, command_str)
        
        command = {"command": 'bet', "arguments": {"action": "call"}}
        command_str = json.dumps(command)        
        self._process_message(username2, command_str)
        
        command = {"command": 'bet', "arguments": {"action": "raise", "amount": 10}}
        command_str = json.dumps(command)        
        self._process_message(username1, command_str)
        
        command = {"command": 'bet', "arguments": {"action": "call"}}
        command_str = json.dumps(command)        
        self._process_message(username2, command_str)
        
        command = {"command": 'bet', "arguments": {"action": "raise", "amount": 10}}
        command_str = json.dumps(command)        
        self._process_message(username1, command_str)
        
        command = {"command": 'bet', "arguments": {"action": "call"}}
        command_str = json.dumps(command)        
        self._process_message(username2, command_str)
        
        command = {"command": 'bet', "arguments": {"action": "raise", "amount": 10}}
        command_str = json.dumps(command)        
        self._process_message(username1, command_str)
        
        command = {"command": 'bet', "arguments": {"action": "call"}}
        command_str = json.dumps(command)        
        self._process_message(username2, command_str)
        
        
    def test_join_and_part(self):
        username1 = 'onlylinh1'
        username2 = 'onlylinh2'
        username3 = 'onlylinh3'
        username4 = 'onlylinh4'
        username5 = 'ff380c89a7964d80b6c089ebb3c68a1e'        
        #username5 = 'fb+100005717430683@ubuntu'        
        
        
        command = {"command":'join', "arguments":[100]}
        command_str = json.dumps(command)        
        self._process_message(username1, command_str)        
        self._process_message(username2, command_str)
        self._process_message(username3, command_str)
        self._process_message(username4, command_str)
        
        
        command = {"command": 'part', "arguments":[]}      
        command_str_part = json.dumps(command)          
        self._process_message(username4, command_str_part)
        self._process_message(username5, command_str)
        
    def test_play_and_part(self):
        username1 = 'onlylinh1'
        username2 = 'onlylinh2'
        username3 = 'onlylinh3'
        username4 = 'onlylinh4'
        command = {"command":'join', "arguments":[100]}
        command_str = json.dumps(command)    
        self._process_message(username1, command_str)        
        self._process_message(username2, command_str)
        self._process_message(username3, command_str)        
        self._process_message(username4, command_str)
        
        cardset1 = [46,49,25,6,33,35,39,37,20,12,8,32,48]
        cardset2 = [24,34,40,17,3,1,4,9,44,45,47,14,15]
        cardset3 = [2,0,23,10,31,28,27,26,5,43,16,18,42]
        cardset4 = [51,50,41,36,38,29,30,22,13,7,11,19,21]
        
        card_list_test = mix_card_set([cardset1, cardset2, cardset3, cardset4])
        custom_deck = Deck()
        custom_deck.set_card_list(card_list_test)
        room_id = self._game.get_player(username1).get_current_room()
        room_instance = self._game.get_room(room_id)
        room_instance.debug_only_set_deck(custom_deck)
        
        command = {"command":'ready', "arguments":[]}
        command_str = json.dumps(command)
        
        self._process_message(username1, command_str)        
        self._process_message(username2, command_str)
        self._process_message(username3, command_str)        
        self._process_message(username4, command_str)
                
        command = {"command":'part', "arguments":[]}
        command_str = json.dumps(command)
        self._process_message(username3, command_str)
        
        command = {"command":'submit', "arguments": cardset1}
        command_str = json.dumps(command)
        self._process_message(username1, command_str)
        
        command = {"command":'submit', "arguments": cardset2}
        command_str = json.dumps(command)
        self._process_message(username2, command_str)
        
        #command = {"command":'submit', "arguments": cardset3}
        #command_str = json.dumps(command)
        #self._process_message(username3, command_str)
        
        command = {"command":'submit', "arguments": cardset4}
        command_str = json.dumps(command)
        self._process_message(username4, command_str)
        #self._process_message(username2, 'ready')        
        #self._process_message(username4, 'ready')
        
                                     
if __name__=="__main__":
    logging.config.fileConfig('../../../logging.conf')
    logging.disable(0)
    #unittest.main()
    widgetTestSuite = unittest.TestSuite()
    #widgetTestSuite.addTest(NormalGamePlayTestCase('test_play_finish_1_game'))
    #widgetTestSuite.addTest(NormalGamePlayTestCase('test_play_raise_1_game'))
    widgetTestSuite.addTest(NormalGamePlayTestCase('test_play_raise_1_game'))
    #widgetTestSuite.addTest(NormalGamePlayTestCase('test_join_and_part'))
    #widgetTestSuite.addTest(NormalGamePlayTestCase('test_play_and_part'))
    unittest.TextTestRunner(verbosity=2).run(widgetTestSuite)