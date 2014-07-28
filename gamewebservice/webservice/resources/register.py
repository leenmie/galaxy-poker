'''
Created on Sep 16, 2012

@author: leen
'''
import cherrypy
import random
from recaptcha.client import captcha
from webservice.resources.resource import Resource
from webservice.resources import RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY,\
                                REGEX_USERNAME, REGEX_PASSWORD, REGEX_EMAIL, REGEX_PHONE,\
                                REGEX_GUEST_USERNAME, XMPP_DOMAIN_NAME, HOST_DOMAIN_NAME
from webservice.resources import push_email_to_sending_queue, captcha_validate
from webservice.tools.utils import multipart_email, to_json, random_string_generator
from webservice.main_config import CF_FREE_MONEY, CF_GUEST_FREE_MONEY

class RegisterResource(Resource):
    check_captcha = False
    
    def __init__(self, authenticate_database, userinfo_database, guest_auth_db, guest_userinfo_db):
        self._auth_db = authenticate_database
        self._userinfo_db = userinfo_database
        self._guest_auth_db = guest_auth_db
        self._guest_userinfo_db = guest_userinfo_db
    
    def GET(self):
        #int('hehe')
        form_html = '''<html>
        <head>
        <title>Register</title>
        </head>
        <body>
        <form name="input" method="post">
        Email: <input type="text" name="email" />
        Password: <input type="password" name="password" />
        GuestID: <input type="text" name="guestid" />
        <div id="captcha_area"></div>
        <input type="submit" value="Submit" />
        </form>
        </body></html>'''
        return form_html         
    
    def check_register_value(self, password, email):        
        if not REGEX_PASSWORD.match(password):
            return False
        if not REGEX_EMAIL.match(email):
            return False
        return True

    def send_verification_email(self,username, email, verification_code):
        #msg = MIMEText('Registration is sucessful. Your verification code is {}.'.format(verification_code))
        sent_email = False
        verified = self._auth_db.create_email_verification_code(verification_code, username)
        if verified:        
            text="""\
            Registration for user {0} is successful.
            Your verification code is {1}.
            Follow this link to complete your email verification: http://{2}/service/verifyemail?verification_code={1}&username={0}
            """
            text = text.format(username, verification_code, HOST_DOMAIN_NAME)
            html="""\
            <html>
            <head></head>
            <body>
            Registration for user <b>{0}</b> is successful.<br/>
            Your verification code is <b><i>{1}</i></b>.<br/>
            Follow this link to complete your email verification: <a href=http://{2}/service/verifyemail?verification_code={1}&username={0}>Verify Email</a>
            </body>
            </html>
            """
            html = html.format(username, verification_code, HOST_DOMAIN_NAME)
            msg = multipart_email('noreply@cacafefe.com', email, 'Cacafefe registration', text, html)
            sent_email = push_email_to_sending_queue(msg)            
        return sent_email
    
    def POST(self, email, password, guestid=None):
        email = email.lower()
        """register"""
        guest_user = None
        if guestid:
            guest_user = self._guest_auth_db.exist_user(guestid)
            if not guest_user:
                return to_json({'result': 5, 'description': 'Invalid guest ID.'})
            else:
                guest_user = self._guest_userinfo_db.exist_user(guestid)          
            
        if self.check_register_value(password, email):
            avatar_random = random.randint(0,24)         
            created_auth = self._auth_db.create_user_by_email(email, password)
            #create a userinfo record
            created_info = None
            if created_auth:
                init_money = 0
                free_money = CF_FREE_MONEY
                nickname = 'ThanBai'
                if guest_user:
                    init_money = guest_user['money']
                    free_money = init_money + (CF_FREE_MONEY - CF_GUEST_FREE_MONEY)
                    nickname = guest_user['nickname']
                    
                #full_name = "{}@{}".format(created_auth["username"],XMPP_DOMAIN_NAME)
                created_info = self._userinfo_db.create_user(created_auth["username"], free_money = free_money, 
                                                             avatar_id = avatar_random, nickname = nickname)
                #print created_auth
            #verification_code = random_string_generator(12)
            #verified = self.send_verification_email(username, email, verification_code)
            if created_auth and created_info:
                if guest_user:
                    self._guest_auth_db.remove_user(guestid)
                    self._guest_userinfo_db.remove_user(guestid)
                return to_json({'result': 0, 'description': 'Registration is successful.'})
            else:
                return to_json({'result': 4, 'description': 'Duplicate email.'})
        else:
            return to_json({'result': 3, 'description': 'Invalid input value.'})
        return to_json({'result': 1, 'description': 'Registration error.'})

