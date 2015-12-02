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
##
## In addition, this page copies huge swaths of documentation from the
## Microformats documents, which you can find at
##   http://microformats.org/wiki/microformats2
## It seems to be under CC0 but it's hard to find the legal info on that page...


import json

from .core import (
    ASType, ASVocab, Environment, shortids_from_vocab,
    resource_filename, chain_dicts,
    AS2_CONTEXT, AS2_CONTEXT_URI, make_simple_loader)
from .vocab import CoreVocab, Object


def jf2_uri(identifier):
    return "http://microformats.org/wiki/" + identifier


Adr = ASType(
    jf2_uri("h-adr"), [Object], "Adr",
    notes=(
        "The h-adr microformat is for marking up structured locations such "
        "as addresses, physical and/or postal."))

Card = ASType(
    jf2_uri("h-card"), [Object], "Card",
    notes=(
        "The h-card microformat is for marking up people and organizations."))

Entry = ASType(
    jf2_uri("h-entry"), [Object], "Entry",
    notes=(
        "The h-entry microformat is for marking up syndicatable content such "
        "as blog posts, notes, articles, comments, photos and similar."))

Feed = ASType(
    jf2_uri("h-feed"), [Object],
    "Feed",
    notes=(
        "h-feed is a microformats2 draft for marking up a stream or feed of "
        "h-entry posts, like complete posts on a home page or archive pages, "
        "or summaries or other brief lists of posts."))

Item = ASType(
    jf2_uri("h-item"), [Object],
    "Item",
    notes=(
        "h-item is a simple, open format for publishing details about "
        "arbitrary items."))

Listing = ASType(
    jf2_uri("h-listing"), [Object],
    "Listing",
    notes=(
        "h-listing is a simple, open format for publishing product data on "
        "the web."))

Product = ASType(
    jf2_uri("h-product"), [Object],
    "Product",
    notes=(
        "h-product is a simple, open format for "
        "publishing product data on the web."))

Recipe = ASType(
    jf2_uri("h-recipe"), [Object],
    "Recipe",
    notes=(
        "h-recipe is a simple, open format for publishing recipes on the web."))

Resume = ASType(
    jf2_uri("h-resume"), [Object],
    "Resume",
    notes=(
        "h-resume is a simple, open format for publishing resumes and CVs on "
        "on the web."))

Review = ASType(
    jf2_uri("h-review"), [Object],
    "Review",
    notes=(
        "h-review is a simple, open format for publishing reviews on the web."))

ReviewAggregate = ASType(
    jf2_uri("h-review-aggregate"), [Object],
    "Review-aggregate",
    notes=(
        "The h-review-aggregate microformat is for marking up aggregate "
        "reviews of a single item."))

Cite = ASType(
    jf2_uri("h-cite"), [Object],
    "Cite",
    notes=(
        "h-cite is a simple, open format for publishing citations and "
        "references to online publications."))


JF2Vocab = ASVocab(
    [Adr, Card, Entry, Feed, Item,
     Listing, Product, Recipe, Resume,
     Review, ReviewAggregate, Cite])


JF2_CONTEXT_FILE = resource_filename(
    'activipy', 'jf2-context.jsonld')
JF2_CONTEXT = json.loads(open(JF2_CONTEXT_FILE, 'r').read())
JF2_CONTEXT_URI = (
    "http://stream.thatmustbe.us/jf2.php")
JF2_DEFAULT_URL_MAP = {
    JF2_CONTEXT_URI: JF2_CONTEXT,
    AS2_CONTEXT_URI: AS2_CONTEXT}

jf2_loader = make_simple_loader(JF2_DEFAULT_URL_MAP)


BasicJf2Env = Environment(
    implied_context=JF2_CONTEXT_URI,
    document_loader=jf2_loader,
    vocabs=[CoreVocab, JF2Vocab],
    shortids=chain_dicts(
        shortids_from_vocab(CoreVocab),
        shortids_from_vocab(JF2Vocab)),
    c_accessors=chain_dicts(
        shortids_from_vocab(CoreVocab),
        shortids_from_vocab(JF2Vocab)))

Env = BasicJf2Env

