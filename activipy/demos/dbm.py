import json
from dbm import gnu as gdbm

from activipy import core, vocab


class JsonDBM(object):
    """
    json wrapper around a gdbm database
    """
    def __init__(self, db):
        self.db = db

    def __getitem__(self, key):
        return json.loads(self.db[key.encode('utf-8')].decode('utf-8'))

    def __setitem__(self, key, value):
        self.db[key.encode('utf-8')] = json.dumps(value)

    def __delitem__(self, key):
        del self.db[key.encode('utf-8')]

    @classmethod
    def open(cls, filename):
        return cls(gdbm.open(filename, 'c'))

    def close(self):
        self.db.close()



# Each of these returns the full object inserted into dbm

def dbm_fetch(id, db):
    return core.ASObj(db[id])

def dbm_insert(asobj, db, private=None):
    pass

def dbm_update(asobj, db, private=None):
    pass

def dbm_upsert(asobj, db, private=None):
    pass

def dbm_delete(asobj, db):
    pass




# Insert/update special methods for Activity / IntransitiveActivity
# objects




# Now, DBM with private data edition

def privatedbm_fetch(db, id):
    pass

def privatedbm_insert(asobj, db, private=None):
    pass

def privatedbm_update(asobj, db, private=None):
    pass

def privatedbm_upsert(asobj, db, private=None):
    pass

def privatedbm_delete(asobj, db):
    pass
