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

import os
import tempfile
import shutil

# Use unittest2 on Python < 2.7.
try:
    import unittest2 as unittest
except ImportError:
    import unittest


# A test harness for all easydms tests.
# Provides temporary, isolated configuration.
class TestCase(unittest.TestCase):
    """A unittest.TestCase subclass that saves and restores easydms'
    global configuration. This allows tests to make temporary
    modifications that will then be automatically removed when the test
    completes. Also provides some additional assertion methods, a
    temporary directory, and a DummyIO.
    """
    def setUp(self):
        # Direct paths to a temporary directory. Tests can also use this
        # temporary directory.
        self.temp_dir = tempfile.mkdtemp()

        # Set $HOME, which is used by confit's `config_dir()` to create
        # directories.
        self._old_home = os.environ.get('HOME')
        os.environ['HOME'] = self.temp_dir

    def tearDown(self):
        if os.path.isdir(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        if self._old_home is None:
            del os.environ['HOME']
        else:
            os.environ['HOME'] = self._old_home

    def assertExists(self, path):
        self.assertTrue(os.path.exists(path),
                        'file does not exist: {!r}'.format(path))

    def assertNotExists(self, path):
        self.assertFalse(os.path.exists(path),
                         'file exists: {!r}'.format((path)))
