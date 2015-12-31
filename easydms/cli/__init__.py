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

import os
import sys
from optparse import OptionParser
import datetime
from easydms.util.prompt import prompt_yn, prompt_date
import easydms.config
import easydms.dbcore as dbcore

parser = OptionParser(version="easydms version 0.0.0")
parser.add_option("-c", "--config", dest="CONFIG",
                  help="path to configuration file")


def print_usage_config():
    sys.exit("Usage (Not implemented)")


def print_usage_add():
    sys.exit("Usage (Not implemented)")


def add(db, docs):
    """Add one or more documents to database"""
    if isinstance(docs, str):
        docs = [docs]
    for doc in docs:
        date = prompt_date("Date of document?", guess_document_date(doc))
        db.insert_document(doc, date)


def guess_document_date(doc):
    """Guess the date of a pdf document.
    This will check the content of a pdf for a usable date in common format

    Current implementation returns todays date.
    """
    return datetime.date.today()


def subcommand_add(options, args, database):
    if len(args) < 2:
        print("No files were given")
        print_usage_add()
    files = args[1:]
    add(database, files)


def main():
    (options, args) = parser.parse_args()

    try:
        config = easydms.config.Config(options.CONFIG)
        if len(args) > 0 and args[0] == 'config':
            if len(args) == 1:
                print_usage_config()

            if args[1] == 'dump':
                print(config)
                sys.exit()
            else:
                print_usage_config()

        dmsdirectory = config.getRequiredKey('directory')
        dmsdirectory = os.path.expanduser(dmsdirectory)
        if not os.path.exists(dmsdirectory):
            create = prompt_yn(
                "Directory \"{0}\" does not exist. Create?".format(
                    dmsdirectory))
            if create:
                os.makedirs(dmsdirectory)
            else:
                sys.exit("Abort due to not existing directory")

        dbpath = os.path.join(dmsdirectory,
                              config.getRequiredKey('library'))
        db = dbcore.Database(dbpath)
        db.create_db()

        subcommands = {
            'add': subcommand_add,
        }
        if len(args) > 0:
            if args[0] in subcommands.keys():
                subcommands[args[0]](options, args, db)

    except easydms.config.ErrorNoConfiguration as e:
        msg = ("Error: Could not load configuration\n"
               "following path(s) were searched:\n"
               "{0}").format(e)
        sys.exit(msg)


if __name__ == '__main__':
    main()
