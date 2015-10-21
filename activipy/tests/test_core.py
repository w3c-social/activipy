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

import pytest

from activipy import core, vocab




# Fake inheritance tree below

def fake_type_uri(type_name):
    return "http://example.org/ns#" + type_name
    
ASObject = core.ASType(fake_type_uri("object"), [], "Object")
ASLink = core.ASType(fake_type_uri("link"), [], "Link")

ASActivity = core.ASType(fake_type_uri("activity"), [ASObject], "Activity")
ASPost = core.ASType(fake_type_uri("post"), [ASActivity], "Post")
ASDelete = core.ASType(fake_type_uri("delete"), [ASActivity], "Delete")

ASCollection = core.ASType(
    fake_type_uri("collection"), [ASObject], "Collection")
ASOrderedCollection = core.ASType(
    fake_type_uri("orderedcollection"),
    [ASCollection],
    "OrderedCollection")
ASCollectionPage = core.ASType(
    fake_type_uri("collectionpage"),
    [ASCollection],
    "CollectionPage")
ASOrderedCollectionPage = core.ASType(
    fake_type_uri("orderedcollectionpage"),
    [ASOrderedCollection, ASCollectionPage],
    "OrderedCollectionPage")

# BS testing widget
ASWidget = core.ASType(
    fake_type_uri("widget"),
    [ASObject],
    "Widget")

ASFancyWidget = core.ASType(
    fake_type_uri("fancywidget"),
    [ASWidget],
    "FancyWidget")


# Example vocab and environment
ExampleVocab = core.ASVocab(
    [ASObject, ASLink,
     ASActivity, ASPost, ASDelete,
     ASCollection, ASOrderedCollection, ASCollectionPage,
     ASOrderedCollectionPage,
     ASWidget, ASFancyWidget])

ExampleEnv = core.Environment(
    vocabs=[ExampleVocab],
    shortids=core.shortids_from_vocab(ExampleVocab),
    c_accessors=core.shortids_from_vocab(ExampleVocab))




# Basic tests

def test_inheritance_list():
    # Should just be itself
    assert core.astype_inheritance_list(ASObject) == \
        [ASObject]
    assert core.astype_inheritance_list(ASLink) == \
        [ASLink]

    # Should be itself, then its parent
    assert core.astype_inheritance_list(ASActivity) == \
        [ASActivity, ASObject]
    assert core.astype_inheritance_list(ASCollection) == \
        [ASCollection, ASObject]

    # A slightly longer inheritance chain
    assert core.astype_inheritance_list(ASPost) == \
        [ASPost, ASActivity, ASObject]
    assert core.astype_inheritance_list(ASDelete) == \
        [ASDelete, ASActivity, ASObject]
    assert core.astype_inheritance_list(ASOrderedCollection) == \
        [ASOrderedCollection, ASCollection, ASObject]
    assert core.astype_inheritance_list(ASCollectionPage) == \
        [ASCollectionPage, ASCollection, ASObject]

    # Multiple inheritance!  Egads.
    # ... this clearly demonstrates our present depth-first
    # traversal.  A breadth-first traversal would mean
    # ASCollectionPage would go before ASCollection, which may be more
    # to a user's expectations.
    assert core.astype_inheritance_list(ASOrderedCollectionPage) == \
        [ASOrderedCollectionPage, ASOrderedCollection,
         ASCollectionPage, ASCollection, ASObject,]

    # does the property version also work?
    assert ASOrderedCollectionPage.inheritance_chain == \
        [ASOrderedCollectionPage, ASOrderedCollection,
         ASCollectionPage, ASCollection, ASObject]

    # What about composite core
    assert core.astype_inheritance_list(
        ASFancyWidget, ASOrderedCollectionPage) == [
            ASFancyWidget, ASWidget,
            ASOrderedCollectionPage, ASOrderedCollection,
            ASCollectionPage, ASCollection, ASObject]
    


