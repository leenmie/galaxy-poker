'''
Created on Sep 19, 2012

@author: leen
'''
import cherrypy
from cherrypy.lib import file_generator
from webservice.resources.resource import Resource
from webservice.tools.image import CaptchaCardImage
from webservice.tools.utils import to_json
from webservice.tools.captchamanager import CAPTCHA_DEFAULT

class ImageCardCaptchaResource(Resource):
    #captcha_manager = None
    def __init__(self, captcha_database, captcha_manager):
        self._captcha_database = captcha_database
        self._captcha_manager = captcha_manager
    
    def GET(self, turingtestid=None):
        captcha_con = self._captcha_database
        #captcha_con = Captcha_Session_Connector()
        if 'X-Real-IP' in cherrypy.request.headers:
            ip_remote = cherrypy.request.headers['X-Real-IP']
        else:
            ip_remote = cherrypy.request.remote.ip
        
        if not turingtestid:
            self._captcha_manager.update_captcha_count(ip_remote)
            if self._captcha_manager.get_captcha_id(ip_remote) != CAPTCHA_DEFAULT:
                return to_json({'result': 3,'description':'Please use recaptcha.'})                                                       
            captcha_card_image = CaptchaCardImage(length=3)
            captcha_image = captcha_card_image.get_image()
            captcha_value = captcha_card_image.get_encode_string_values()
            captcha_insert = captcha_con.create_captcha(captcha_image, captcha_value)
            if captcha_insert:
                result = {'result': 0,'turingtestid': captcha_insert['turingtestid'], 'description':'Successful.'}
                return to_json(result)
            else:
                return to_json({'result': 9,'description':'Unknown error.'})
        else:            
            result = captcha_con.get_captcha(turingtestid)
            #buffering = ''
            if result:
                data = result['image']
                cherrypy.response.headers['Content-Type'] = "image/jpeg"
                #return file_generator(data)
                return str(data)
            else:
                return 'Error'
    
    #def POST(self, turingtestid, captcha_answer):
    #    captcha_con = self._captcha_connection
    #    captcha_result = captcha_con.verify_captcha(turingtestid, captcha_answer)
    #    if captcha_result:
            
            #buffering = StringIO()
            #captcha_image.save(buffering,"JPEG")
            #buffering.seek(0)

def get_card_string(value):
    special_chars = ['&#x2660;', '&#x2663;', '&#x2666;', '&#x2665;']
    _number = (value / 4)+1
    _kind = value % 4
    string_number = ''
    if _number >=2 and _number <=10:
        string_number = str(_number)
    elif _number == 1:
        string_number = 'A'
    elif _number == 11:
        string_number = 'J'
    elif _number == 12:
        string_number = 'Q'
    elif _number == 13:
        string_number = 'K'
    return string_number + special_chars[_kind]            
                    
class ImageCardCaptchaExampleResource(Resource):
    def __init__(self, captcha_database):
        self._captcha_database = captcha_database
            
    def GET(self, turingtestid=None):
        #special_chars = ['&#x2660;', '&#x2663;', '&#x2666;', '&#x2665;']
        #spade_char = '&#x2660;'
        #club_char = '&#x2663;'
        #diamond_char = '&#x2666;'
        #heart_char = '&#x2665;'
        if not turingtestid:
            return 'We need GET parameter turingtestid.'   
        option_input = ''
        for v in range(52):
            _kind = v % 4
            if _kind > 1:
                option = '<option value="{0}" style="color:red">{1}</option>'.format(v, get_card_string(v))
            else:
                option = '<option value="{0}" style="color:black">{1}</option>'.format(v, get_card_string(v))
            option_input += option
        select_input = ''
        for _i in range(3):
            select_input += '<select id="{0}">{1}'.format('captcha_answer_'+str(_i),option_input)            
            select_input += '</select>'
        
        html = '''<html>
        <head>
        <title>Captcha Example</title>
        <script>
        function displayResult()
          {{
          var captcha_answer = document.getElementById("captcha_answer_0").value + "|"+
                              document.getElementById("captcha_answer_1").value + "|"+
                              document.getElementById("captcha_answer_2").value;
          document.getElementById("recaptcha_response_field").value = captcha_answer;
          document.forms["captcha_example"].submit();
          }}
        </script>
        </head>
        <body>
            <form id="captcha_example" name="captcha_example"
                method="post" action="http://localhost:8000/captcha/example">
            <img src="http://localhost:8000/captcha?turingtestid={0}"></img><br/>
            {1} <br/>
            <input type="hidden" name="recaptcha_challenge_field" id="recaptcha_challenge_field" value="{0}"></input>
            <input type="hidden" name="recaptcha_response_field" id="recaptcha_response_field" value="123"></input>
            </form>
            <br/>
            <button type="button" onclick="displayResult()">Display</button>            
        </body>
        </html>
        '''.format(turingtestid, select_input)
        return html
    
    def POST(self, recaptcha_challenge_field, recaptcha_response_field):
        verify = self._captcha_database.verify_captcha(recaptcha_challenge_field, recaptcha_response_field)
        if verify:
            return 'Matched.'
        return 'Not matched.'
    