'''
Created on Feb 24, 2012

@author: leen
'''
#import cPickle
import json
from twisted.words.xish import domish
from wokkel.xmppim import MessageProtocol, AvailablePresence
from boardgame.main_config import XMPP_SERVICE_NAME, XMPP_DOMAIN_NAME
import string
import time
import re
from boardgame.utils.Message import Message

STRING_BODY_LIMIT = 500
REGEX_USERNAME = re.compile('^[a-zA-Z0-9._+@]{4,50}$')
REGEX_BODY = re.compile('^[a-zA-Z0-9 ]{3,200}$')#, flags=re.UNICODE)

def clean_username(username):
    result = None
    try:
        parts = username.split('/')
        if len(parts) <= 2:
            result = parts[0].lower().encode('ascii','strict')
    except:
        return None
    if REGEX_USERNAME.match(result):            
        return result
    return None

def clean_body(body_msg):
    result = None
    #print body_msg
    try:
        result = body_msg.encode('utf-8','strict')
    except:
        return None
    if REGEX_BODY.match(result):
        return result
    return None

class GameBotProtocol(MessageProtocol):
    def __init__(self, component=False, socket=None):
        MessageProtocol.__init__(self)
        self.component = component
        self._socket = socket
        self._message_count = 0
        self._begin_time = None

    def connectionMade(self):
        if not self.component:
            self.send(AvailablePresence())

    def connectionLost(self, reason):
        print "Disconnected!"

    def onMessage(self, msg):
        if self._message_count == 0:
            self._begin_time = time.time()
        if self._socket:
            if msg["type"] == 'chat' and hasattr(msg, "body"):                
                #from_user = msg['from']
                from_user = msg['from'].split('@')[0]
                from_user = clean_username(from_user)
                """ignore malform username"""
                if not from_user:
                    return
                #msg_body = clean_body(str(msg.body))
                #if not msg_body:
                #    return
                msg_body = str(msg.body)
                if len(msg_body) > STRING_BODY_LIMIT:
                    return
                message = {"from_user":from_user, "body":msg_body}
                seri_message = json.dumps(message)
                self._socket.send(seri_message)
        self._message_count += 1
        if self._message_count == 10000:
            delta_time = time.time() - self._begin_time
            print 'Received 10000 messages in [', delta_time, ']seconds.'
            self._message_count = 0
            self._begin_time = time.time()
            
                
    def sendBack(self, msg):
        reply = domish.Element((None, "message"))
        reply["to"] = ''.join([msg['from_user'],'@',XMPP_DOMAIN_NAME])
        reply["from"] = XMPP_SERVICE_NAME
        reply["type"] = 'chat'
        reply.addElement('body', content=msg['body'])        
        self.send(reply)
        