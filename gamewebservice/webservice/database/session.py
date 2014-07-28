'''
Created on Aug 29, 2012

@author: leen
'''
import string
import random
import datetime
import logging
import pymongo
from webservice.database.mongo_connector import Mongo_Connector

logger = logging.getLogger('mongoconnection')
logger.addHandler(logging.FileHandler('mongodb_connection.log'))
logger.setLevel(logging.DEBUG)

CHARS = string.ascii_letters + string.digits
EXPIRED_SESSION_TIME = 3600 * 24 * 7 #1 week

def random_string_generator(size=8):
    system_random = random.SystemRandom()     
    return ''.join(system_random.choice(CHARS) for _ in range(size))

class Session_Mongo_Connector(Mongo_Connector):
    
    def __init__(self, host='localhost',port=27017):
        Mongo_Connector.__init__(self, host, port)
        self._database = self._connection['sessiontoken']
        self._token_collection = self._database['token']
        self._token_collection.ensure_index([('tokenid',1)],unique=True)
        self._token_collection.ensure_index([('username',1)])
        self._token_collection.ensure_index([('created_time',1)], expireAfterSeconds=EXPIRED_SESSION_TIME)
        
    def create_token(self, username, token_id=None):
        result = None
        if not token_id:
            token_id = random_string_generator(64)
            while self.is_exist(token_id):
                token_id = random_string_generator(64)
        existed_user_token = self.get_user_token(username)
        if existed_user_token:
            self.delete_token(existed_user_token['tokenid'])
        try:
            session_record = {'tokenid': token_id,
                              'created_time': datetime.datetime.utcnow(),
#                              'expired_time': expired_time,
                              'auth': True,
                              'username': username,
                              }
            good = self._token_collection.insert(session_record, safe=True)
            if good:
                result = token_id
        except pymongo.errors.DuplicateKeyError:
            logger.error("Duplicate tokenid")
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")
        except:
            logger.error("Unexpected Error")
        return result
    
    def is_exist(self, token_id):
        result = None
        try:
            result = self._token_collection.find_one({'tokenid': token_id})
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")
        except:
            logger.error("Unexpected Error")
        return result
    
    def get_user_token(self, username):
        result = None
        try:
            result = self._token_collection.find_one({'username': username})
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")
        except:
            logger.error("Unexpected Error")
        return result
    
    def get_token(self, token_id):
        return self.is_exist(token_id)
    
    def delete_token(self, token_id):
        result = None
        try:
            result = self._token_collection.remove({'tokenid': token_id}, safe=True)
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")
        except:
            logger.error("Unexpected Error")
        return result            