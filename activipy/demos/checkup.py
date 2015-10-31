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

from activipy.core import (
    ASType, ASVocab, Environment, shortids_from_vocab,
    chain_dicts)
from activipy import vocab

def checkup_uri(identifier):
    return "http://checkup.example/ns#" + identifier

CheckIn = ASType(
    checkup_uri("CheckIn"), [vocab.Arrive], "CheckIn",
    notes=(
        "Check in to a location."))

Coupon = ASType(
    checkup_uri("Coupon"), [vocab.Object], "Coupon",
    notes=(
        "A redeemable voucher (by redeem_url) for hopefully "
        "something exciting!"))

RoyalStatus = ASType(
    checkup_uri("RoyalStatus"), [vocab.Object], "RoyalStatus",
    notes=(
        "How royal you are at a given location!"))


CheckUpVocab = ASVocab([CheckIn, Coupon, RoyalStatus])

CheckUpEnv = Environment(
    vocabs=[vocab.CoreVocab],
    shortids=chain_dicts(
        shortids_from_vocab(vocab.CoreVocab),
        shortids_from_vocab(CheckUpVocab, "CheckUp")),
    c_accessors=chain_dicts(
        shortids_from_vocab(vocab.CoreVocab),
        shortids_from_vocab(CheckUpVocab)))
