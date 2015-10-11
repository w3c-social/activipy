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
## ActivityStreams 2.0 Vocabulary document,
##   http://www.w3.org/TR/activitystreams-vocabulary/
##
## Copyright © 2015 Activity Streams Working Group, IBM & W3C® (MIT,
##   ERCIM, Keio, Beihang). W3C liability, trademark and permissive
##   document license rules apply. 
##
## which is released under the
## "W3C Software and Document Notice and License":
## 
##    This work is being provided by the copyright holders under the
##    following license.
##
##    License
##    -------
##    
##    By obtaining and/or copying this work, you (the licensee) agree
##    that you have read, understood, and will comply with the
##    following terms and conditions.
##    
##    Permission to copy, modify, and distribute this work, with or
##    without modification, for any purpose and without fee or royalty
##    is hereby granted, provided that you include the following on
##    ALL copies of the work or portions thereof, including
##    modifications:
##    
##     - The full text of this NOTICE in a location viewable to users
##       of the redistributed or derivative work.
##     - Any pre-existing intellectual property disclaimers, notices,
##       or terms and conditions. If none exist, the W3C Software and
##       Document Short Notice should be included.
##     - Notice of any changes or modifications, through a copyright
##       statement on the new code or document such as "This software
##       or document includes material copied from or derived from
##       [title and URI of the W3C document]. Copyright © [YEAR] W3C®
##       (MIT, ERCIM, Keio, Beihang)." 
##    
##    Disclaimers
##    -----------
##    
##    THIS WORK IS PROVIDED "AS IS," AND COPYRIGHT HOLDERS MAKE NO
##    REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT
##    NOT LIMITED TO, WARRANTIES OF MERCHANTABILITY OR FITNESS FOR ANY
##    PARTICULAR PURPOSE OR THAT THE USE OF THE SOFTWARE OR DOCUMENT
##    WILL NOT INFRINGE ANY THIRD PARTY PATENTS, COPYRIGHTS,
##    TRADEMARKS OR OTHER RIGHTS.
##    
##    COPYRIGHT HOLDERS WILL NOT BE LIABLE FOR ANY DIRECT, INDIRECT,
##    SPECIAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF ANY USE OF THE
##    SOFTWARE OR DOCUMENT.
##    
##    The name and trademarks of copyright holders may NOT be used in
##    advertising or publicity pertaining to the work without
##    specific, written prior permission. Title to copyright in this
##    work will at all times remain with copyright holders.

from .types import ASType

def as_uri(identifier):
    return "http://www.w3.org/ns/activitystreams#" + identifier


# Core classes
# ============

Object = ASType(
    as_uri("Object"), [], "Object",
    notes=(
        "Describes an object of any kind. "
        "The Object class serves as the base class for most of the "
        "other kinds of objects defined in the Activity Vocabulary, "
        "include other Core classes such as Activity, "
        "IntransitiveActivity, Actor, Collection and OrderedCollection."))

Link = ASType(
    as_uri("Link"), [], "Link",
    notes=(
        "A Link is an indirect, qualified reference to a resource identified by"
        "a URL. The fundamental model for links is established by [RFC5988]. "
        "Many of the properties defined by the Activity Vocabulary allow "
        "values that are either instances of Object or Link. When a Link is "
        "used, it establishes a qualified relation connecting the subject "
        "(the containing object) to the resource identified by the href."))

Activity = ASType(
    as_uri("Activity"), [Object], "Activity",
    notes=(
        "An Activity is a subclass of Object that describes some form of "
        "action that may happen, is currently happening, or has already "
        "happened. The Activity class itself serves as an abstract base "
        "class for all types of activities. It is important to note that "
        "the Activity class itself does not carry any specific semantics "
        "about the kind of action being taken."))

IntransitiveActivity = ASType(
    as_uri("IntransitiveActivity"), [Activity], "IntransitiveActivity",
    notes=(
        "Instances of IntransitiveActivity are a subclass of Activity whose "
        "actor property identifies the direct object of the action as opposed "
        "to using the object property."))

Actor = ASType(
    as_uri("Actor"), [Object], "Actor",
    notes=(
        "An Actor is any entity that is capable of being the primary actor "
        "for an Activity."))

Collection = ASType(
    as_uri("Collection"), [Object], "Collection",
    notes=(
        "A Collection is a subclass of Object that represents ordered or "
        "unordered sets of Object or Link instances.\n\n"
        "Refer to the Activity Streams 2.0 Core specification for a complete"
        "description of the Collection type."))

OrderedCollection = ASType(
    as_uri("OrderedCollection"), [Collection], "OrderedCollection",
    notes=(
        "A subclass of Collection in which members of the logical collection "
        "are assumed to always be strictly ordered."))

CollectionPage = ASType(
    as_uri("CollectionPage"), [Collection], "CollectionPage",
    notes=(
        "Used to represent distinct subsets of items from a Collection. "
        "Refer to the Activity Streams 2.0 Core for a complete description of "
        "the CollectionPage object."))

OrderedCollectionPage = ASType(
    as_uri("OrderedCollectionPage"), [OrderedCollection, CollectionPage],
    "OrderedCollectionPage",
    notes=(
        "Used to represent ordered subsets of items from an OrderedCollection. "
        "Refer to the Activity Streams 2.0 Core for a complete description of "
        "the OrderedCollectionPage object."))



# Extended Classes: Activity Types
# ================================

