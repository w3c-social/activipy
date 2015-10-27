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

    def __contains__(self, key):
        return key in self.db

    @classmethod
    def open(cls, filename):
        return cls(gdbm.open(filename, 'c'))

    def close(self):
        self.db.close()

    def get(self, key, default=None):
        if key in self.db:
            return self[key]
        else:
            return default


# Each of these returns the full object inserted into dbm

def dbm_fetch(id, db):
    return core.ASObj(db[id])

def dbm_save(env, asobj, db):
    assert asobj.id is not None
    new_val = asobj.json()
    db[asobj.id] = new_val
    return new_val

def dbm_delete(env, asobj, db):
    assert asobj.id is not None
    del db[asobj.id]


dbm_save_method = core.MethodId(
    "save", "Save object to the DBM store.",
    core.handle_one)
dbm_delete_method = core.MethodId(
    "delete", "Delete object from the DBM store.",
    core.handle_one)

DbmEnv = core.Environment(
    vocabs=[vocab.CoreVocab],
    methods={
        (dbm_save_method, vocab.Object): dbm_save,
        (dbm_delete_method, vocab.Object): dbm_delete},
    shortids=core.shortids_from_vocab(vocab.CoreVocab),
    c_accessors=core.shortids_from_vocab(vocab.CoreVocab))


def dbm_save_activity(env, asobj, db):
    pass




# Insert/update special methods for Activity / IntransitiveActivity
# objects




# Now, DBM with private data edition

def privatedbm_fetch(db, id):
    pass

def privatedbm_insert(env, asobj, db, private=None):
    pass

def privatedbm_update(env, asobj, db, private=None):
    pass

def privatedbm_upsert(env, asobj, db, private=None):
    pass

def privatedbm_delete(env, asobj, db):
    pass
