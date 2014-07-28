'''
Created on Sep 16, 2012

@author: leen
'''
from webservice import main_config
from webservice.captcha.generalcaptcha import GeneralCaptcha
from recaptcha.client import captcha

RECAPTCHA_PUBLIC_KEY = main_config.CF_RECAPTCHA_PUBLIC_KEY
RECAPTCHA_PRIVATE_KEY = main_config.CF_RECAPTCHA_PRIVATE_KEY

class ReCaptcha(GeneralCaptcha):
    
    def get_embedded_code(self):
        return captcha.displayhtml(RECAPTCHA_PUBLIC_KEY)
    
    def verify(self, recaptcha_challenge_field, recaptcha_response_field, ip_remote='127.0.0.1'):
        res_captcha = captcha.submit(recaptcha_challenge_field, recaptcha_response_field, RECAPTCHA_PRIVATE_KEY, ip_remote)
        return res_captcha.is_valid