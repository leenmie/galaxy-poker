'''
Created on Aug 21, 2012

@author: leen
'''
from mongo_connector import Mongo_Connector
import pymongo
import logging
import datetime
EXPIRED_TIME_VERIFICATION = 24*60*60*7#a week
EXPIRED_TIME_RESETPASS = 24*60*60*7#a week
logging.basicConfig(filename = 'cleaner.log', level = logging.DEBUG)

class Mongo_Cleaner(Mongo_Connector):
    def __init__(self, database_name='authentication', host='localhost', port=27017):
        Mongo_Connector.__init__(self, database_name, host, port)
        self._database = self._connection[database_name]
        self._verification_collection = 'verification'
        self._resetpassword_collection = 'resetpassword'
        
    def clear_expired(self):
        try:
            today = datetime.datetime.now()
            verification_expired_time = today - datetime.timedelta(seconds = EXPIRED_TIME_VERIFICATION)
            self._database[self._verification_collection].remove({'created_date':{'$lt':verification_expired_time}}, safe=True)
            resetpass_expired_time = today - datetime.timedelta(seconds = EXPIRED_TIME_RESETPASS)
            self._database[self._verification_collection].remove({'created_date':{'$lt':resetpass_expired_time}}, safe=True)
        except pymongo.errors.AutoReconnect:
            logging.error("Auto reconnect")
        except:
            logging.error("Unexpected Error")

if __name__ == '__main__':
    cleaner = Mongo_Cleaner()
    cleaner.clear_expired()