ROOT_BEER_NOTE_JSOBJ = {
    "@type": "Create",
    "@id": "http://tsyesika.co.uk/act/foo-id-here/",
    "actor": {
        "@type": "Person",
        "@id": "http://tsyesika.co.uk/",
        "displayName": "Jessica Tallon"},
    "to": ["acct:cwebber@identi.ca",
           "acct:justaguy@rhiaro.co.uk",
           "acct:ladyaeva@hedgehog.example"],
    "object": {
        "@type": "Note",
        "@id": "htp://tsyesika.co.uk/chat/sup-yo/",
        "content": "Up for some root beer floats?"}}

ROOT_BEER_NOTE_MIXED_ASOBJ = {
    "@type": "Create",
    "@id": "http://tsyesika.co.uk/act/foo-id-here/",
    "actor": core.ASObj({
        "@type": "Person",
        "@id": "http://tsyesika.co.uk/",
        "displayName": "Jessica Tallon"}),
    "to": ["acct:cwebber@identi.ca",
           "acct:justaguy@rhiaro.co.uk",
           "acct:ladyaeva@hedgehog.example"],
    "object": core.ASObj({
        "@type": "Note",
        "@id": "htp://tsyesika.co.uk/chat/sup-yo/",
        "content": "Up for some root beer floats?"})}

ROOT_BEER_NOTE_VOCAB = vocab.Create(
    "http://tsyesika.co.uk/act/foo-id-here/",
    actor=vocab.Person(
        "http://tsyesika.co.uk/",
        displayName="Jessica Tallon"),
    to=["acct:cwebber@identi.ca",
        "acct:justaguy@rhiaro.co.uk",
        "acct:ladyaeva@hedgehog.example"],
    object=vocab.Note(
        "htp://tsyesika.co.uk/chat/sup-yo/",
        content="Up for some root beer floats?"))


def _looks_like_root_beer_note(jsobj):
    return (
        len(jsobj) == 5 and
        jsobj["@type"] == "Create" and
        jsobj["@id"] == "http://tsyesika.co.uk/act/foo-id-here/" and
        isinstance(jsobj["actor"], dict) and
        len(jsobj["actor"]) == 3 and
        jsobj["actor"]["@type"] == "Person" and
        jsobj["actor"]["@id"] == "http://tsyesika.co.uk/" and
        jsobj["actor"]["displayName"] == "Jessica Tallon" and
        isinstance(jsobj["to"], list) and
        jsobj["to"] == ["acct:cwebber@identi.ca",
                        "acct:justaguy@rhiaro.co.uk",
                        "acct:ladyaeva@hedgehog.example"] and
        isinstance(jsobj["object"], dict) and
        len(jsobj["object"]) == 3 and
        jsobj["object"]["@type"] == "Note" and
        jsobj["object"]["@id"] == "htp://tsyesika.co.uk/chat/sup-yo/" and
        jsobj["object"]["content"] == "Up for some root beer floats?")


def test_deepcopy_jsobj():
    # We'll mutate later, so let's make a copy of this
    root_beer_note = copy.deepcopy(ROOT_BEER_NOTE_JSOBJ)
    assert _looks_like_root_beer_note(root_beer_note)

    # Test copying a compicated datastructure
    copied_root_beer_note = core.deepcopy_jsobj(root_beer_note)
    assert _looks_like_root_beer_note(copied_root_beer_note)

    # Mutate
    root_beer_note["to"].append("sneaky@mcsneakers.example")
    assert not _looks_like_root_beer_note(root_beer_note)
    # but things are still as they were in our copy right??
    assert _looks_like_root_beer_note(copied_root_beer_note)

    # Test nested asobj copying
    assert _looks_like_root_beer_note(
        core.deepcopy_jsobj(ROOT_BEER_NOTE_MIXED_ASOBJ))


def test_vocab_constructor():
    assert isinstance(
        ROOT_BEER_NOTE_VOCAB,
        core.ASObj)

    assert _looks_like_root_beer_note(
        ROOT_BEER_NOTE_VOCAB.json())


