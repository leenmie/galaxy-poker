'''
Created on Mar 13, 2012

@author: leen
'''
import unittest
import sys
import time
from boardgame.models.couchbase_connector import CouchBaseConnector


class CouchBaseTestCase(unittest.TestCase):
    
    test_name = 'test001'
    
    @classmethod
    def setUpClass(self):
        self._connector = CouchBaseConnector()    
    
    @classmethod
    def tearDownClass(self):
        #self._connector.close()
        pass        
    
    def setUp(self):          
        self._connector.delete_user(self.test_name)

    def tearDown(self):                        
        self._connector.delete_user(self.test_name)
        
    def test_user_create(self):                
        user = self._connector.create_user(self.test_name)
        self.assertIsNotNone(user, 'Creating user error')        
        
    def test_user_get(self):
        user = self._connector.create_user(self.test_name)
        user = self._connector.get_user(self.test_name)
        self.assertIsNotNone(user, 'Getting user error')
        self.assertEqual(user.username, self.test_name, 'Invalid username')
        
    def test_read_speed(self):
        count = 100000
        __ = self._connector.create_user(self.test_name)
        __ = self._connector.get_user(self.test_name)        
        cur_time = time.time()
        for _ in range(count):
            self._connector.get_user(self.test_name)
        delta = time.time() - cur_time
        print 'Read per second:', count/delta
    
    def test_write_speed(self):
        count = 100000
        cur_time = time.time()
        for _ in range(count):            
            self._connector.create_user(self.test_name+str(_))
        delta = time.time() - cur_time
        print 'Write per second:', count/delta

if __name__ == "__main__":
    unittest.main()