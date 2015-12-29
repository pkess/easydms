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
import tempfile
import shutil
import subprocess

# Use unittest2 on Python < 2.7.
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class InputException(Exception):
    def __init__(self, output=None):
        self.output = output

    def __str__(self):
        msg = "Attempt to read with no input provided."
        if self.output is not None:
            msg += " Output: %s" % self.output
        return msg


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

        # Initialize, but don't install, a DummyIO.
        self.io = DummyIO()

    def tearDown(self):
        if os.path.isdir(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        if self._old_home is None:
            del os.environ['HOME']
        else:
            os.environ['HOME'] = self._old_home

        self.io.restore()

    def createConfigDir(self):
        configpath = os.path.join(self.temp_dir, ".config")
        os.mkdir(configpath)

    def assertExists(self, path):
        self.assertTrue(os.path.exists(path),
                        'file does not exist: {!r}'.format(path))

    def assertNotExists(self, path):
        self.assertFalse(os.path.exists(path),
                         'file exists: {!r}'.format((path)))


class TestCaseCommandline(TestCase):
    """A TestCase which will invoke programm on commandline
    """
    def setUp(self):
        super(TestCaseCommandline, self).setUp()

    def call(self, prog, arg=[]):
        cmd = list(arg)
        cmd.insert(0, prog)
        p = subprocess.Popen(cmd, stdin=self.io.stdin, stdout=self.io.stdout,
                             stderr=self.io.stdout)
        return p.wait()


class DummyOut(object):
    """Collect output of tests to report only on failure
    """
    encoding = 'utf8'

    def __init__(self):
        self.f = tempfile.TemporaryFile()

    def write(self, s):
        self.f.write(s)

    def get(self):
        return self.f.read()

    def clear(self):
        self.f.seek(0)
        self.f.truncate()

    def fileno(self):
        if self.f is None:
            self.f = tempfile.TemporaryFile()

        return self.f.fileno()


class DummyIn(object):
    """Simulate input for tests
    """
    encoding = 'utf8'

    def __init__(self, out=None):
        self.f = None
        self.buf = []
        self.reads = 0
        self.out = out

    def add(self, s):
        self.buf.append(s + b'\n')

    def readline(self):
        if not self.buf:
            if self.out:
                raise InputException(self.out.get())
            else:
                raise InputException()
        self.reads += 1
        return self.buf.pop(0)

    def clear(self):
        self.buf = []
        if self.f is not None:
            self.f.seek(0)
            self.f.truncate()

    def fileno(self):
        if self.f is None:
            self.f = tempfile.TemporaryFile()
            for l in self.buf:
                self.f.write(l)
            self.f.seek(0)

        return self.f.fileno()


class DummyIO(object):
    """Mocks input and output streams for testing UI code."""
    def __init__(self):
        self.stdout = DummyOut()
        self.stdin = DummyIn(self.stdout)

    def addinput(self, s):
        self.stdin.add(s)

    def getoutput(self):
        res = self.stdout.get()
        self.stdout.clear()
        return res

    def readcount(self):
        return self.stdin.reads

    def clear(self):
        self.stdin.clear()
        self.stdout.clear()

    def install(self):
        sys.stdin = self.stdin
        sys.stdout = self.stdout

    def restore(self):
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__
