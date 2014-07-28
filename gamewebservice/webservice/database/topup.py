'''
Created on Oct 1, 2012

@author: leen
'''
import pymongo
import logging
import traceback
from webservice.database.mongo_connector import Mongo_Connector



logger = logging.getLogger('mongoconnection')
logger.addHandler(logging.FileHandler('mongodb_connection.log'))
logger.setLevel(logging.DEBUG)

class TopUpConnector(Mongo_Connector):
    def __init__(self, host='localhost',port=27017):
        Mongo_Connector.__init__(self, host, port)
        self._database = self._connection['logTopUp']
        self._nganluong_collection = self._database['nganluong']
        self._error_collection = self._database['error']
        self._nganluong_collection.ensure_index([('ref_code',1)],unique=True)
        self._error_collection.ensure_index([('ref_code',1)],unique=True)
        #self._token_collection.ensure_index([('created_time',1)], expireAfterSeconds=EXPIRED_SESSION_TIME)
        
    def log_nganluong(self, response_results):
        """error_code|merchant_id|transaction_id|amount|pin_card|
        type_card|ref_code| merchant_account|client_fullname|client_email|client_mobile"""
        result = None
        try:        
            error_code = response_results[0]
            merchant_id = response_results[1]
            transaction_id = response_results[2]
            amount = None
            try:
                amount = int(response_results[3])
            except:
                pass
            pin_card = response_results[4]
            type_card = response_results[5]
            ref_code = response_results[6]
            merchant_account = response_results[7]
            log_record = {
                          'error_code': error_code,
                          'merchant_id': merchant_id,
                          'transaction_id': transaction_id,
                          'amount': amount,
                          'pin_card': pin_card,
                          'type_card': type_card,
                          'ref_code': ref_code,
                          'merchant_account': merchant_account,                                              
                        }
            result = self._nganluong_collection.insert(log_record, safe=True)
        
        except pymongo.errors.DuplicateKeyError:
            logger.error("Duplicate ref_code")
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")
            """run it again"""
            self.log_nganluong(response_results)
        except:
            logger.error("Unexpected Error: "+ traceback.format_exc())
            #raise
        return result
    
    def log_error(self, ref_code, info, reason):
        result = None
        try:
            log_record = {
                          'ref_code':ref_code,
                          'info':info,
                          'reason':reason
                          }
            result = self._error_collection.insert(log_record, safe=True)        
        except pymongo.errors.DuplicateKeyError:
            logger.error("Duplicate ref_code")
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")
            """run it again"""
            self.log_error(ref_code, info, reason)
        except:
            logger.error("Unexpected Error: "+  traceback.format_exc())
        return result
        