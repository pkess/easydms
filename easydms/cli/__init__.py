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
import easydms.config
import easydms.dbcore as dbcore

parser = OptionParser(version="easydms version 0.0.0")
parser.add_option("-c", "--config", dest="CONFIG",
                  help="path to configuration file")


def input_yn(prompt, require=False):
    """Prompts the user for a "yes" or "no" response. The default is
    "yes" unless `require` is `True`, in which case there is no default.
    """
    yes = set(['yes', 'y', 'ye'])
    no = set(['no', 'n'])

    if not require:
        # raw_input returns the empty string for "enter"
        yes.add('')

    sys.stdout.write(prompt)
    sys.stdout.write(" (Yes/No) ")
    choice = raw_input().lower()
    if choice in yes:
        return True
    elif choice in no:
        return False

    print("Please respond with 'yes' or 'no'")
    return input_yn(prompt, require)


def print_usage_config():
    sys.exit("Usage (Not implemented)")


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
            create = input_yn(
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
        assert db
    except easydms.config.ErrorNoConfiguration as e:
        msg = ("Error: Could not load configuration\n"
               "following path(s) were searched:\n"
               "{0}").format(e)
        sys.exit(msg)


if __name__ == '__main__':
    main()
