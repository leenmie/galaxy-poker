'''
Created on Sep 15, 2012

@author: leen
'''
from webservice.tools.utils import to_json

class Resource(object):
    exposed = True
    
    def __init__(self, auth_database = None):
        self._database = auth_database
    
    def GET(self):
        return to_json({'message':'Welcome to Cacafefe\'s services.'})