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

from activipy import types




# Fake inheritance tree below

def fake_type_uri(type_name):
    return "http://example.org/ns#" + type_name
    
ASObject = types.ASType("Object", fake_type_uri("object"), [])
ASLink = types.ASType("Link", fake_type_uri("link"), [])

ASActivity = types.ASType("Activity", fake_type_uri("activity"), [ASObject])
ASPost = types.ASType("Post", fake_type_uri("post"), [ASActivity])
ASDelete = types.ASType("Delete", fake_type_uri("delete"), [ASActivity])

ASCollection = types.ASType(
    "Collection", fake_type_uri("collection"), [ASObject])
ASOrderedCollection = types.ASType(
    "OrderedCollection",
    fake_type_uri("orderedcollection"),
    [ASCollection])
ASCollectionPage = types.ASType(
    "CollectionPage",
    fake_type_uri("collectionpage"),
    [ASCollection])
ASOrderedCollectionPage = types.ASType(
    "OrderedCollectionPage",
    fake_type_uri("orderedcollectionpage"),
    [ASOrderedCollection, ASCollectionPage])




# Basic tests

def test_inheritance_list():
    # Should just be itself
    assert types.astype_inheritance_list(ASObject) == \
        [ASObject]
    assert types.astype_inheritance_list(ASLink) == \
        [ASLink]

    # Should be itself, then its parent
    assert types.astype_inheritance_list(ASActivity) == \
        [ASActivity, ASObject]
    assert types.astype_inheritance_list(ASCollection) == \
        [ASCollection, ASObject]

    # A slightly longer inheritance chain
    assert types.astype_inheritance_list(ASPost) == \
        [ASPost, ASActivity, ASObject]
    assert types.astype_inheritance_list(ASDelete) == \
        [ASDelete, ASActivity, ASObject]
    assert types.astype_inheritance_list(ASOrderedCollection) == \
        [ASOrderedCollection, ASCollection, ASObject]
    assert types.astype_inheritance_list(ASCollectionPage) == \
        [ASCollectionPage, ASCollection, ASObject]

    # Multiple inheritance!  Egads.
    # ... this clearly demonstrates our present depth-first
    # traversal.  A breadth-first traversal would mean
    # ASCollectionPage would go before ASCollection, which may be more
    # to a user's expectations.
    assert types.astype_inheritance_list(ASOrderedCollectionPage) == \
        [ASOrderedCollectionPage, ASOrderedCollection,
         ASCollection, ASObject, ASCollectionPage]

