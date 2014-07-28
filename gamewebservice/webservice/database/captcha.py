'''
Created on Sep 20, 2012

@author: leen
'''
from webservice.database.mongo_connector import Mongo_Connector
from webservice.tools.utils import random_string_generator
import bson
import StringIO
import datetime

EXPIRED_CAPTCHA_TIME = 60*5 #5 minutes
MAX_CAPTCHA_TRY = 3 

class Captcha_Session_Connector(Mongo_Connector):
    
    def __init__(self, host='localhost',port=27017):
        Mongo_Connector.__init__(self, host, port)
        self._database = self._connection['captcha']
        self._captcha_collection = self._database['captcha']
        self._captcha_collection.ensure_index([('turingtestid',1)],unique=True)
        self._captcha_collection.ensure_index([('created_time',1)], expireAfterSeconds=EXPIRED_CAPTCHA_TIME)   
        
    
    def create_captcha(self, captcha_image, value): 
        try:
            buffering = StringIO.StringIO()
            captcha_image.save(buffering,"JPEG")
            #buffering.getvalue()
            image_data = bson.binary.Binary(buffering.getvalue())
            turingtestid = random_string_generator(10)
        except:
            raise
            #return None
        captcha_values = {'turingtestid':turingtestid,
                          'image':image_data,
                          'value':value,
                          'try':0,
                          'created_time': datetime.datetime.utcnow(),
                          }
        try:
            self._captcha_collection.insert(captcha_values, safe=True)
        except:
            return None
        return captcha_values
           
    def get_captcha(self, turingtestid):
        result = None
        try:
            result = self._captcha_collection.find_one({'turingtestid':turingtestid})
            if result:
                if result['try'] >= MAX_CAPTCHA_TRY:
                    self.delete_captcha(turingtestid)
                    return None
                else:
                    self._captcha_collection.update({'turingtestid':turingtestid},{'$inc': {'try': 1}})
        except:
            pass        
        return result
    
    def verify_captcha(self, turingtestid, answer):
        result = None
        try:
            result = self._captcha_collection.find_one({'turingtestid':turingtestid},['turingtestid','value','try'])
            if result:                
                if result['value'] != answer:
                    result = None
                #delete this captcha
                self.delete_captcha(turingtestid)                
        except:
            pass
        if result:
            return True
        else:            
            return False
    
    def delete_captcha(self, turingtestid):
        try:
            self._captcha_collection.remove({'turingtestid':turingtestid})
        except:
            pass