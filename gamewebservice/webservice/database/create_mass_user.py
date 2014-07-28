'''
Created on Aug 26, 2012

@author: leen
'''
from mongo_connector import Mongo_Ejabberd_Connector, Mongo_UserInfo_Connector
import random

if __name__ == '__main__':
    
    auth_db = Mongo_Ejabberd_Connector()
    userinfo_db = Mongo_UserInfo_Connector()

    f = open('userlist.txt','r')
    lines = f.readlines()
    print len(lines)
    for l in lines:
        mm = l.split()
        username = mm[0]
        password = mm[1]
        auth_db.create_user(username, password, ''.join([username,'@bot.cacafefe.com']))
        ava_id = random.randint(0,3)
        userinfo_db.create_user(username, avatar_id=ava_id)
    f.close()
