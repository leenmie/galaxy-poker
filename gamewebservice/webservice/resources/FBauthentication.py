'''
Created on Sep 16, 2012

@author: leen
'''
import cherrypy
import urllib2
import json
from recaptcha.client import captcha
from webservice.resources.resource import Resource
from webservice.main_config import CF_FACEBOOK_PREFIX, CF_XMPP_DOMAIN_NAME, CF_FACEBOOK_APPTOKEN, CF_FACEBOOK_APPID
from webservice.tools.utils import multipart_email, to_json, random_string_generator


class FBAuthenticationResource(Resource):
    
    def __init__(self, userinfo_database, session_database):
        self._userinfo_db = userinfo_database
        self._session_db = session_database
    
    def GET(self):
        form_html = "<html><head><title>Log in</title></head><body>"+\
        "Facebook authentication"+\
        "</body></html>"
        return form_html
        
    def POST(self, accesstoken):        
        graph_url = "https://graph.facebook.com/debug_token?input_token={0}&access_token={1}".format(accesstoken, CF_FACEBOOK_APPTOKEN)
        try:
            debug_data = urllib2.urlopen(graph_url).read()            
            json_data = json.loads(debug_data)
            token_data = json_data['data']
            #print token_data
            is_valid = token_data['is_valid']
            if is_valid:                
                app_id = str(token_data['app_id'])
                fb_id = str(token_data['user_id'])            
                if fb_id and (app_id == CF_FACEBOOK_APPID):
                    username = CF_FACEBOOK_PREFIX + fb_id
                    username_full = username
                    if not self._userinfo_db.exist_user(username_full):
                        #create facebook account here                    
                        self._userinfo_db.create_user(username_full)
                    session_id = self._session_db.create_token(username)
                    if session_id:
                        return to_json({'result':0, 'authenticated_token': session_id, 
                                        'userid': username,
                                        'description': 'Token is created successfully.'})            
        except:
            return to_json({'result':1, 'description': 'Error.'})
        return to_json({'result':1, 'description': 'Error.'})
    