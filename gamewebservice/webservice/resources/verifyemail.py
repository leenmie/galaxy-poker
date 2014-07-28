'''
Created on Sep 16, 2012

@author: leen
'''
from webservice.tools.utils import to_json
from webservice.resources.resource import Resource

class VerifyEmailResource(Resource):
    
    def GET(self, verification_code=None, username=None):
        if verification_code and username:
            res = self._database.verify_email(verification_code, username)
            if res:
                return to_json({'result': 0, 'description': 'Verification is successful.'})
            else:
                return to_json({'result': 1, 'description': 'Verification failed.'})
        else:
            form_html = '<html><head><title>Verify Email</title></head><body>'+\
            '<form name="input" method="get">'+\
            'Username: <input type="text" name="username" />'+\
            'Code: <input type="text" name="verification_code" />'+\
            '<input type="submit" value="Submit" />'+\
            '</form>' +\
            '</body></html>'
            return form_html
