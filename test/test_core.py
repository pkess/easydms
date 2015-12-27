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

"""Test core funtionalities."""

from _common import unittest
import tempfile
import os
import shutil
from subprocess import call

import easydms.config


class TestConfig(unittest.TestCase):
    def setUp(self):
        super(TestConfig, self).setUp()

    def test_nonexisting_config(self):
        """Check behaviour of not existing configuration file"""
        try:
            tempdir = tempfile.mkdtemp()
            filename = os.path.join(tempdir, "Config.yaml")
            with self.assertRaises(easydms.config.ErrorNoConfiguration):
                easydms.config.Config(filename)
        finally:
            shutil.rmtree(tempdir)

    def test_nonexisting_config_cmd(self):
        """Check behaviour of not existing configuration file"""
        try:
            tempdir = tempfile.mkdtemp()
            filename = os.path.join(tempdir, "Config.yaml")
            ret = call(["easydms", "-c {0}".format(filename)])
            self.assertNotEqual(ret, 0)
        finally:
            shutil.rmtree(tempdir)

    def test_dump_config(self):
        """Check dump of config"""
        config = easydms.config.Config()
        print(config)

    def test_dump_config_cmd(self):
        """Check dump of config by commandline invoke"""
        ret = call(["easydms", "config", "dump"])
        self.assertEqual(ret, 0)