ROOT_BEER_NOTE_ASOBJ = core.ASObj({
    "@type": "Create",
    "@id": "http://tsyesika.co.uk/act/foo-id-here/",
    "actor": core.ASObj({
        "@type": "Person",
        "@id": "http://tsyesika.co.uk/",
        "displayName": "Jessica Tallon"}),
    "to": ["acct:cwebber@identi.ca",
           "acct:justaguy@rhiaro.co.uk"],
    "object": core.ASObj({
        "@type": "Note",
        "@id": "htp://tsyesika.co.uk/chat/sup-yo/",
        "content": "Up for some root beer floats?"})})


def test_asobj_keyaccess():
    assert ROOT_BEER_NOTE_ASOBJ["@type"] == "Create"
    assert ROOT_BEER_NOTE_ASOBJ["@id"] == \
        "http://tsyesika.co.uk/act/foo-id-here/"

    # Accessing things that look like asobjects
    # will return asobjects
    assert isinstance(
        ROOT_BEER_NOTE_ASOBJ["object"],
        core.ASObj)

    # However, we should still be able to get the
    # dictionary edition by pulling down .json()
    assert isinstance(
        ROOT_BEER_NOTE_ASOBJ.json()["object"],
        dict)

    # Traversal of traversal should work
    assert ROOT_BEER_NOTE_ASOBJ["object"]["content"] == \
        "Up for some root beer floats?"


def test_handle_one():
    # Fake value boxes
    received_args = []
    received_kwargs = []

    def test_method1(*args, **kwargs):
        received_args.append(args)
        received_kwargs.append(kwargs)
        return "Got it!"

    def test_method2(*args, **kwargs):
        # we should never hit this
        assert False
        return "skip me!"

    # well if we got this far we never hit test_method2, which is good
    # did we run test_method1 then?
    our_jsobj = ASWidget(foo="bar")
    handler = core.handle_one(
        [(test_method1, ASWidget), (test_method2, ASObject)],
        our_jsobj)
    assert handler(1, 2, foo="bar") == "Got it!"
    assert received_args[0] == (our_jsobj, 1, 2)
    assert received_kwargs[0] == {"foo": "bar"}

    # Okay, let's try running with no methods available
    with pytest.raises(core.NoMethodFound):
        core.handle_one([], our_jsobj)

    # Let's try running something with a custom fallback...
    # ... this fallback drinks the half empty glass
    glass = ["half_empty"]
    def drink_glass(asobj):
        # down the hatch
        glass.pop()
    core.handle_one([], our_jsobj, _fallback=drink_glass)
    assert len(glass) == 0  # if this passes, the pessimists win


def test_handle_map():
    def test_one(*args, **kwargs):
        return (1, args, kwargs)

    def test_two(*args, **kwargs):
        return (2, args, kwargs)

    def test_three(*args, **kwargs):
        return (3, args, kwargs)

    our_asobj = ASWidget(snorf="snizzle")
    handler = core.handle_map([(test_one, ASFancyWidget),
                                (test_two, ASWidget), (test_three, ASObject)],
                               our_asobj)
    result = handler("one", "two", "three", lets="go!")
    assert result[0][0] == 1
    assert result[1][0] == 2
    assert result[2][0] == 3
    for r in result:
        assert r[1] == (our_asobj, "one", "two", "three")
        assert r[2] == {"lets": "go!"}


