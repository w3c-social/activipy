import json
from dbm import gnu as gdbm


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

    @classmethod
    def open(cls, filename):
        return cls(gdbm.open(filename, 'c'))

    def close(self):
        self.db.close()


# Each of these returns the full object inserted into dbm

def dbm_insert_method(asobj, db, private=None):
    pass

def dbm_update_method(asobj, db, private=None):
    pass

def dbm_upsert_method(asobj, db, private=None):
    pass

def dbm_delete_method(asobj, db):
    pass




# Now, DBM with private data edition

def privatedbm_insert_method(asobj, db, private=None):
    pass

def privatedbm_update_method(asobj, db, private=None):
    pass

def privatedbm_upsert_method(asobj, db, private=None):
    pass

def privatedbm_delete_method(asobj, db):
    pass
