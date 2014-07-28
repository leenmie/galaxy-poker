'''
Created on Sep 20, 2012

@author: leen
'''
import time
from webservice import main_config
from webservice.captcha.defaultcaptcha import ImageCardCaptcha
from webservice.captcha.Recaptcha import ReCaptcha
from webservice.database.captcha import Captcha_Session_Connector

CAPTCHA_DEFAULT = main_config.CF_CAPTCHA_DEFAULT
CAPTCHA_RECAPTCHA = 1

SAFE_CAPTCHA_ACCESS_LIMIT_GLOBAL = main_config.CF_SAFE_CAPTCHA_ACCESS_LIMIT_GLOBAL
SAFE_CAPTCHA_ACCESS_LIMIT_IP = main_config.CF_SAFE_CAPTCHA_ACCESS_LIMIT_IP

class CaptchaManager():
    
    def __init__(self):
        self._log_per_IP = {}
        self._access_last_minute = 0
        self._remember_time = time.time()
        self._captcha_database = Captcha_Session_Connector()
        
    def update_captcha_count(self, IPAddress):
        """
        Update accesing load base on IP Addresses
        """
        current_time = time.time()
        if current_time - self._remember_time <=60:
            self._access_last_minute += 1
        else:
            self._remember_time = current_time
            self._access_last_minute = 0
        if IPAddress in self._log_per_IP:
            if current_time - self._log_per_IP[IPAddress]['last_access'] <=60:
                self._log_per_IP[IPAddress]['count'] +=1                
            else:
                self._log_per_IP[IPAddress]['count'] = 1
                self._log_per_IP[IPAddress]['last_access'] = current_time                
        else:
            self._log_per_IP[IPAddress] = {'count': 1, 'last_access':current_time}
    
    def get_captcha_id(self, IPAddress):
        """
        get captcha type base on IPAddress and accessing load. Use Recaptcha if suspect any spam
        """        
        current_time = time.time()
        if current_time - self._remember_time > 60:
            self._remember_time = current_time
            self._access_last_minute = 0
        
        if self._access_last_minute > SAFE_CAPTCHA_ACCESS_LIMIT_GLOBAL:
            """we got spam now, use recaptcha. Good luck google"""
            return CAPTCHA_RECAPTCHA
        if IPAddress in self._log_per_IP:
            if current_time - self._log_per_IP[IPAddress]['last_access'] > 60:
                self._log_per_IP[IPAddress]['count'] = 1            
                self._log_per_IP[IPAddress]['last_access'] = current_time
            if self._log_per_IP[IPAddress]['count'] > SAFE_CAPTCHA_ACCESS_LIMIT_IP:
                """This IP is spamming us, use recaptcha"""
                return CAPTCHA_RECAPTCHA                    
        return CAPTCHA_DEFAULT
    
    def get_captcha(self, IPAddress):
        captcha_id = self.get_captcha_id(IPAddress)
        if captcha_id == CAPTCHA_DEFAULT:
            return ImageCardCaptcha(self._captcha_database)
        elif captcha_id == CAPTCHA_RECAPTCHA:
            return ReCaptcha()
        return None
            
    def verify_captcha(self, recaptcha_challenge_field, recaptcha_response_field, ip_remote):
        captcha = self.get_captcha(ip_remote)
        return captcha.verify(recaptcha_challenge_field, recaptcha_response_field, ip_remote)
    
    def cleanup(self):
        """clean all information after a long interval, release memory"""
        self._log_per_IP = {}
        self._access_last_minute = 0
        self._remember_time = time.time()        
            