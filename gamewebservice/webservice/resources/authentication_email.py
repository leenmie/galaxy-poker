'''
Created on Sep 16, 2012

@author: leen
'''
import cherrypy
from recaptcha.client import captcha
from webservice.resources.resource import Resource
from webservice.resources import RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY,\
                                REGEX_USERNAME, REGEX_PASSWORD, REGEX_EMAIL, REGEX_PHONE
from webservice.resources import push_email_to_sending_queue
from webservice.tools.utils import multipart_email, to_json, random_string_generator

class AuthenticationEmailResource(Resource):
    
    def __init__(self, auth_database, session_database):
        self._auth_db = auth_database
        self._session_db = session_database
    
    def GET(self):
        form_html = "<html><head><title>Log in</title></head><body>"+\
        "<form name=\"input\" method=\"post\">"+\
        'Email: <input type="text" name="email" />'+\
        'Password: <input type="text" name="password" />'+\
        "<input type=\"submit\" value=\"Submit\" />"+\
        "</form>" +\
        "</body></html>"
        return form_html
        
    def POST(self, email, password):
        email = email.lower()
        authenticated = self._auth_db.authenticate_email(email, password)
        if authenticated:
            username = authenticated['username']
            session_id = self._session_db.create_token(username)
            if session_id:
                return to_json({'result':0, 'authenticated_token': session_id,
                                'userid': username, 
                                'description': 'Token is created successfully.'})
        return to_json({'result':1, 'description': 'Error.'})