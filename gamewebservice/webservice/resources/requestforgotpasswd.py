'''
Created on Sep 16, 2012

@author: leen
'''
import cherrypy
import recaptcha
#from recaptcha.client import captcha
from webservice.resources.resource import Resource
from webservice.resources import RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY,\
                                REGEX_USERNAME, REGEX_PASSWORD, REGEX_EMAIL, REGEX_PHONE
from webservice.resources import push_email_to_sending_queue
from webservice.tools.utils import multipart_email, to_json, random_string_generator
from webservice.main_config import CF_WEBSERVICE_URL, CF_EMAIL_NOREPLY


class RequestForgotPasswordResource(Resource):
    check_captcha = None
    email_manager = None
    
    def send_reset_password_email(self, email, reset_code):
        sent_email = None
        request = self._database.request_forgot_password(email, reset_code)
        
        if request:
            text="""\
            Hi {1},            
            Your reset password code is {0}.
            Follow this link to reset your password: {2}/resetpassword?email={1}&resetcode={0}
            """
            text = text.format(reset_code, email, CF_WEBSERVICE_URL)
            html="""\
            <html>
            <head></head>
            <body>
            Hi <b>{1}</b>,            
            Your reset password code is {0}.<br/>
            Follow this link to reset your password: <a href={2}/resetpassword?email={1}&resetcode={0}>Reset password</a>
            </body>
            </html>
            """
            html = html.format(reset_code, email, CF_WEBSERVICE_URL)
            msg = multipart_email(CF_EMAIL_NOREPLY, email, 'Reset password', text, html)
            if self.email_manager:
                sent_email = self.email_manager.enqueue(msg)
        return sent_email
        
    def GET(self):
        form_html = "<html><head><title>Forgot Password</title></head><body>"+\
        "<form name=\"input\" method=\"post\">"+\
        'Email: <input type="text" name="email" />'+\
        "<input type=\"submit\" value=\"Submit\" />"+\
        "</form>" +\
        "</body></html>"
        return form_html
    
    def POST(self, email, recaptcha_challenge_field=None, recaptcha_response_field=None):
        if 'X-Real-IP' in cherrypy.request.headers:
            ip_remote = cherrypy.request.headers['X-Real-IP']
        else:
            ip_remote = cherrypy.request.remote.ip
        if self.check_captcha:
            check = self.check_captcha.verify_captcha(recaptcha_challenge_field, recaptcha_response_field,ip_remote)
            if not check:
                return to_json({'result': 2, 'description': 'Wrong captcha.'})
            
        reset_code = random_string_generator(12)
        email = email.lower()
        res = self.send_reset_password_email(email, reset_code)
        if res:
            return to_json({'result': 0, 'description': 'Reset password email sent.'})
        return to_json({'result': 1, 'description': 'Request resetting password failed.'})                                
