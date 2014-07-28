import smtplib
from Queue import Queue
from webservice.main_config import CF_SMTP_HOST, CF_SMTP_USER, CF_SMTP_PASSWORD


MAX_MESSAGE_IN_QUEUE = 10000

class EmailManager():
    def __init__(self, max_message = 200):
        self._Queue = Queue(MAX_MESSAGE_IN_QUEUE)
        self._max_message = max_message
        
    def enqueue(self, msg):
        try:
            self._Queue.put(msg)
        except:
            return None
        return msg
        
    def send_email(self, smtp, msg):
        from_address = msg['From']
        to_address = msg['To']
        smtp.sendmail(from_address, [to_address,], msg.as_string())
        
    def send_queue(self):
        if self._Queue.empty():
            return
        try:
            smtp = smtplib.SMTP(CF_SMTP_HOST)
            smtp.starttls()
            smtp.login(CF_SMTP_USER, CF_SMTP_PASSWORD)
                        
            for _ in range(self._max_message):
                msg = self._Queue.get_nowait()
                self.send_email(smtp, msg)
            smtp.close()
        except:
            pass
        