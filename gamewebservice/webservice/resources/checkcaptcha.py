'''
Created on Sep 30, 2012

@author: leen
'''
import cherrypy
from webservice.resources.resource import Resource

class CheckCaptchaResource(Resource):
    
    def __init__(self, captcha_manager):
        self._captcha_manager = captcha_manager
            
    def GET(self, recaptcha_challenge_field, recaptcha_response_field):
        if 'X-Real-IP' in cherrypy.request.headers:
            ip_remote = cherrypy.request.headers['X-Real-IP']
        else:
            ip_remote = cherrypy.request.remote.ip
        res = self._captcha_manager.verify_captcha(recaptcha_challenge_field, recaptcha_response_field,ip_remote)
        return str(res)    