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


class ASObj(object):
    """
    The general ActivityStreams object that a user will work with
    """
    pass


