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


class RegisterResource(Resource):
    check_captcha = False
    
    def __init__(self, authenticate_database, userinfo_database):
        self._auth_db = authenticate_database
        self._userinfo_db = userinfo_database
    
    def GET(self):
        #int('hehe')
        form_html = '''<html>
        <head>
        <title>Register</title>
        <script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
        <script type="text/javascript" src="http://www.google.com/recaptcha/api/js/recaptcha_ajax.js"></script>
        <script type="text/javascript" src="/captchajs"></script>
        <script>
        $(document).ready(function(){
            var cafecaptcha = new CafeCaptcha("captcha_area");
            cafecaptcha.loadCaptcha();
        })            
        </script>
        </head>
        <body>
        <form name="input" method="post">
        Username: <input type="text" name="username" />
        Password: <input type="password" name="password" />
        Email: <input type="text" name="email" />
        Phone: <input type="text" name="phone" />
        <div id="captcha_area"></div>
        <input type="submit" value="Submit" />
        </form>
        </body></html>'''
        return form_html         
    
    def check_register_value(self, username, password, email, phone=None):
        if not REGEX_USERNAME.match(username):
            return False
        """dont allow register a guest username"""
        if REGEX_GUEST_USERNAME.match(username):
            return False
        if not REGEX_PASSWORD.match(password):
            return False
        if not REGEX_EMAIL.match(email):
            return False
        if phone:
            if not REGEX_PHONE.match(phone):
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
    
    def POST(self, username, password, email, phone=None, recaptcha_challenge_field=None, recaptcha_response_field=None):
        username = username.lower()
        full_username = '{}@{}'.format(username, XMPP_DOMAIN_NAME)        
        """check captcha"""
        if 'X-Real-IP' in cherrypy.request.headers:
            ip_remote = cherrypy.request.headers['X-Real-IP']
        else:
            ip_remote = cherrypy.request.remote.ip        
        if self.check_captcha:
            check = self.check_captcha.verify_captcha(recaptcha_challenge_field, recaptcha_response_field, ip_remote)
            if not check:
                return to_json({'result': 2, 'description': 'Wrong captcha.'})
        """register"""
        if self.check_register_value(username, password, email, phone):
            avatar_random = random.randint(0,24)         
            created_auth = self._auth_db.create_user(username, password, email, phone)
            #create a userinfo record
            created_info = self._userinfo_db.create_user(full_username, avatar_id = avatar_random)
            verification_code = random_string_generator(12)
            verified = self.send_verification_email(username, email, verification_code)
            if created_auth and created_info:
                return to_json({'result': 0, 'description': 'Registration is successful.'})
            else:
                return to_json({'result': 4, 'description': 'Duplicate username or email.'})
        else:
            return to_json({'result': 3, 'description': 'Invalid input value.'})
        return to_json({'result': 1, 'description': 'Registration error.'})

