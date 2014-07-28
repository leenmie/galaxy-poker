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

class ResetPasswordResource(Resource):
    check_captcha = True
        
    def GET(self, email=None, resetcode=None):
        email_text = ''
        resetcode_text=resetcode
        if email:
            email_text = email
        if not resetcode:
            resetcode_text=''
        form_html = "<html><head><title>Forgot Password</title></head><body>"+\
        "<form name=\"input\" method=\"post\" action=\"/service/resetpassword/\">"+\
        'Email: <input type="text" name="email" value="{}" />'.format(email_text)+\
        'Reset Code: <input type="text" name="resetcode" value="{}" />'.format(resetcode_text)+\
        'New password: <input type="password" name="newpassword" />'+\
        "<input type=\"submit\" value=\"Submit\" />"+\
        "</form>" +\
        "</body></html>"
        return form_html

    
    def POST(self, email, resetcode, newpassword, recaptcha_challenge_field=None, recaptcha_response_field=None):
        if 'X-Real-IP' in cherrypy.request.headers:
            ip_remote = cherrypy.request.headers['X-Real-IP']
        else:
            ip_remote = cherrypy.request.remote.ip
        if self.check_captcha:
            check = self.check_captcha.verify_captcha(recaptcha_challenge_field, recaptcha_response_field,ip_remote)
            if not check:
                return to_json({'result': 2, 'description': 'Wrong captcha.'})                
        #print username
        email = email.lower()
        res = self._database.reset_password(email, resetcode, newpassword)
        if res:
            return to_json({'result': 0, 'description': 'Password changed.'})
        return to_json({'result': 1, 'description': 'Reset password failed.'})                                
