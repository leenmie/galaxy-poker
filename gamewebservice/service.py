'''
Created on Aug 17, 2012

@author: leen
'''
import cherrypy
import threading

from webservice.database.mongo_connector import Mongo_Ejabberd_Connector, Mongo_UserInfo_Connector
from webservice.database.session import Session_Mongo_Connector
from webservice.database.captcha import Captcha_Session_Connector
from webservice.database.topup import TopUpConnector
from webservice.database.anonymous import Mongo_Guest_Auth_Connector, Mongo_Guest_UserInfo_Connector

from webservice.resources.resource import Resource
from webservice.resources.register import RegisterResource
#from webservice.resources.register_new import RegisterResource
from webservice.resources.changepassword import ChangePasswordResource
from webservice.resources.verifyemail import VerifyEmailResource
from webservice.resources.requestverifyemail import RequestVerifyEmailResource
from webservice.resources.getauthenticatedsession import GetAuthenticatedSessionResource
from webservice.resources.requestforgotpasswd import RequestForgotPasswordResource
#from webservice.resources.hellocaptcha import HelloCaptchaResource
from webservice.resources.imagecardcaptcha import ImageCardCaptchaResource, ImageCardCaptchaExampleResource
from webservice.resources.checkcaptcha import CheckCaptchaResource
from webservice.resources.anonymous import AnonymousResource
from webservice.resources.resetpassword import ResetPasswordResource
from webservice.resources.FBauthentication import FBAuthenticationResource
from webservice.resources.authentication_email import AuthenticationEmailResource
from webservice.resources.userinfo import UserInfoResource

from webservice.tools.captchamanager import CaptchaManager
from webservice.tools.emailmanager import EmailManager

USE_CAPTCHA_PROTECTION = True

class Root(Resource):
    pass

def error_response_default(status, message, traceback, version):
    result = 'Sorry, an error occured.'
    return result

def error_response():
    result = 'Sorry, an error occured at processing.'
    return result

def clean_up_captcha_manager(captcha_manager):
    captcha_manager.cleanup()
    #print 'Clean up'
    threading.Timer(3600, clean_up_captcha_manager,[captcha_manager,]).start()
    
def send_email_in_queue(email_manager):
    email_manager.send_queue()
    threading.Timer(60, send_email_in_queue,[email_manager,]).start()

if __name__ == '__main__':
    root = Root()
    captcha_manager = CaptchaManager()
    email_manager = EmailManager()
    #timer = threading.Timer(3600, captcha_manager.cleanup)
    #timer.start()
    clean_up_captcha_manager(captcha_manager)
    send_email_in_queue(email_manager)
    
    auth_database = Mongo_Ejabberd_Connector()
    userinfo_database = Mongo_UserInfo_Connector()
    session_database = Session_Mongo_Connector()
    captcha_database = Captcha_Session_Connector()
    logtopup_database = TopUpConnector()
    guest_auth_database = Mongo_Guest_Auth_Connector()
    guest_userinfo_database = Mongo_Guest_UserInfo_Connector()
    
    
    """Register service"""
    register = RegisterResource(auth_database, userinfo_database, guest_auth_database, guest_userinfo_database)
    register.check_captcha = None# captcha_manager
    root.register = register
    """Change password service"""
    root.changepassword = ChangePasswordResource(auth_database)
    """Verify email service"""
    root.verifyemail = VerifyEmailResource(auth_database)
    """Captcha service"""
    root.captcha = ImageCardCaptchaResource(captcha_database, captcha_manager)
    root.captcha.example = ImageCardCaptchaExampleResource(captcha_database)
    """Topup service"""
    """Anonymous service"""
    resource_anonymous = AnonymousResource(guest_auth_database, guest_userinfo_database)
    resource_anonymous.check_captcha = None
    root.anonymous = resource_anonymous
    """Facebook login service"""
    resource_fblogin = FBAuthenticationResource(userinfo_database, session_database)
    root.fblogin = resource_fblogin
    """UserInfo service"""
    resource_userinfo = UserInfoResource(auth_database, userinfo_database, session_database, guest_auth_database, guest_userinfo_database)
    resource_userinfo.check_captcha = None
    root.userinfo = resource_userinfo
            
    root.checkcaptcha = CheckCaptchaResource(captcha_manager)
    
    
    #root.requestverify = RequestVerifyEmailResource(auth_database, session_database)
    #root.authenticate = GetAuthenticatedSessionResource(auth_database, session_database)
    #root.topup = TopUpMoneyResource(None)
    #root.requestforgot = RequestForgotPasswordResource(auth_database)
    #root.requestforgot.check_captcha = captcha_manager
    root.authenticate = AuthenticationEmailResource(auth_database, session_database)
    root.requestforgot = RequestForgotPasswordResource(auth_database)
    root.requestforgot.check_captcha = None
    root.requestforgot.email_manager = email_manager
    root.resetpassword = ResetPasswordResource(auth_database)
    root.resetpassword.check_captcha = None
    #root.getuserinfo = GetUserInfoResource(auth_database, userinfo_database)
    
    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8000,
            'server.thread_pool': 200,
            'error_page.default': error_response_default,
        },
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),            
        },
        '/example': {'tools.staticfile.on': True,
                      'tools.staticfile.filename':'/home/leen/workspace/GameWebService/webservice/static/example.html',
        },
        '/captchajs': {'tools.staticfile.on': True,
                      'tools.staticfile.filename':'/home/leen/workspace/GameWebService/webservice/static/captcha.js',     
        },       
    }    
    #cherrypy.quickstart(root, '/', conf)
    cherrypy.log.screen = True
    cherrypy.log.access_file = 'access.log'
    cherrypy.log.error_file = 'error.log'
    #cherrypy.quickstart(root,'/', config=conf)
    cherrypy.tree.mount(root,"/", config=conf)
    
    cherrypy.config.update(conf)
    cherrypy.engine.start()    
    #root.sidewinder.send_verification_email('test1000','onlylinh@gmail.com')