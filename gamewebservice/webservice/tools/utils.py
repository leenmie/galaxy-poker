'''
Created on Sep 7, 2012

@author: leen
'''
import random
import hashlib
import string
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from webservice.main_config import CF_SMTP_HOST, CF_SMTP_USER, CF_SMTP_PASSWORD

CHARS = string.ascii_letters + string.digits

def random_string_generator(size=8):
    return ''.join(random.SystemRandom().choice(CHARS) for _ in range(size))

def hash_password_salt(password, salt):
    return hashlib.sha256(''.join([password, salt])).hexdigest()

def to_json(content):
    return json.dumps(content)

def multipart_email(from_address, to_address, subject, text, html=None) :
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address    
    part1 = MIMEText(text,'plain')
    msg.attach(part1)
    if html:
        part2 = MIMEText(html,'html')   
        msg.attach(part2)
    return msg            

def send_email(from_address, to_address, mime_content, smtp=None, quit_after=False):
    sent = True
    try:
        if not smtp:
            smtp = smtplib.SMTP(CF_SMTP_HOST)
            smtp.starttls()
            smtp.login(CF_SMTP_USER, CF_SMTP_PASSWORD)
        smtp.sendmail(from_address, [to_address,], mime_content.as_string())
    except:
        sent = False
    try:
        if quit_after:
            smtp.quit()
    except:
        pass
    return sent
    