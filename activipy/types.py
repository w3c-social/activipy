## Activipy --- ActivityStreams 2.0 implementation and testing for Python
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
import pyld


# The actual instances of these are defined in vocab.py

class ASType(object):
    """
    A @type than an ActivityStreams object might take on.

    BTW, you might wonder why this isn't using python class heirarchies
    as an abstraction.  The reason is simple: ActivityStreams objects
    can have multiple types listed under @type.  So our inheritance
    model is a bit different than python's.
    """
    def __init__(self, id_short, id_uri, parents, methods=None):
        self.id_short = id_short
        self.id_uri = id_uri
        self.parents = parents
        self.methods = methods or {}

        self._inheritance = None

    def validate(self, asobj):
        validator = self.methods.get("validate")
        if validator is not None:
            validator(asobj)

    def __repr__(self):
        return "<ASType %s>" % self.id_short

    @property
    def inheritance_chain(self):
        # memoization
        if self._inheritance is None:
            self._inheritance = astype_inheritance_list(self)

        return self._inheritance

    def __call__(self, **kwargs):
        # TODO: Use this as a friendly ActivityStreams object constructor
        pass


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
    # TODO
    def __init__(self, jsobj):
        self.__jsobj = copy.deepcopy(jsobj)

    # TODO
    def __getitem__(self, key):
        # grab from the key value-pair
        pass

    # META TODO: Convert some @property here to @memoized_property
    # TODO
    @property
    def type_simple(self):
        pass

    # TODO
    @property
    def type_expanded(self):
        pass

    # TODO
    @property
    def type_astype(self):
        pass

    # TODO
    # TODO Memoize
    def validate(self):
        pass
    
    # TODO
    @property
    def is_valid(self):
        pass

    # Don't memoize this, users might mutate
    @property
    def as_json(self):
        return copy.deepcopy(self.__jsobj)

    # TODO
    @property
    def as_json_str(self):
        pass

    # TODO
    # TODO Memoize
    def __expanded_jsonld(self):
        pass

    # TODO: Memoize
    @property
    def as_expanded_jsonld(self):
        """
        Note: this produces a copy of the object returned, so consumers
          of this method may want to keep a copy of its result
          rather than calling over and over.
        """
        copy.deepcopy(self.__expanded_jsonld())

    # TODO
    @property
    def as_expanded_jsonld_str(self):
        pass

