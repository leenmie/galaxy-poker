'''
Created on Feb 14, 2013

@author: leen
'''
import cherrypy
import time
import random
from webservice import main_config
from webservice.resources.resource import Resource
from webservice.resources import to_json, XMPP_DOMAIN_NAME
from webservice.tools.utils import random_string_generator
import uuid

GUEST_FREE_MONEY = main_config.CF_GUEST_FREE_MONEY

class AnonymousResource(Resource):
    
    def __init__(self, guest_auth_db, guest_userinfo_db):
        self._auth_db = guest_auth_db
        self._userinfo_db = guest_userinfo_db
        
    def GET(self):
        html = \
        """<html>
        <head><title>Anonymous</title></head>
        <body>
            <form method="post">
                <input type="submit" value="POST"/>
            </form>
        </body>
        </html>"""
        return html
    
    def POST(self, recaptcha_challenge_field=None, recaptcha_response_field=None):
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
            random_username = ''.join(['guest',uuid.uuid4().hex]).lower()
            #full_username = '{}@{}'.format(random_username, XMPP_DOMAIN_NAME) 
            avatar_random = random.randint(0,24)
            created_auth = self._auth_db.create_user(random_username)
            created_info = self._userinfo_db.create_user(random_username, free_money=GUEST_FREE_MONEY, avatar_id=avatar_random)
            if created_auth and created_info:
                return to_json({'result': 0,
                                'userid': random_username,
                                 'description': 'Anonymous registration is successful.'})
            else:
                return to_json({'result': 3, 'description': 'Cannot register anonymous user.'})
        except: 
            return to_json({'result': 9, 'description': 'Error.'})
        return to_json({'result': 9, 'description': 'Error.'})