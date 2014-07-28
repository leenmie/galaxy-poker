'''
Created on Sep 20, 2012

@author: leen
'''
from webservice.captcha.generalcaptcha import GeneralCaptcha

class ImageCardCaptcha(GeneralCaptcha):
    
    #def get_embedded_code(self):
    #    return captcha.displayhtml(RECAPTCHA_PUBLIC_KEY)
    
    def __init__(self, captcha_database):
        self._captcha_connection = captcha_database
    
    def verify(self, captcha_challenge, captcha_response, ip_remote='127.0.0.1'):
        #captcha_con = Captcha_Session_Connector()
        valid = self._captcha_connection.verify_captcha(captcha_challenge, captcha_response)
        return valid