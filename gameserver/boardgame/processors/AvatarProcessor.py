from GenericProcessor import GenericProcessor
import logging
LOGGER = logging.getLogger('gamedebug')

class AvatarProcessor(GenericProcessor):
    
    def process(self):
        if len(self._arguments)>=1:
            if self._arguments[0] == 'get':
                result = ' '.join(['AVATAR', str(self._player.get_avatar())])
                self._game.send_output(self._player, result)
                return True
            elif self._arguments[0] == 'set':
                if len(self._arguments) == 2:
                    value = self._arguments[1]
                    try:
                        iAvatar = int(value)
                        if iAvatar >=0 and iAvatar <=24:
                            self._player.set_avatar(iAvatar)
                    except:
                        return False
                    result = ' '.join(['AVATAR', str(self._player.get_avatar())])
                    self._game.send_output(self._player, result)                    
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False                                    
        return False