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

import datetime

import easydms.util.prompt
import easydms.util.datetime


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

    def test_prompt_int(self):
        """Test function to prompt an integer value from user"""
        prompt_int = easydms.util.prompt.prompt_int
        tests = [
            # ( prompt
            #   default,
            #    min,
            #    max,
            #    input,
            #    result
            ('prompt',
             5, None, None,
             [''],
             5),
            ('',
             5, 10, None,
             [''],
             10),
            ('prompt',
             5, None, 2,
             [''],
             2),
            ('prompt',
             5, None, None,
             ['8'],
             8),
            ('prompt',
             5, 10, 100,
             ['12'],
             12),
            ('prompt',
             5, None, None,
             ['12.8', ''],
             12),
            ('prompt',
             5, None, None,
             ['12.8', '1'],
             1),
            ('prompt',
             5, 10, 100,
             ['8', ''],
             10),
            ('prompt',
             5, None, None,
             ['M', ''],
             5),
            ('prompt',
             5, 2, 7,
             ['8', ''],
             7),
        ]
        for test in tests:
            prompt = test[0]
            default = test[1]
            min = test[2]
            max = test[3]
            inp = test[4]
            result = test[5]
            self.io.clear()
            for inp in inp:
                self.io.addinput(inp)
            self.assertEqual(prompt_int(prompt, default, min, max),
                             result, msg=str(test))

    def test_prompt_date(self):
        """Test function to prompt a date from user"""
        prompt_date = easydms.util.prompt.prompt_date
        tests = [
            # ( prompt
            #   default,
            #   input,
            #   result
            ('prompt',
             datetime.date(2015, 12, 31),
             ['', '', ''],
             datetime.date(2015, 12, 31)),
            ('prompt',
             datetime.date(2016, 2, 29),
             ['2015', '', ''],
             datetime.date(2015, 2, 28)),
            ('prompt',
             datetime.date(2015, 12, 31),
             ['', '11', '30'],
             datetime.date(2015, 11, 30)),
            ('prompt',
             None,
             ['2000', '1', '1'],
             datetime.date(2000, 1, 1)),
        ]
        for test in tests:
            prompt = test[0]
            default = test[1]
            inp = test[2]
            result = test[3]
            self.io.clear()
            for inp in inp:
                self.io.addinput(inp)
            self.assertEqual(prompt_date(prompt, default),
                             result, msg=str(test))

        with self.assertRaises(TypeError):
            prompt_date('', "2015-5-5")


class TestUtilDatetime(TestCase):
    def setUp(self):
        super(TestUtilDatetime, self).setUp()

    def test_days_in_month(self):
        self.assertEqual(easydms.util.datetime.days_in_month(2012, 2), 29)
        self.assertEqual(easydms.util.datetime.days_in_month(2013, 2), 28)
        self.assertEqual(easydms.util.datetime.days_in_month(2014, 2), 28)
        self.assertEqual(easydms.util.datetime.days_in_month(2015, 2), 28)
        self.assertEqual(easydms.util.datetime.days_in_month(2016, 2), 29)
        self.assertEqual(easydms.util.datetime.days_in_month(2015, 10), 31)
        self.assertEqual(easydms.util.datetime.days_in_month(2015, 11), 30)
        self.assertEqual(easydms.util.datetime.days_in_month(2015, 12), 31)
        self.assertEqual(easydms.util.datetime.days_in_month(2016, 1), 31)
