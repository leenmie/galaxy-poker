from ZODB import FileStorage, DB
from BTrees.OOBTree import OOBTree
import transaction

class ZODB_Connector():
    def __init__(self):
        storage = FileStorage.FileStorage('game_list.fs')
        db = DB(storage)
        self._conn = db.open()        
        dbroot = self._conn.root()
        if not dbroot.has_key('userlist'):            
            dbroot['userlist'] = OOBTree()
        self._user_list = dbroot['userlist']
        if not dbroot.has_key('roomlist'):
            dbroot['roomlist'] = OOBTree()
        self._room_list = dbroot['roomlist']            
    
    def add_room(self, room):
        self._room_list[room.get_id()]=room
        transaction.commit()
        
    def clear_room(self):
        dbroot = self._conn.root()
        del dbroot['roomlist']
        dbroot['roomlist'] = OOBTree()
        self._room_list = dbroot['roomlist']
        transaction.commit()
    
    def list_room(self):
        return self._room_list.keys()
    
    
if __name__=='__main__':
    import sys
    if '../' not in sys.path:
        sys.path.append('../')
    from Room import Room
    import random,time
    
    connector = ZODB_Connector()
    #for _ in range(1000000):
    #    room = Room(100)
    #    connector.add_room(room)
    connector.clear_room()
    before = time.time()
    ll = connector.list_room()
    len_list = len(ll)
    after = time.time()
    print after - before
#    for _ in range(100):
#        rindex = random.randint(0,len_list-1)
#        print(ll[rindex])
#    
