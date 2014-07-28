'''
Created on Mar 13, 2012

@author: leen
'''
import cPickle
import uuid
import couchbase.couchbaseclient
from couchbase.couchbaseclient import VBucketAwareCouchbaseClient, MemcachedError
from couchbase.couchbaseclient import MemcachedClient
from boardgame.models.player import ModelPlayerBasic

URL = "http://ubuntu:8091/pools/default"
BUCKET_GAME = "game_user"
BUCKET_GAME_PASSWORD = "game" 

class MemcacheConnector():
    def __init__(self):
        self._connection = MemcachedClient(host='127.0.0.1',port=10000)
         
        #self._connection = VBucketAwareCouchbaseClient(URL, 'route')
        
    def get(self, key):
        value = None
        try:
            _, _, value =  self._connection.get(key, vbucket=0)
        except:
            pass
            #raise
        return value
        
    def add(self, key, value):
        return self._connection.add(key= key, exp = 0, flags = 0, val= value, vbucket=0)
    
    def set(self, key, value):
        return self._connection.set(key= key, exp = 0, flags = 0, val= value, vbucket=0)
        #return self._connection.set(key, 0, 0, value)
    
    def delete(self, key):
        try:
            self._connection.delete(key, vbucket = 0)
        except:
            pass
    
    def close(self):
        self._connection.close()
        
    def flush(self):
        self._connection.flush()


class CouchBaseConnector():
    
    def __init__(self):
        #self._connection_user = VBucketAwareCouchbaseClient(URL, BUCKET_GAME, BUCKET_GAME_PASSWORD, False)
        self._connection_user = MemcachedClient(host='127.0.0.1',port=11000)
    
    def get_user(self, username):
        #print "Couchbase ...", username, type(username)        
        connection = self._connection_user
        try:
            user = connection.get(username)
        except MemcachedError as error:
            if error.status == couchbase.couchbaseclient.MemcachedConstants.ERR_NOT_FOUND:
                user = None
        if user:            
            user = cPickle.loads(user[2]) 
        return user
    
    def create_user(self, username, deposit_money = 0, active_money = 10000):
        connection = self._connection_user
        player = ModelPlayerBasic()
        player.username = username
        player.deposit_money = deposit_money
        player.active_money = active_money
        picklestr = cPickle.dumps(player)       
        try:
                #newid = uuid.uuid4().get_hex()
            connection.add(username, 0, 0, picklestr)
#            except MemcachedError as error:
#                if error.status == couchbase.couchbaseclient.MemcachedConstants.ERR_EXISTS:
#                    pass
        except:
            return None        
        return player
    
    def delete_user(self, username):
        connection = self._connection_user
        try:
            connection.delete(username)
        except:
            pass
    
    def close(self):
        self._connection_user.done()