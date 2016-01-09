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
from easydms.util.prompt import prompt_yn
import easydms.config
import easydms.dbcore as dbcore

from easydms.cli.subcommands import parser


def main():
    args = parser.parse_args(sys.argv)
    if args.rawCmd is not None:
        args.rawCmd(args)

    try:
        config = easydms.config.Config(args.config)
        if args.configCmd is not None:
            args.configCmd(config, args)

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

        if args.cmd is not None:
            args.cmd(config, db, args)

    except easydms.config.ErrorNoConfiguration as e:
        msg = ("Error: Could not load configuration\n"
               "following path(s) were searched:\n"
               "{0}").format(e)
        sys.exit(msg)


if __name__ == '__main__':
    main()
