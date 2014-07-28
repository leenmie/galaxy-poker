'''
Created on Apr 10, 2012

@author: leen
'''
from boardgame.processors.GenericProcessor import GenericProcessor

class EmotionProcessor(GenericProcessor):
    '''
    Process emotion command
    '''
    def _other_init(self):
        #print 'emotion init'
        return True
    
    def process(self):
        try:
            emotion_id = int(self._arguments[0])
        except:
            print 'Invalid emotion id'
            return False
        if emotion_id < 0 or emotion_id >24:
            return False
        current_room_id = self._player.get_current_room()
        if current_room_id:
            current_room = self._game.get_room(current_room_id)
            current_room.emotion(self._player, emotion_id)
            return True
        return False
        