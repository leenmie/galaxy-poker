'''
Created on Aug 6, 2012

@author: leen
'''
import pymongo
#import time
import datetime
import traceback
from boardgame.main_config import DEFAULT_FREE_MONEY, DEFAULT_FREE_MONEY_TIME, EXCHANGE_RATE_CASH_MONEY, GUEST_ACCOUNT_EXPIRED_TIME

FREE_MONEY = DEFAULT_FREE_MONEY
SECONDS_IN_A_DAY = DEFAULT_FREE_MONEY_TIME
#EXCHANGE_RATE_CASH_MONEY = 1000
#GUEST_ACCOUNT_EXPIRED_TIME = 24*60*60 #1 day


class Mongo_Connector():
    def __init__(self, host='localhost',port=27017):        
        self._connection = pymongo.Connection(host=host,port=port)
                #logging.debug('Databases: %s',str(self._connection.database_names()))    
        
    def close(self):
        self._connection.close()

        
class Mongo_UserInfo_Connector(Mongo_Connector):
    def __init__(self, host='localhost',port=27017):
        database_name = 'userinfo'
        Mongo_Connector.__init__(self, host, port)
        self._database = self._connection[database_name]
        self._userinfo_collection = self._database['userinfo']
        self._userinfo_collection.ensure_index([('username',1)],unique=True)            
        
    def create_user(self, username, free_money=FREE_MONEY, cash_money=0):
        result = None
        try:
            current_time = datetime.datetime.utcnow()
            _user_info = {'username': username,
                          'avatar':0,
                          'money': free_money,
                          'money_last_update': current_time,
                          'cash': cash_money,
                          'cash_last_update': current_time,
                          'cash_total': 0,
                          'free_money_last_update': current_time,
                          }
            result = self._userinfo_collection.insert(_user_info, safe=True)
        except pymongo.errors.DuplicateKeyError:
            print "Duplicate username or email"
        except pymongo.errors.AutoReconnect:
            print "Auto reconnect"
        except:
            print "Unexpected Error" + traceback.format_exc()
            #raise
        return result

    def exist_user(self, username):
        result = None
        try:
            result = self._userinfo_collection.find_one({'username':username})
        except pymongo.errors.DuplicateKeyError:
            print "Duplicate username or email"
        except pymongo.errors.AutoReconnect:
            print "Auto reconnect"
        except:
            print "Unexpected Error" + traceback.format_exc()
        return result            
    
    def update_user_money(self, username, old_money, new_money):
        result = None                
        #user = self.exist_user(username)
        try:
            money_amount = int(new_money)
            if money_amount < 0:
                money_amount = 0
            #if user:
            result = self._userinfo_collection.update({'username': username, 'money': old_money}, 
                                                                {'$set':{'money': money_amount, 'money_last_update': datetime.datetime.utcnow()}},
                                                                safe=True, 
                                                                multi=False)
        except ValueError:
            print 'Money is not a valid integer'
        except pymongo.errors.AutoReconnect:
            print "Auto reconnect"                
        except:
            print 'Unexpected Error' + traceback.format_exc()
        return result

    def increase_user_money(self, username, amount):
        result = None                
        #user = self.exist_user(username)
        try:
            money_amount = int(amount)
            #if money_amount < 0:
            #    money_amount = 0
            #if user:
            result = self._userinfo_collection.update({'username': username,}, 
                                                                {'$inc':{'money': money_amount}, '$set':{'money_last_update': datetime.datetime.utcnow()}},
                                                                safe=True, 
                                                                multi=False)
        except ValueError:
            print 'Money is not a valid integer'
        except pymongo.errors.AutoReconnect:
            print "Auto reconnect"                
        except:            
            print 'Unexpected Error' + traceback.format_exc()
        return result
    
    def get_user_money(self, username):
        result = -1
        try:            
            #if user:
            user = self._userinfo_collection.find_one({'username': username}, 
                                                            {'money': 1},
                                                            )
            result = int(user['money'])
        except ValueError:
            print 'Money is not a valid integer'
        except pymongo.errors.AutoReconnect:
            print "Auto reconnect"                
        except:            
            print 'Unexpected Error' + traceback.format_exc()
        return result

    def get_user_free_money_last_update(self, username):
        result = -1
        try:            
            #if user:
            user = self._userinfo_collection.find_one({'username': username}, 
                                                            {'free_money_last_update': 1},
                                                            )
            result = user['free_money_last_update']
        except ValueError:
            print 'Money is not a valid integer'
        except pymongo.errors.AutoReconnect:
            print "Auto reconnect"                
        except:
            print 'Unexpected Error' + traceback.format_exc()
        return result

    
    def give_free_money(self, username, free_money=FREE_MONEY, time_out=SECONDS_IN_A_DAY):
        result = None
        try:
            user = self._userinfo_collection.find_one({'username': username}, 
                                                            {'money': 1, 'free_money_last_update': 1},                                                            
                                                            )
            if user:
                current_time = datetime.datetime.utcnow()
                free_money_last_update = user['free_money_last_update']
                if (current_time - free_money_last_update).total_seconds() > time_out:
                    money = int(user['money'])
                    if money < free_money:
                        result = self._userinfo_collection.update({'username': username, 'money': money}, 
                                                                            {'$set':{'money': free_money, 'money_last_update': current_time, 'free_money_last_update': current_time}},
                                                                            safe=True, 
                                                                            multi=False)
        except ValueError:
            print 'Money is not a valid integer'
        except pymongo.errors.AutoReconnect:
            print "Auto reconnect"                
        except:
            print 'Unexpected Error' + traceback.format_exc()
        return result
    
    def get_user_avatar(self, username):
        result = -1
        try:                        
            user = self._userinfo_collection.find_one({'username': username}, 
                                                            {'avatar': 1},
                                                            )
            result = int(user['avatar'])
        except ValueError:
            print 'Money is not a valid integer'
        except pymongo.errors.AutoReconnect:
            print "Auto reconnect"                
        except:
            print 'Unexpected Error' + traceback.format_exc()
        return result
    
    def update_user_avatar(self, username, iAvatar):
        result = None                
        #user = self.exist_user(username)
        try:            
            result = self._userinfo_collection.update({'username': username}, 
                                                                {'$set':{'avatar': iAvatar}},
                                                                safe=True, 
                                                                multi=False)
        except ValueError:
            print 'Money is not a valid integer'
        except pymongo.errors.AutoReconnect:
            print "Auto reconnect"                
        except:
            print 'Unexpected Error' + traceback.format_exc()
        return result
    
    def increase_user_cash(self, username, amount):
        result = None                
        #user = self.exist_user(username)
        try:
            cash_amount = int(amount)
            if cash_amount < 0:
                return None
            #if user:
            result = self._userinfo_collection.update({'username': username,}, 
                                                                {'$inc':{'cash': cash_amount,'total_cash': cash_amount}, '$set':{'cash_last_update': datetime.datetime.utcnow()}},
                                                                safe=True, 
                                                                multi=False)
        except ValueError:
            print 'Cash is not a valid integer'
        except pymongo.errors.AutoReconnect:
            print "Auto reconnect"           
        except:
            print 'Unexpected Error' + traceback.format_exc()
        return result
    
    def convert_cash_to_money(self, username, cash_amount):
        result = None
        try:
            icash_amount = int(cash_amount)
            if icash_amount <= 0:
                """cash amount is a positive number"""
                return None
            current_value = self._userinfo_collection.find_one({'username': username}, {'cash': 1,'money': 1})
            #current_money = current_value['money']
            current_cash = current_value['cash']
            if current_cash < icash_amount:
                """the converting cash is bigger than your cash"""
                return None
            converted_money = icash_amount * EXCHANGE_RATE_CASH_MONEY
            
            result = self._userinfo_collection.update({'username': username, 'cash': current_cash},
                                               {'$inc':{'cash': -(icash_amount), 'money':converted_money}},
                                               safe=True,
                                               multi=False)
            
        except ValueError:
            print 'Cash is not a valid integer'
        except pymongo.errors.AutoReconnect:
            print "Auto reconnect"
        except:
            print 'Unexpected Error' + traceback.format_exc()
        return result

class Mongo_Guest_UserInfo_Connector(Mongo_UserInfo_Connector):    
    def __init__(self, host='localhost',port=27017):
        Mongo_Connector.__init__(self, host, port)
        self._database = self._connection['guest']
        self._userinfo_collection = self._database['userinfo']
        self._userinfo_collection.ensure_index([('username',1)],unique=True)
        self._userinfo_collection.ensure_index([('money_last_update',1)],expireAfterSeconds=GUEST_ACCOUNT_EXPIRED_TIME)

if __name__ == '__main__':
    db = Mongo_UserInfo_Connector()
    db.create_user('test100@ubuntu')
    db.create_user('test200@ubuntu')
    db.create_user('test300@ubuntu')
    db.create_user('test400@ubuntu')
    money = db.get_user_money('test100@ubuntu')    
    print money
    xx = db.get_user_free_money_last_update('test100@ubuntu')
    print xx
    xx = db.exist_user('test100@ubuntu')
    print xx
    money = db.get_user_money('test400@ubuntu')
    db.update_user_money('test400@ubuntu', money, 200)