'''
Created on Jul 24, 2012

@author: leen
'''
#import string
#import random
import traceback
import logging
import hashlib
import base64
import uuid
import pymongo
#import time
import datetime
from Crypto import Random
from Crypto.Cipher import AES
from webservice.tools.utils import hash_password_salt, random_string_generator
from webservice import main_config

"""configuration values"""
FREE_MONEY = main_config.CF_FREE_MONEY
ENCRYPTION_AES_KEY = main_config.CF_ENCRYPTION_AES_KEY
SECRET_SALT = main_config.CF_SECRET_SALT

EMAIL_VERIFICATION_EXPIRED_TIME = main_config.CF_EMAIL_VERIFICATION_EXPIRED_TIME
EMAIL_VERIFICATION_LIMIT_TIME = main_config.CF_EMAIL_VERIFICATION_LIMIT_TIME
RESET_PASSWORD_EXPIRED_TIME = main_config.CF_RESET_PASSWORD_EXPIRED_TIME
RESET_PASSWORD_LIMIT_TIME = main_config.CF_RESET_PASSWORD_LIMIT_TIME
EXCHANGE_RATE_CASH_MONEY = main_config.CF_EXCHANGE_RATE_CASH_MONEY

logger = logging.getLogger('mongoconnection')
logger.addHandler(logging.FileHandler('mongodb_connection.log'))
logger.setLevel(logging.DEBUG)




class Mongo_Connector():
    """
    A generic wrapper class for mongodb connection
    """
    def __init__(self, host='localhost',port=27017):        
        self._connection = pymongo.Connection(host=host,port=port)
        
    def close(self):
        self._connection.close()

class Mongo_UserInfo_Connector(Mongo_Connector):
    """
    In-Game User Information
    Use in internal game only
    """
    
    def __init__(self, host='localhost',port=27017):
        Mongo_Connector.__init__(self, host, port)
        database_name = 'userinfo'
        
        self._database = self._connection[database_name]
        self._userinfo_collection = self._database['userinfo']
        self._userinfo_collection.ensure_index([('username',1)],unique=True)            
        
    def create_user(self, username, free_money=FREE_MONEY, cash_money=0, avatar_id=0, nickname='ThanBai'):
        result = None
        try:
            username = username.lower()
            current_time = datetime.datetime.utcnow()
            _user_info = {'username': username,
                          'avatar':avatar_id,
                          'money': free_money,
                          'money_last_update': current_time,
                          'cash': cash_money,
                          'cash_last_update': current_time,
                          'total_cash': 0,
                          'free_money_last_update': current_time,
                          'nickname': nickname,
                          }
            result = self._userinfo_collection.insert(_user_info, safe=True)
        except pymongo.errors.DuplicateKeyError:
            logger.error("Duplicate username or email")
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")
        except:
            logger.error("Unexpected Error: " + traceback.format_exc())
            #raise
        #if result:
        #    return _user_info
        return result

    def exist_user(self, username):
        result = None
        try:
            result = self._userinfo_collection.find_one({'username':username})
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")
        except:
            logger.error("Unexpected Error: " + traceback.format_exc())
        return result
    
    def remove_user(self, username):
        result = None
        try:
            result = self._userinfo_collection.remove({'username':username})
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")
        except:
            logger.error("Unexpected Error: " + traceback.format_exc())
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
            logger.error('Money is not a valid integer')
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")                
        except:
            logger.error('Unexpected Error')
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
            logger.error('Money is not a valid integer')
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")                
        except:
            logger.error('Unexpected Error')
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
            print 'Unexpected Error'
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
                                                                {'$inc':{'cash': cash_amount,'total_cash': cash_amount},
                                                                 '$set':{'cash_last_update': datetime.datetime.utcnow()}},
                                                                safe=True, 
                                                                multi=False)
        except ValueError:
            logger.error('Cash is not a valid integer')
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")                
        except:
            logger.error('Unexpected Error')
        return result
    
    def update_userinfo(self, username, updateinfo):
        result = None
        try:
            result = self._userinfo_collection.update({'username': username,}, 
                                                                {'$set': updateinfo},
                                                                safe=True, 
                                                                multi=False)
        except ValueError:
            logger.error('Updateinfo is not valid.')
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")                
        except:
            logger.error('Unexpected Error')
        return result
    
    def convert_cash_to_money(self, username, cash_amount):
        result = None
        try:
            icash_amount = int(cash_amount)
            if icash_amount < 0:
                """cash amount is a natural number"""
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
            logger.error('Cash is not a valid integer')
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")
        except:
            logger.error('Unexpected Error')
        return result
    
