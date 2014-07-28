'''
Created on Feb 14, 2013

@author: leen
'''
import datetime
import pymongo
import logging
import traceback
from webservice.database.mongo_connector import Mongo_Connector,Mongo_UserInfo_Connector, Mongo_Ejabberd_Connector

logger = logging.getLogger('mongoconnection')
logger.addHandler(logging.FileHandler('mongodb_connection.log'))
logger.setLevel(logging.DEBUG)

GUEST_ACCOUNT_EXPIRED_TIME = 24*60*60 #1 day

class Mongo_Guest_UserInfo_Connector(Mongo_UserInfo_Connector):
    
    def __init__(self, host='localhost',port=27017):
        Mongo_Connector.__init__(self, host, port)
        #Mongo_UserInfo_Connector.__init__(self, host, port)
        self._database = self._connection['guest']
        self._userinfo_collection = self._database['userinfo']
        self._userinfo_collection.ensure_index([('username',1)],unique=True)
        """TODO"""
        self._userinfo_collection.ensure_index([('money_last_update',1)],expireAfterSeconds=GUEST_ACCOUNT_EXPIRED_TIME)
        
        
        
class Mongo_Guest_Auth_Connector(Mongo_Connector):
    
    def __init__(self, host='localhost',port=27017):
        Mongo_Connector.__init__(self, host, port)
        self._database = self._connection['guest']
        self._auth_collection = self._database['authentication']
        self._auth_collection.ensure_index([('username',1)],unique=True)
        self._auth_collection.ensure_index([('created_time',1)],expireAfterSeconds=GUEST_ACCOUNT_EXPIRED_TIME)
        
    def create_user(self, username):
        result = None
        username = username.lower()
        _newuser = {'username': username,
                    'created_time': datetime.datetime.utcnow()}
        try:
            result = self._auth_collection.insert(_newuser, safe=True)
        except pymongo.errors.DuplicateKeyError:
            logger.error("Duplicate random guest user")
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")
        except:
            logger.error("Unexpected Error: " + traceback.format_exc())
        return result
    
    def exist_user(self, username):
        result = None
        try:
            result = self._auth_collection.find_one({'username':username})
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")
        except:
            logger.error("Unexpected Error: " + traceback.format_exc())
        return result
        
    def remove_user(self, username):
        """
        Check whether user exist or not. Return user's information if exist, else None.
        """
        result = None
        try:
            result = self._auth_collection.remove({'username':username})
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")
        except:
            logger.error("Unexpected Error: " + traceback.format_exc())
        return result
    
if __name__ == '__main__':
    guest_userinfo = Mongo_Guest_UserInfo_Connector()
    print guest_userinfo.create_user('hihihihi')
    guest_auth = Mongo_Guest_Auth_Connector()
    print guest_auth.create_user('hihihihi')
    print guest_auth.exist_user('hihihihi')