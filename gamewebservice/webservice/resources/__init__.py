import re
from webservice.tools.utils import to_json
from webservice import main_config

REGEX_USERNAME = re.compile('^[a-zA-Z0-9._]{4,32}$')
REGEX_NICKNAME = re.compile('^[a-zA-Z0-9._ ]{4,32}$')
"""guestxxxxxx"""
REGEX_GUEST_USERNAME = re.compile('^(guest)')
"""password's length is from 6 to 32"""
REGEX_PASSWORD = re.compile('^.{6,32}$')
#REGEX_EMAIL = re.compile('^[a-zA-Z0-9+&*-]+(?:\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,7}$')
REGEX_EMAIL = re.compile('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,7}$')
"""+84 xxx xxx"""
REGEX_PHONE = re.compile('^\+?[0-9 ]{7,15}$')

REGEX_ALPHANUM = re.compile('^[a-zA-Z0-9]{4,32}$')


RECAPTCHA_PUBLIC_KEY = main_config.CF_RECAPTCHA_PUBLIC_KEY
RECAPTCHA_PRIVATE_KEY = main_config.CF_RECAPTCHA_PRIVATE_KEY


XMPP_DOMAIN_NAME = main_config.CF_XMPP_DOMAIN_NAME
HOST_DOMAIN_NAME = main_config.CF_HOST_DOMAIN_NAME



def push_email_to_sending_queue(msg):
    return True

def captcha_validate(captcha_manager, recaptcha_challenge_field, recaptcha_response_field, ip_remote):
    captcha_valid = None
    if captcha_manager:
        if (not recaptcha_challenge_field) or (not recaptcha_response_field):
            """need captcha"""
            return to_json({'result': 2, 
                            'description': 'Captcha is required.',})
        captcha_challenge = recaptcha_challenge_field
        captcha_response = recaptcha_response_field

        #captcha = captcha_manager.get_captcha(ip_remote)
        captcha_valid = captcha_manager.verify_captcha(captcha_challenge, captcha_response, ip_remote)            
        if not captcha_valid:
            return to_json({'result': 3, 'description': 'Wrong captcha.'})
    return captcha_valid