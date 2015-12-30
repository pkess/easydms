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


def prompt_yn(prompt, require=False):
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
    choice = input().lower()
    if choice in yes:
        return True
    elif choice in no:
        return False

    print("Please respond with 'yes' or 'no'")
    return prompt_yn(prompt, require)


def prompt_int(prompt, default=None, min=None, max=None):
    sys.stdout.write(prompt)
    if default is not None:
        sys.stdout.write(' ({0})'.format(default))
        if min is not None and default < min:
            default = min
        elif max is not None and default > max:
            default = max
    sys.stdout.write(' ')
    inp = input()
    if default is not None and inp == '':
        return default
    try:
        ret = int(inp)
        if min is not None and ret < min:
            ret = prompt_int(prompt, min, min, max)
        elif max is not None and ret > max:
            ret = prompt_int(prompt, max, min, max)
        sys.stdout.write('\n')
        return ret
    except ValueError:
        try:
            newGuess = float(inp)
            return prompt_int(prompt, int(newGuess), min, max)
        except ValueError:
            return prompt_int(prompt, default, min, max)
