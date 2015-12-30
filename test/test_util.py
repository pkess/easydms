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

"""Test command line interface."""

from _common import TestCase

import easydms.util.prompt


class TestUtilPrompt(TestCase):
    def setUp(self):
        super(TestUtilPrompt, self).setUp()
        self.io.install()

    def test_prompt_yn(self):
        """Check yes no prompt for user"""
        trueInput = ["y", "Y", "yes", "YES"]
        falseInput = ["n", "no", "N", "NO"]
        ambInput = ["yo", "ne", "z", " ", " y", " n"]
        prompt = "Prompt an input"
        for inp in trueInput:
            self.io.addinput(inp)
            self.assertTrue(easydms.util.prompt.prompt_yn(prompt))
            self.io.clear()
        for inp in falseInput:
            self.io.addinput(inp)
            self.assertFalse(easydms.util.prompt.prompt_yn(prompt))
            self.io.clear()
        for inp in ambInput:
            self.io.addinput(inp)
            self.io.addinput("y")
            self.assertTrue(easydms.util.prompt.prompt_yn(prompt))
            self.io.clear()
        self.io.addinput("")
        self.io.addinput("y")
        self.assertTrue(easydms.util.prompt.prompt_yn(prompt, True))
        self.io.clear()
        self.io.addinput("")
        self.io.addinput("n")
        self.assertFalse(easydms.util.prompt.prompt_yn(prompt, True))
        self.io.clear()
        self.io.addinput("")
        self.assertTrue(easydms.util.prompt.prompt_yn(prompt))
        self.io.clear()
        self.io.addinput("")
        self.assertTrue(easydms.util.prompt.prompt_yn(prompt, False))
        self.io.clear()
