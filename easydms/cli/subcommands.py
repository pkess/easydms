# -*- coding: utf-8 -*-
#
# This file is part of easydms.
# Copyright (c) 2015 Peter Kessen
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject
# to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import sys
import argparse
import datetime

from easydms.util.prompt import prompt_date


parser = argparse.ArgumentParser(prog="easydms")
# Execute function without configuration or db
parser.set_defaults(rawCmd=None)
# Execute function with configuration but without db
parser.set_defaults(configCmd=None)
# Execute function with configuration and db
parser.set_defaults(cmd=None)


# ===========================================================================
# Top level arguments
# ===========================================================================
class VersionAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(VersionAction, self).__init__(
            option_strings, dest, help="print version and exit",
            nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print('{0} {1}'.format(parser.prog, "0.0.0"))
        sys.exit()


parser.add_argument('--version', action=VersionAction)


parser.add_argument('-c', '--config',
                    help="path to configuration file")
subparsers = parser.add_subparsers()

# ===========================================================================
# config
# ===========================================================================
configParser = subparsers.add_parser('config',
                                     help='view or edit configuration')


def print_usage_config(args):
    sys.exit(configParser.format_usage())


configParser.set_defaults(rawCmd=print_usage_config)

configSubparsers = configParser.add_subparsers()

# =======================================================================
# config dump
# =======================================================================
configDumpParser = configSubparsers.add_parser(
    'dump', help='dump configuration to stdout')


def configDumpCmd(config, args=None):
    print(config)
    raise Exception("config dump")
    sys.exit()
configDumpParser.set_defaults(rawCmd=None)
configDumpParser.set_defaults(configCmd=configDumpCmd)

# =======================================================================
# config edit
# =======================================================================
configEditParser = configSubparsers.add_parser(
    'edit', help='launch editor to edit configuration')


def configEditCmd(config, args=None):
    print(config)
    raise Exception("config Edit")
    sys.exit()
configEditParser.set_defaults(rawCmd=None)
configEditParser.set_defaults(configCmd=configEditCmd)

# ===========================================================================
# add
# ===========================================================================
addParser = subparsers.add_parser('add',
                                  help='add document to database')
addParserFile = addParser.add_argument('files', nargs='+',
                                       help='files to add')


def addCmd(config, db, args):
    """Add one or more documents to database"""
    for doc in args.files:
        date = prompt_date("Date of document?", guess_document_date(doc))
        db.insert_document(doc, date)


def guess_document_date(doc):
    """Guess the date of a pdf document.
    This will check the content of a pdf for a usable date in common format

    Current implementation returns todays date.
    """
    return datetime.date.today()


addParser.set_defaults(rawCmd=None)
addParser.set_defaults(configCmd=None)
addParser.set_defaults(cmd=addCmd)
