'''
Created on Sep 16, 2012

@author: leen
'''
from webservice.tools.utils import to_json
from webservice.resources.resource import Resource
from webservice.resources import XMPP_DOMAIN_NAME, REGEX_PASSWORD

class ChangePasswordResource(Resource):
    
    def GET(self):
        form_html = '<html><head><title>Change Password</title></head><body>'+\
        '<form name="input" method="post">'+\
        'Username: <input type="text" name="username" />'+\
        'Current Password: <input type="password" name="oldpassword" />'+\
        'New Password: <input type="password" name="newpassword" />'+\
        '<input type="submit" value="Submit" />'+\
        '</form>' +\
        '</body></html>'
        return form_html
    
    def POST(self,username, oldpassword, newpassword):
        username = username.lower()
        if not REGEX_PASSWORD.match(newpassword):
            return to_json({'result': 2, 'description': 'Password can contain from 6 to 32 characters.'})
        res = self._database.change_password(username, oldpassword, newpassword)
        if res:
            return to_json({'result': 0, 'description': 'Password changed.'})
        else:
            return to_json({'result': 1, 'description': 'Changing password failed.'})
