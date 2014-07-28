'''
Created on Sep 16, 2012

@author: leen
'''
import cherrypy
from recaptcha.client import captcha
from webservice.resources.resource import Resource
from webservice.resources import RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY,\
                                REGEX_USERNAME, REGEX_PASSWORD, REGEX_EMAIL, REGEX_PHONE
from webservice.resources import push_email_to_sending_queue
from webservice.tools.utils import multipart_email, to_json, random_string_generator
from webservice.main_config import CF_WEBSERVICE_URL, CF_EMAIL_NOREPLY

class RequestVerifyEmailResource(Resource):
    check_captcha = True
    
    def __init__(self, authentication_db, session_db):
        self._auth_db = authentication_db
        self._session_db = session_db
    
    def send_verification_email(self,username, email, verification_code):
        sent_email = False
        verified = self._auth_db.create_email_verification_code(verification_code, username)
        if verified:            
            text="""\
            Hi {1},            
            Your verification code is {0}.
            Follow this link to complete your email verification: {2}/verifyemail?verification_code={0}&username={1}
            """
            text = text.format(verification_code,username, CF_WEBSERVICE_URL)
            html="""\
            <html>
            <head></head>
            <body>  
            Hi <b>{1}</b>,         
            Your verification code is {0}.<br/>
            Follow this link to complete your email verification: <a href={2}/verifyemail?verification_code={0}&username={1}>Verify Email</a>
            </body>
            </html> 
            """
            html = html.format(verification_code, username, CF_WEBSERVICE_URL)
            msg = multipart_email(CF_EMAIL_NOREPLY, email, 'Email verification', text, html)
            sent_email = push_email_to_sending_queue(msg)            
        return sent_email
                    
    def GET(self):
        form_html = '<html><head><title>Verify Email</title></head><body>'+\
        '<form name="input" method="post">'+\
        'Session: <input type="text" name="session_token" />'+\
        '<input type="submit" value="Submit" />'+\
        '</form>' +\
        '</body></html>'
        return form_html
    
    def POST(self, session_token, recaptcha_challenge_field=None, recaptcha_response_field=None):
        
        authenticated = self._session_db.get_token(session_token)
        if not authenticated:
            return to_json({'result': 3, 'description': 'Invalid session.'})
        if authenticated:
            username = authenticated['username']
            verification_code = random_string_generator(12)
            email = self._auth_db.exist_user(username)['email']
            res = self.send_verification_email(username, email, verification_code)
            if res:
                return to_json({'result': 0, 'description': 'Request is successful.'})
        return to_json({'result': 1, 'description': 'Request failed.'})
