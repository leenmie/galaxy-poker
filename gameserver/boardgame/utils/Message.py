class Message:
    def __init__(self,from_user, msg):
        self._from_user = from_user
        self._body = msg
        
    def set_body(self, body):
        self._body = body
        
    def get_body(self):
        return self._body
    
    def get_from_user(self):
        return self._from_user
    