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


import sys
import argparse
from collections import namedtuple, OrderedDict

# from . import types, vocab




# Dump command
# ============

def dump_cli():
    pass


def dump_setup_subparser(subparser):
    subparser.add_argument("as_json")




# Build command
# ==============

def build_cli():
    pass


def build_setup_subparser(subparser):
    pass




# Testdriver command
# ==================

def testdriver_cli():
    pass


def testdriver_setup_subparser(subparser):
    pass




# Build CLI
# =========

Command = namedtuple("command", ["cli_proc", "setup_subparser"])

SUBCOMMANDS_MAP = OrderedDict([
    ("dump", Command(
        dump_cli, dump_setup_subparser)),
    ("build", Command(
        build_cli, build_setup_subparser)),
    ("testdriver", Command(
        testdriver_cli, testdriver_setup_subparser))])


def main():
    parser = argparse.ArgumentParser(
        # @@: this sucks as a description
        description="Test for activitystreams correctness")

    subparsers = parser.add_subparsers(dest="subparser_name")

    for subcommand_key, subcommand_cmd in SUBCOMMANDS_MAP.items():
        subcmd_parser = subparsers.add_parser(subcommand_key)
        subcommand_cmd.setup_subparser(subcmd_parser)

    args = parser.parse_args()
    if not args.subparser_name:
        parser.print_help()
        sys.exit(1)

    subcmd_proc = SUBCOMMANDS_MAP[args.subparser_name].cli_proc
    subcmd_proc(args)


if __name__ == "__main__":
    main()

