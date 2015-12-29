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

from _common import TestCase, TestCaseCommandline
import tempfile
import os
import sys
import shutil

import easydms.config
import easydms.cli


class TestConfig(TestCase):
    def setUp(self):
        super(TestConfig, self).setUp()
        self.createConfigDir()
        self.io.install()

    def test_nonexisting_config(self):
        """Check behaviour of not existing configuration file"""
        try:
            tempdir = tempfile.mkdtemp()
            filename = os.path.join(tempdir, "Config.yaml")
            with self.assertRaises(easydms.config.ErrorNoConfiguration):
                easydms.config.Config(filename)

            with self.assertRaises(SystemExit) as cm:
                sys.argv = ["prog", "-c", filename]
                easydms.cli.main()
            self.assertNotEqual(cm.exception.code, 0)

        finally:
            shutil.rmtree(tempdir)

    def test_dump_config(self):
        """Check dump of config"""
        config = easydms.config.Config()
        print(config)
        self.io.stdout.clear()
        sys.argv = ["prog", "config", "dump"]
        with self.assertRaises(SystemExit):
            easydms.cli.main()

    def test_get_key(self):
        """Check getkey method of config"""
        pairs = {'library': '~/home/documents/dms',
                 'key': 'value',
                 }
        try:
            tempconfig = tempfile.NamedTemporaryFile(
                suffix=".yaml", delete=False)
            for key, value in pairs.iteritems():
                tempconfig.write("{0}: {1}\n".format(key, value))
            tempconfig.close()
            config = easydms.config.Config(tempconfig.name)

            for key, value in pairs.iteritems():
                self.assertEqual(config.getKey(key, "Spam"), value)
            for key, value in pairs.iteritems():
                self.assertEqual(config.getRequiredKey(key), value)
        finally:
            os.remove(tempconfig.name)

    def test_get_invalid_key(self):
        """Check getkey method of config with not existing key"""
        pairs = {'library': '~/home/documents/dms',
                 'key': 'value',
                 }
        exceptionKeys = ['Hello', 'spam']
        try:
            tempconfig = tempfile.NamedTemporaryFile(
                suffix=".yaml", delete=False)
            tempconfig.write('ham: eggs')
            tempconfig.close()
            config = easydms.config.Config(tempconfig.name)

            for key, value in pairs.iteritems():
                self.assertEqual(config.getKey(key, value), value)

            for key in exceptionKeys:
                with self.assertRaises(easydms.config.ErrorConfigKeyNotFound):
                    config.getRequiredKey(key)
        finally:
            os.remove(tempconfig.name)

    def test_create_dir(self):
        dmsdir = '~/documents/dms'
        configfilePath = os.path.expanduser("~/.config/easydms.yaml")
        configfile = open(configfilePath, mode="w")
        configfile.write('library: easydms.db\n')
        configfile.write('directory: {0}\n'.format(dmsdir))
        configfile.close()

        with self.assertRaises(SystemExit):
            self.io.addinput("n")
            sys.argv = ["prog"]
            easydms.cli.main()
        self.assertNotExists(os.path.expanduser(dmsdir))
        self.io.addinput("y")
        sys.argv = ["prog"]
        easydms.cli.main()
        self.assertExists(os.path.expanduser(dmsdir))
        sys.argv = ["prog"]
        easydms.cli.main()
        self.assertExists(os.path.expanduser(dmsdir))


class TestConfigCmd(TestCaseCommandline):
    def setUp(self):
        super(TestConfigCmd, self).setUp()
        self.createConfigDir()

    def test_nonexisting_config_cmd(self):
        """Check behaviour of not existing configuration file"""
        try:
            tempdir = tempfile.mkdtemp()
            filename = os.path.join(tempdir, "Config.yaml")
            ret = self.call("easydms", ["-c {0}".format(filename)])
            self.assertNotEqual(ret, 0)
        finally:
            shutil.rmtree(tempdir)

    def test_dump_config_cmd(self):
        """Check dump of config by commandline invoke"""
        ret = self.call("easydms", ["config", "dump"])
        self.assertEqual(ret, 0)