class Mongo_Ejabberd_Connector(Mongo_Connector):
    
    def __init__(self, host='localhost',port=27017):
        Mongo_Connector.__init__(self, host, port)
        database_name = 'authentication'
        self._database = self._connection[database_name]
        self._auth_collection = self._database['authentication']
        self._veri_collection = self._database['verification']
        self._resetpass_collection = self._database['resetpassword']

        """ authentication collection's indexes """
        self._auth_collection.ensure_index([('username',1)],unique=True)
        self._auth_collection.ensure_index([('hash_email',1)],unique=True)
        """ verification collection's indexes """
        self._veri_collection.ensure_index([('username',1)],unique=True)
        self._veri_collection.ensure_index([('created_date',1)],expireAfterSeconds=EMAIL_VERIFICATION_EXPIRED_TIME)
        """ reset password collection's indexes """
        self._resetpass_collection.ensure_index([('username',1)],unique=True)
        self._resetpass_collection.ensure_index([('created_date',1)],expireAfterSeconds=RESET_PASSWORD_EXPIRED_TIME)
        
    def create_user(self, username, password, email, phone=None):
        """
        Create an user in authentication database. Username or email is unique in the collection.
        """
        result = None
        username = username.lower()
        try:
            """salt for password's hash"""
            salt = random_string_generator()
            """password's hash"""
            password_hash = hash_password_salt(password, salt)
            """encrypt email with AES"""
            encryption_iv = Random.new().read(AES.block_size)
            cipher = AES.new(ENCRYPTION_AES_KEY, AES.MODE_CFB, encryption_iv)
            encrypted_email_string = ''.join([encryption_iv,cipher.encrypt(email)])
            encrypted_email_base64 = base64.b64encode(encrypted_email_string)            
            hash_email = hashlib.md5('{}{}'.format(email,SECRET_SALT)).hexdigest()
            """encrypt phone with AES"""
            encrypted_phone_base64 = None
            hash_phone = None
            if phone:
                encryption_iv = Random.new().read(AES.block_size)
                cipher = AES.new(ENCRYPTION_AES_KEY, AES.MODE_CFB, encryption_iv)
                encrypted_phone_string = ''.join([encryption_iv,cipher.encrypt(phone)])
                encrypted_phone_base64 = base64.b64encode(encrypted_phone_string)
                hash_phone = hashlib.md5('{}{}'.format(phone,SECRET_SALT)).hexdigest()
            _newuser = {'username': username, 
                        'password': password_hash,
                        'salt': salt,
                        'email': encrypted_email_base64,
                        'hash_email': hash_email,
                        'phone': encrypted_phone_base64,
                        'hash_phone': hash_phone,
                        'verified': False,
                        }
            result = self._auth_collection.insert(_newuser, safe=True)
        except pymongo.errors.DuplicateKeyError:
            logger.error("Duplicate username or email.")
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect.")
        except:
            logger.error("Unexpected Error.")
            #raise
        """if result:
            if not verification_code:
                verification_code = random_string_generator(12)
            verified = self.create_email_verification_code(verification_code, username)
            if not verified:
                logger.error('Cannot create verification code.')"""        
        return result
    
    def create_user_by_email(self, email, password):
        """
        Create an user in authentication database. Username or email is unique in the collection.
        """
        result = None
        email = email.lower()
        try:
            """salt for password's hash"""
            salt = random_string_generator()
            """password's hash"""
            password_hash = hash_password_salt(password, salt)
            """encrypt email with AES"""
            encryption_iv = Random.new().read(AES.block_size)
            cipher = AES.new(ENCRYPTION_AES_KEY, AES.MODE_CFB, encryption_iv)
            encrypted_email_string = ''.join([encryption_iv,cipher.encrypt(email)])
            encrypted_email_base64 = base64.b64encode(encrypted_email_string)            
            hash_email = hashlib.md5('{}{}'.format(email,SECRET_SALT)).hexdigest()
            username = uuid.uuid4().hex
            
            _newuser = {'username': username, 
                        'password': password_hash,
                        'salt': salt,
                        'email': encrypted_email_base64,
                        'hash_email': hash_email,
                        'verified': False,
                        }
            result = self._auth_collection.insert(_newuser, safe=True)
        except pymongo.errors.DuplicateKeyError:
            logger.error("Duplicate username or email.")
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect.")
        except:
            logger.error("Unexpected Error.")
            #raise
        """if result:
            if not verification_code:
                verification_code = random_string_generator(12)
            verified = self.create_email_verification_code(verification_code, username)
            if not verified:
                logger.error('Cannot create verification code.')"""        
        if result:
            return _newuser
    
    def print_user(self, username):
        """
        Read user's information. Validate encrypted data.        
        """
        user = self.exist_user(username)
        if user:
            print 'Username', user['username']
            print 'Password', user['password']
            email_saving = user['email']
            email_encrypted_with_iv = base64.b64decode(email_saving)
            encryption_iv = email_encrypted_with_iv[:AES.block_size]
            encrypted_email = email_encrypted_with_iv[AES.block_size:]
            cipher = AES.new(ENCRYPTION_AES_KEY, AES.MODE_CFB, encryption_iv)
            email_decrypted = cipher.decrypt(encrypted_email)
            print 'Email', email_decrypted
            phone_saving = user['phone']
            if phone_saving:
                phone_encrypted_with_iv = base64.b64decode(phone_saving)
                phone_encryption_iv = phone_encrypted_with_iv[:AES.block_size]
                encrypted_phone = phone_encrypted_with_iv[AES.block_size:]
                cipher = AES.new(ENCRYPTION_AES_KEY, AES.MODE_CFB, phone_encryption_iv)
                phone_decrypted = cipher.decrypt(encrypted_phone)
                print 'Phone', phone_decrypted
    
    def create_email_verification_code(self, code, username):
        """
        create an email's verification code
        Use case: someone create a new user or request to verify their email
        The code should be sent to user's email. 
        """
        if self.is_verified(username):
            return None                
        verified = None        
        try:
            existed_code = self._veri_collection.find_one({'username': username})
            if existed_code:
                created_date = existed_code['created_date']
                delta = datetime.datetime.utcnow() - created_date
                if delta.total_seconds() < EMAIL_VERIFICATION_LIMIT_TIME:
                    return None
                #else:
                """Now mongodb 2.2 do this for us by expiration job"""
                #    self._veri_collection.remove({'username': username}, safe=True)
            verification_code = {
                                 'code': code,
                                 'username': username,                                     
                                 'created_date': datetime.datetime.utcnow(),
                                 }
            verified = self._veri_collection.insert(verification_code, safe=True)
            #print verified
        except pymongo.errors.DuplicateKeyError:
            logger.error("Duplicate verification code")
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")
        except:
            logger.error("Unexpected Error: " + traceback.format_exc())
        return verified
    
    def verify_email(self,code, username):
        """
        verify email using the code user has requested before.
        After verifying email, user can use function which need email (reset password...)
        """
        result = None
        try:
            result = self._veri_collection.find_one({'code': code,'username': username})
            if result:
                created_date = result['created_date']
                delta = datetime.datetime.utcnow() - created_date
                #print delta
                if delta.total_seconds() < EMAIL_VERIFICATION_EXPIRED_TIME:
                    result = self._auth_collection.update({'username': username,}, 
                                                                          {'$set':{'verified':True}},
                                                                          safe=True, 
                                                                          multi=False)
                else:
                    result = None
                self._veri_collection.remove({'code':code, 'username': username}, safe=True)            
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")
        except:
            logger.error("Unexpected Error: " + traceback.format_exc())            
        return result
    
    def request_forgot_password(self, email, reset_code):
        """
        Request a reset code to reset password.
        This code should be sent to user's email. 
        """
        result = None
        try:
            user = self.exist_email(email)
            username = user['username']            
            if user:
                existed_reset = self._database['resetpassword'].find_one({'username': username})
                if existed_reset:
                    created_date = existed_reset['created_date']
                    delta = datetime.datetime.utcnow() - created_date
                    if delta.total_seconds() < RESET_PASSWORD_LIMIT_TIME:
                        return None
                    #else:
                    """Now mongodb 2.2 do this job for us"""
                    #    self._database['resetpassword'].remove({'username': username}, safe=True)                
                reset_password = {'email': email,
                                  'reset_code': reset_code,
                                  'created_date': datetime.datetime.utcnow(), 
                                  }
                result = self._database['resetpassword'].insert(reset_password, safe=True)
                result = reset_password
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")
        except:
            logger.error("Unexpected Error: " + traceback.format_exc())            
        return result
        
    def reset_password(self, email, reset_code, new_password):
        """
        Reset password with the reset code
        """
        result = None
        try:
            existed_reset = self._database['resetpassword'].find_one({'email': email,'reset_code':reset_code})
            if existed_reset:
                created_day = existed_reset['created_date']
                delta = datetime.datetime.utcnow() - created_day
                if delta.total_seconds() < RESET_PASSWORD_EXPIRED_TIME:
                    salt = random_string_generator()
                    password_hash = hash_password_salt(new_password, salt)
                    user = self.exist_email(email)
                    username = user['username']
                    result = self._auth_collection.update({'username': username,}, 
                                                                          {'$set':{'salt':salt, 'password': password_hash}},
                                                                          safe=True, 
                                                                          multi=False)                    
                else:
                    result = None
                """mongodb will delete old reset code for us"""
                self._database['resetpassword'].remove({'email': email,})
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")
        except:
            logger.error("Unexpected Error: " + traceback.format_exc())            
        return result                

    def change_password(self, username, old_password, new_password):
        """
        Change current password to new password
        """
        result = None
        try:
            if self.authenticate_user(username, old_password):
                salt = random_string_generator()
                password_hash = hash_password_salt(new_password, salt)
                result = self._auth_collection.update({'username': username,}, 
                                                                      {'$set':{'salt':salt, 'password': password_hash}},
                                                                      safe=True, 
                                                                      multi=False)
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")
        except:
            logger.error("Unexpected Error: " + traceback.format_exc())            
        return result
            
    def authenticate_user(self, username, password):
        """
        Authenticate with username and password
        """
        result = False
        user = self.exist_user(username)
        if user:
            salt = user['salt']
            if user['password'] == hash_password_salt(password, salt):
                result = True
        return result
    
    def authenticate_email(self, email, password):
        """
        Authenticate with username and password
        """
        result = False
        user = self.exist_email(email)
        if user:
            salt = user['salt']
            if user['password'] == hash_password_salt(password, salt):
                result = user
        return result
    
    def is_verified(self, username):
        result = False
        user = self.exist_user(username)
        if user:
            result = user['verified']
        return result
    
    def exist_user(self, username):
        """
        Check whether user exist or not. Return user's information if exist, else None.
        """
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
    
    def exist_email(self, email):
        """
        Check whether user exist or not. Return user's information if exist, else None.
        """
        result = None
        hash_email = hashlib.md5('{}{}'.format(email,SECRET_SALT)).hexdigest()
        try:
            result = self._auth_collection.find_one({'hash_email':hash_email})
        except pymongo.errors.AutoReconnect:
            logger.error("Auto reconnect")
        except:
            logger.error("Unexpected Error: " + traceback.format_exc())
        return result            

if __name__ == '__main__':
    """
    COUNT = 200
    c = Mongo_Ejabberd_Connector()
    import time
    current_time = time.time()
    for _ in xrange(0, COUNT):
        username = random_string_generator(random.randint(10,20))
        password = '1234'
        email = ''.join([username,'@gmail.com'])
        phone = random_string_generator(random.randint(10,20))
        c.create_user(username, password, email, phone)
    delta = time.time() - current_time
    print 'Speed', COUNT/delta, 'actions per second.'
    """
        
    c = Mongo_Ejabberd_Connector()
    #yy = c.create_user('test100','123456','hehe2@gmail.com')
    yy = c.create_user('test200','123456','hehe3@gmail.com','12345678')
    #c.print_user('test200')
    #print c.verify_email('DGxfeB7qIgcr', 'test200')
    #print c.request_forgot_password('test200', random_string_generator(12))
    #print c.reset_password('test200', 'hrEF0wynjnaM', '654321')
    #print c.change_password('test200', '654321', 'abcdef')
    #print c.authenticate_user('test200', 'abcdef')
    #print yy
    
    #zz = c.exist_user('hehehe')
    #print zz
    #aa = c.authenticate_user('hehehe88','1234')
    #print aa

    #c.check_index()