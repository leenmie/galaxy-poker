import logging
import traceback
import json

import boardgame.processors.JoinProcessor
import boardgame.processors.PartProcessor
import boardgame.processors.ReadyProcessor
import boardgame.processors.DebugDealProcessor
import boardgame.processors.AvatarProcessor
import boardgame.processors.ConvertCash2MoneyProcessor
import boardgame.processors.PingProcessor
import boardgame.processors.InfoProcessor

import boardgame.TexasPoker.processors.JoinProcessor
import boardgame.TexasPoker.processors.BetProcessor

#import boardgame.SimplePointGame.processors
LOGGER = logging.getLogger('gamedebug')

from Message import Message
from Player import Player
#from Game import Game

Processor_Mapper = {
                    'TexasPokerGame':{
                                        'ping': 'boardgame.processors.PingProcessor.PingProcessor',
                                        'join': 'boardgame.TexasPoker.processors.JoinProcessor.JoinProcessor',
                                        'part': 'boardgame.processors.PartProcessor.PartProcessor',
                                        'ready': 'boardgame.processors.ReadyProcessor.ReadyProcessor',
                                        'bet': 'boardgame.TexasPoker.processors.BetProcessor.BetProcessor',
                                        },                                            
                    }

class getProcessor():
    def __init__(self, mapper):        
        self._mapper = mapper
        self._processors = dict()
        for key in self._mapper.keys():
            self._processors[key] = eval(self._mapper[key])
    
    def get_processor(self, command):
        processor = None
        if self._processors.has_key(command):
            return self._processors[command]
        return processor

class bodyParser():
    """legacy parser, delimiter is space"""
    def __init__(self,body):
        self._body = body
        self._parse()
    
    def _parse(self):
        parts = self._body.split(" ")
        if len(parts)>0:
            self._command = parts[0]
        self._arguments = []
        if len(parts)>1:
            self._arguments = parts[1:]
    
    def get_command(self):
        return self._command
    
    def get_arguments(self):
        return self._arguments
    
class JSONbodyParser(bodyParser):
    def _parse(self):
        try:
            #print self._body
            message = json.loads(self._body)
            #print message
            self._command = message["command"]
            self._arguments = message["arguments"]
        except:            
            raise JSONCommandException()

class JSONCommandException(Exception):
    pass

class MessageProcessor():
    def __init__(self, game):        
        self._game = game
        class_name = self._game.__class__.__name__        
        mapper = Processor_Mapper[class_name]        
        self._getProcessor = getProcessor(mapper)        
        
    def process(self, message):        
        game = self._game
        #player = Player(self._player) ##to be working
        player = message.get_from_user()        
        parser = bodyParser(message.get_body())
        command = parser.get_command()
        arguments = parser.get_arguments()
        pro = self._getProcessor.get_processor(command)
        process_result = False
        if pro:
            try:
                proc = pro(game, player, arguments)
                process_result = proc.process()
            except:                
                #raise(Exception('MessageProcessor: unexpected error.'))
                #raise
                
                LOGGER.error('MessageProcessor: unexpected error.'+traceback.format_exc())
                process_result = False
        #else:
            #print 'Invalid command'
        #    self._game.send_output(player, 'ERROR XX')
        if not process_result:
            self._game.send_output(player, 'ERROR XX')
        self._game.commit_output()
        return process_result

class JSONMessageProcessor(MessageProcessor):
    def process(self, message):        
        game = self._game
        process_result = False
        parser = None
        #player = Player(self._player) ##to be working
        player = message.get_from_user()
        try:        
            parser = JSONbodyParser(message.get_body())
        except:
            LOGGER.error('JSONMessageProcessor: unexpected error.'+traceback.format_exc())            
            #pass
        if parser:
            command = parser.get_command()
            arguments = parser.get_arguments()
            pro = self._getProcessor.get_processor(command)        
            if pro:
                try:
                    proc = pro(game, player, arguments)
                    process_result = proc.process()
                except:                
                    #raise(Exception('MessageProcessor: unexpected error.'))
                    #raise
                    LOGGER.error('JSONMessageProcessor: unexpected error.'+traceback.format_exc())
                    process_result = False
        #else:
            #print 'Invalid command'
        #    self._game.send_output(player, 'ERROR XX')
        if not process_result:
            self._game.send_JSON_output(player, {'command': 'ERROR', 'code':'XX'})
        self._game.commit_output()
        return process_result
        