def test_handle_fold():
    def test_one(val, asobj, location):
        return val + "one %s... " % location

    def test_two(val, asobj, location):
        return val + "two %s... " % location

    def test_three(val, asobj, location):
        return val + "three %s... " % location

    our_asobj = ASWidget(snorf="snizzle")
    handler = core.handle_fold([(test_one, ASFancyWidget),
                                 (test_two, ASWidget), (test_three, ASObject)],
                                our_asobj)
    result = handler("Counting down! ", "mississippi")
    assert result == (
        "Counting down! one mississippi... "
        "two mississippi... three mississippi... ")

    # Now test breaking out early
    def test_two_breaks_out(val, asobj, location):
        return core.HaltIteration(val + "two %s... " % location)

    handler = core.handle_fold([(test_one, ASFancyWidget),
                                 (test_two_breaks_out, ASWidget),
                                 (test_three, ASObject)],
                                our_asobj)
    result = handler("Counting down! ", "mississippi")
    # we never get to three in this version
    assert result == (
        "Counting down! one mississippi... "
        "two mississippi... ")




# Methods testing
# ===============

### begin testing methods ###

save = core.MethodId("save", "Save things", core.handle_one)
get_things = core.MethodId("get_things", "Build up a map of stuff",
                           core.handle_map)
# This one's name intentionally different than its variable name
# for testing reasons
combine_things = core.MethodId("combine", "combine things", core.handle_fold)

def _object_save(asobj, db):
    db[asobj["@id"]] = ("saved as object", asobj)

def _widget_save(asobj, db):
    db[asobj["@id"]] = ("saved as widget", asobj)

def _object_get_things(asobj):
    return "objects are fun"

def _activity_get_things(asobj):
    return "activities are neat"

def _post_get_things(asobj):
    return "posts are cool"

def _collection_combine_things(asobj, val, chant):
    return val + chant + "%s, my friend, and remember us collected\n"
    
def _ordered_collection_combine_things(asobj, val, chant):
    return val + chant + ", my dear, and cherish the order\n"

def _ordered_collection_page_combine_things(asobj, val, chant):
    return val + chant + ", my sweet, a new page is turning\n"

### end testing methods ###

MethodEnv = core.Environment(
    vocabs=[ExampleVocab],
    methods={
        (save, ASObject): _object_save,
        (save, ASWidget): _widget_save,
        (get_things, ASObject): _object_get_things,
        (get_things, ASActivity): _activity_get_things,
        (get_things, ASPost): _post_get_things,
        (combine_things, ASCollection): _collection_combine_things,
        (combine_things, ASOrderedCollection): (
            _ordered_collection_combine_things),
        (combine_things, ASOrderedCollectionPage): (
            _ordered_collection_page_combine_things)},
    shortids=core.shortids_from_vocab(ExampleVocab),
    c_accessors=core.shortids_from_vocab(ExampleVocab))


def test_environment_c_access():
    widget = MethodEnv.c.Widget(foo="bar")
    assert widget["foo"] == "bar"
    assert widget.types_astype == [ASWidget]
    assert widget.env == MethodEnv
    assert MethodEnv.c.Widget.astype == ASWidget


def test_environment_m_access_handle_one():
    db = {}
    widget = MethodEnv.c.Widget("fooid:12345")
    MethodEnv.m.save(widget, db)
    assert db["fooid:12345"] == ("saved as widget", widget)

    foo_object = MethodEnv.c.Object("fooid:00001")
    MethodEnv.m.save(foo_object, db)
    assert db["fooid:00001"] == ("saved as object", foo_object)

    collection = MethodEnv.c.Collection("fooid:8888")
    MethodEnv.m.save(collection, db)
    assert db["fooid:8888"] == ("saved as object", collection)


def test_environment_m_access_handle_map():
    result = MethodEnv.m.get_things(MethodEnv.c.Widget("fooid:12345"))
    assert result == ["objects are fun"]

    result = MethodEnv.m.get_things(MethodEnv.c.Activity("fooid:0202"))
    assert result == ["activities are neat", "objects are fun"]

    result = MethodEnv.m.get_things(MethodEnv.c.Delete("fooid:0303"))
    assert result == ["activities are neat", "objects are fun"]

    result = MethodEnv.m.get_things(MethodEnv.c.Post("fooid:0808"))
    assert result == ["posts are cool", "activities are neat",
                      "objects are fun"]
