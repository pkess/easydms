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

"""Test if version will be displayed correctly."""

from _common import TestCase, TestCaseCommandline

import sys
import unittest


class TestVersion(TestCase):
    def setUp(self):
        super(TestVersion, self).setUp()

        self.io.install()

    @unittest.skip("No CLI in this branch")
    def test_print_version(self):
        """Check if easydms prints version string"""
        sys.argv = [sys.argv[0], "--version"]
        with self.assertRaises(SystemExit) as cm:
            pass
        self.assertEqual(cm.exception.code, None)


class TestVersionCmd(TestCaseCommandline):
    def setUp(self):
        super(TestVersionCmd, self).setUp()

        self.io.install()

    @unittest.skip("No CLI in this branch")
    def test_print_version(self):
        """Check if easydms can be called and exits zero"""
        self.call("easydms", ["--version"])
