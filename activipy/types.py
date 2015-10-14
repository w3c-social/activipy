## Activipy --- ActivityStreams 2.0 implementation and validator for Python
## Copyright © 2015 Christopher Allan Webber <cwebber@dustycloud.org>
##
## This file is part of Activipy, which is GPLv3+ or Apache v2, your option
## (see COPYING); since that means effectively Apache v2 here's those headers
##
## Apache v2 header:
##   Licensed under the Apache License, Version 2.0 (the "License");
##   you may not use this file except in compliance with the License.
##   You may obtain a copy of the License at
##
##       http://www.apache.org/licenses/LICENSE-2.0
##
##   Unless required by applicable law or agreed to in writing, software
##   distributed under the License is distributed on an "AS IS" BASIS,
##   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##   See the License for the specific language governing permissions and
##   limitations under the License.

import copy
from pyld import jsonld


# The actual instances of these are defined in vocab.py

class ASType(object):
    """
    A @type than an ActivityStreams object might take on.

    BTW, you might wonder why this isn't using python class heirarchies
    as an abstraction.  The reason is simple: ActivityStreams objects
    can have multiple types listed under @type.  So our inheritance
    model is a bit different than python's.
    """
    def __init__(self, id_uri, parents, id_short=None,
                 methods=None, notes=None,
                 # Core means "core vocabulary", and must only
                 # ever be set by ASType
                 core=False):
        self.id_uri = id_uri
        self.parents = parents
        self.id_short = id_short
        self.methods = methods or {}
        self.notes = notes
        self.core = core

        self._inheritance = None

    def validate(self, asobj):
        validator = self.methods.get("validate")
        if validator is not None:
            validator(asobj)

    def __repr__(self):
        return "<ASType %s>" % (self.id_short or self.id_uri)

    @property
    def inheritance_chain(self):
        # memoization
        if self._inheritance is None:
            self._inheritance = astype_inheritance_list(self)

        return self._inheritance

    def __call__(self, id=None, **kwargs):
        # @@: In the future maybe we want a way for people
        #   to be able to add things within their vocabulary
        #   without having to use the id_uri.
        #
        #   One way to do this would be to add a method
        #   to construct things from the vocabulary,
        #   and the default method in __call__ uses the BaseVocabulary
        #   or whatever we call it
        if self.core:
            type_val = self.id_short
        else:
            type_val = self.id_uri
        jsobj = {"@type": type_val}
        jsobj.update(kwargs)
        if id:
            jsobj["@id"] = id
        return ASObj(jsobj)


def astype_inheritance_list(astype):
    """
    A depth-first gathering of this astype and all its parents
    """
    def traverse(astype, family):
        if not astype in family:
            family.append(astype)
            for parent in astype.parents:
                traverse(parent, family)

        return family

    return traverse(astype, [])


def astype_methods(astype):
    """
    Gather all methods applicable to this astype
    """
    pass



class ASVocab(object):
    """
    Mapping of known type IDs to ASTypes

    TODO: Maybe this should include the appropriate context
      it's working within?
    """
    def __init__(self, vocabs):
        self.vocab_map = self._map_vocabs(vocabs)

    def _map_vocabs(self, vocabs):
        return {
            type.id: type
            for type in vocabs}


# So, questions for ourselves.  What is this, if not merely a json
# object?  After all, an ActivityStreams object can be represented as
# "just JSON", and be done with it.  So what's *useful*?
#
# Here are some potentially useful properties:
#  - Expanded json-ld form
#  - Extracted types
#    - As short forms
#    - As expanded / unambiguous URIs (see json-ld)
#    - As ASType objects (where possible)
#  - Validation
#  - Lookup of what a property key "means"
#    (checking against activitystreams vocabulary)
#  - key-value access, including fetching any nested activitystreams
#    objects as ASObj types
#  - json serialization to string
#
# Of all the above, it would be nice not to have to repeat these
# operations.  If we've done it once, that should be good enough
# forever... in other words, memoization.  But memoization means
# that the object should be immutable.
# 
# ... but maybe ASObj objects *should* be immutable.
# This means we copy.deepcopy() on our way in, and if users want
# to change things, they either make a new ASObj or get back
# entirely new ASObj objects.
#
# I like this idea...

class ASObj(object):
    """
    The general ActivityStreams object that a user will work with
    """
    def __init__(self, jsobj):
        self.__jsobj = deepcopy_jsobj(jsobj)
        assert (isinstance(self.__jsobj.get("@type"), str) or
                isinstance(self.__jsobj.get("@type"), list))

    def __getitem__(self, key):
        val = self.__jsobj[key]
        if isinstance(val, dict) and "@type" in val:
            return ASObj(val)
        else:
            return deepcopy_jsobj(val)

    # META TODO: Convert some @property here to @memoized_property
    @property
    def type(self):
        type_attr = self["@type"]
        if isinstance(self["@type"], list):
            return type_attr
        else:
            return [type_attr]

    # TODO
    @property
    def type_expanded(self):
        pass

    # TODO
    @property
    def type_astype(self):
        pass

    ## @@: Do these belong here really?
    ##   Or do they belong as part of the Vocab system?
    # TODO
    # TODO Memoize
    def validate(self):
        pass
    
    # TODO
    @property
    def is_valid(self):
        pass

    # Don't memoize this, users might mutate
    def json(self):
        return copy.deepcopy(self.__jsobj)

    # TODO
    # TODO: Memoize
    def json_str(self):
        pass

    # TODO
    # TODO Memoize
    def __expanded_jsonld(self):
        pass

    # TODO: Memoize
    def expanded_jsonld(self):
        """
        Note: this produces a copy of the object returned, so consumers
          of this method may want to keep a copy of its result
          rather than calling over and over.
        """
        copy.deepcopy(self.__expanded_jsonld())

    # TODO
    # TODO: Memoize
    def expanded_jsonld_str(self):
        pass

    def __repr__(self):
        return "<ASObj %s>" % ", ".join(self.type)


def deepcopy_jsobj(jsobj):
    """
    Perform a deep copy of a JSON style object, but also
    permit insertions of 
    """
    def copy_asobj(asobj):
        return asobj.json()

    def copy_dict(this_dict):
        new_dict = {}
        for key, val in this_dict.items():
            new_dict[key] = copy_main(val)
        return new_dict

    def copy_list(this_list):
        new_list = []
        for item in this_list:
            new_list.append(copy_main(item))
        return new_list

    def copy_main(jsobj):
        if isinstance(jsobj, dict):
            return copy_dict(jsobj)
        elif isinstance(jsobj, ASObj):
            return copy_asobj(jsobj)
        elif isinstance(jsobj, list):
            return copy_list(jsobj)
        else:
            # All other JSON type objects are immutable,
            # just copy them down.
            # @@: We could provide validation that it's
            #   a valid json object here but that seems like
            #   it would bring unnecessary performance penalties.
            return jsobj

    return copy_main(jsobj)
