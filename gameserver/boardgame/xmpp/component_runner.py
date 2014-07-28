'''
Created on Feb 24, 2012

@author: leen
'''
import sys
sys.path.append('../')

from boardgame.zeromq.MsgQueue_XMPP import MsgQueue_XMPP
from twisted.application import service
from twisted.words.protocols.jabber import jid
from twisted.internet import reactor
from wokkel.component import Component
from boardgame.xmpp.GameBotProtocol import GameBotProtocol
from boardgame.xmpp.ThreadOutput import ThreadOutput
from boardgame.main_config import XMPP_SERVICE_HOST, XMPP_SERVICE_PORT, XMPP_SERVICE_NAME, XMPP_SERVICE_PASSWORD, XMPP_SERVICE_LOG

msgqueue = MsgQueue_XMPP()
#msgqueue = None
echobot = GameBotProtocol(component=True, socket=msgqueue)
#ping_protocol = PingClientProtocol()

thread_output = ThreadOutput(msgqueue, echobot)
thread_output.start()

application = service.Application("GameBot")
xmppcomponent = Component(XMPP_SERVICE_HOST, XMPP_SERVICE_PORT, XMPP_SERVICE_NAME, XMPP_SERVICE_PASSWORD)
xmppcomponent.logTraffic = XMPP_SERVICE_LOG
echobot.setHandlerParent(xmppcomponent)
xmppcomponent.setServiceParent(application)
#reactor.run()