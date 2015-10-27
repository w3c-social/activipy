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

def dbm_save(asobj, db):
    assert asobj.id is not None
    new_val = asobj.json()
    db[asobj.id] = new_val
    return new_val

def dbm_delete(asobj, db):
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


def dbm_activity_normalized_save(asobj, db):
    assert asobj.id is not None
    as_json = asobj.json()

    def maybe_normalize(key):
        val = as_json.get(key)
        # yup, time to normalize
        if asobj.env.is_astype(val, vocab.Object):
            val_asobj = core.ASObj(val, asobj.env)
            # If there's no id, or if this object is already in the database,
            # then okay, don't normalize
            if val.id is None or val.id in db:
                return

            # Otherwise, save to the database
            asobj.env.run_method(val_asobj, dbm_save_method, db)
            # and set the key to be the .id
            as_json[key] = val_asobj.id

    maybe_normalize("actor")
    maybe_normalize("object")
    maybe_normalize("target")
    db[asobj.id] = as_json
    return as_json


DbmNormalizedEnv = core.Environment(
    vocabs=[vocab.CoreVocab],
    methods={
        (dbm_save_method, vocab.Object): dbm_save,
        (dbm_delete_method, vocab.Object): dbm_delete,
        (dbm_save_method, vocab.Activity): dbm_save},
    shortids=core.shortids_from_vocab(vocab.CoreVocab),
    c_accessors=core.shortids_from_vocab(vocab.CoreVocab))




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
