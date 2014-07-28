'''
Created on Feb 14, 2013

@author: leen
'''
import cherrypy
import time
import random
from webservice import main_config
from webservice.resources.resource import Resource
from webservice.resources import to_json, XMPP_DOMAIN_NAME, REGEX_NICKNAME, REGEX_PASSWORD
from webservice.tools.utils import random_string_generator
import uuid

GUEST_FREE_MONEY = main_config.CF_GUEST_FREE_MONEY

def check_userid(userid):
    """TODO: validate userid"""
    return True

def check_nickname(nickname):
    return REGEX_NICKNAME.match(nickname)
    
def check_password(password):
    return REGEX_PASSWORD.match(password)

class UserInfoResource(Resource):
    
    def __init__(self, auth_db, userinfo_db, session_db, guest_auth_db, guest_userinfo_db):
        self._auth_db = auth_db
        self._userinfo_db = userinfo_db
        self._session_db = session_db
        self._guest_auth_db = guest_auth_db
        self._guest_userinfo_db = guest_userinfo_db
        
    def GET(self, sessiontoken=None, guestid=None):
        if not sessiontoken:
            return to_json({'result':4, 'description': 'Null Session Token'})
        try:
            userid = None
            user = None
            if sessiontoken == 'guest':
                if guestid:
                    #userid = self._guest_auth_db.exist_user(guestid)["username"]
                    user = self._guest_userinfo_db.exist_user(guestid)
                else:
                    return to_json({'result':5, 'description': 'Null GuestID'})
            else:
                session_token = self._session_db.is_exist(sessiontoken)
                #print session_token
                if session_token:
                    userid = session_token["username"]
                    if userid:
                        user = self._userinfo_db.exist_user(userid)
            if user:
                userinfo = {'userid': user["username"],
                            'avatar': user["avatar"],
                            'money': user["money"],
                            'cash': user["cash"],
                            'nickname': user["nickname"],                            
                            }
                return to_json({'result': 0, 'userinfo': userinfo})
            else:
                return to_json({'result':9, 'description': 'Unknown error.'})
        except:
            #raise
            return to_json({'result':9, 'description': 'Unknown error.'})
        return None
        
    
    def POST(self, sessiontoken, guestid=None, recaptcha_challenge_field=None, recaptcha_response_field=None,
             avatar=None, nickname=None, oldpassword=None,newpassword=None):
        """check captcha"""
        if 'X-Real-IP' in cherrypy.request.headers:
            ip_remote = cherrypy.request.headers['X-Real-IP']
        else:
            ip_remote = cherrypy.request.remote.ip        
        if self.check_captcha:
            check = self.check_captcha.verify_captcha(recaptcha_challenge_field, recaptcha_response_field,ip_remote)
            if not check:
                return to_json({'result': 2, 'description': 'Wrong captcha.'})
        try:
            userid = None
            userinfo_db = self._userinfo_db
            if sessiontoken == 'guest':
                if guestid:
                    check_guest = self._guest_auth_db.exist_user(guestid)
                    if check_guest:
                        userinfo_db = self._guest_userinfo_db
                        userid = guestid
                else:
                    return to_json({'result':5, 'description': 'Null GuestID'})
            else:
                session_token = self._session_db.is_exist(sessiontoken)
                if session_token:
                    userid = session_token["username"]
                else:
                    return to_json({'result':3, 'description': 'Invalid Session Token'})
            if not userid:
                return to_json({'result':1, 'description': 'Null UserID'})
            
            updateinfo = {}
            result={}
            updated = False
            if avatar:
                iavatar = int(avatar)
                if iavatar>=0 and iavatar<=24:
                    updateinfo['avatar'] = iavatar
            if nickname:
                check_nick = check_nickname(nickname)
                if check_nick:
                    updateinfo['nickname'] = nickname
            if updateinfo:
                updated = userinfo_db.update_userinfo(userid, updateinfo)
                if updated:
                    result["update_info"] = updateinfo
            updated = False
            if sessiontoken != 'guest': 
                """guest account does not have password"""
                if newpassword and oldpassword:
                    if check_password(newpassword):
                        updated = self._auth_db.change_password(userid, oldpassword, newpassword)
                        if updated:
                            result["update_password"] = True
            if result:
                result["result"] = 0
                return to_json(result)
        except:
            return to_json({'result': 9, 'description': 'Error.'})
        return to_json({'result': 9, 'description': 'Error.'})