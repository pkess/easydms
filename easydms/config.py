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

import platform
import os

UNIX_DIR_VAR           = 'XDG_CONFIG_HOME'
UNIX_DIR_FALLBACK      = '~/.config'

WINDOWS_DIR_VAR        = 'APPDATA'
WINDOWS_DIR_FALLBACK   = '~\\AppData\\Roaming'

MAC_DIR                = '~/Library/Application Support'

CONFIG_FILENAME        = 'easydms.yaml'


class ErrorNoConfiguration(Exception):
    """No Configuration could be loaded
    """


class Config(object):
    """Central configuration of easydms
    """
    def __init__(self, path=None):
        if path is not None:
            self.path = path
        else:
            self.path = config_location()

        self.confFile = None
        try:
            self.confFile = open(self.path, 'r')
        except IOError:
            raise ErrorNoConfiguration(self.path)

    def __del__(self):
        if self.confFile is not None:
            self.confFile.close()

    def __repr__(self):
        self.confFile.seek(0)
        out = self.confFile.read()
        return out


def list_config_locations():
    """Return a platform-specific list of candidates for user
    configuration locations on the system

    The candidates are in order of priority, from highest to lowest. The
    last element is the "fallback" location to be used when no
    higher-priority config file exists.
    """
    paths = []

    if platform.system() == 'Darwin':
        paths.append(MAC_DIR)
        paths.append(UNIX_DIR_FALLBACK)
        if UNIX_DIR_VAR in os.environ:
            paths.append(os.environ[UNIX_DIR_VAR])

    elif platform.system() == 'Windows':
        paths.append(WINDOWS_DIR_FALLBACK)
        if WINDOWS_DIR_VAR in os.environ:
            paths.append(os.environ[WINDOWS_DIR_VAR])

    else:
        # Assume Unix.
        paths.append(UNIX_DIR_FALLBACK)
        if UNIX_DIR_VAR in os.environ:
            paths.append(os.environ[UNIX_DIR_VAR])

    # Expand and deduplicate paths.
    out = []
    for path in paths:
        path = os.path.join(path, CONFIG_FILENAME)
        path = os.path.abspath(os.path.expanduser(path))
        if path not in out:
            out.append(path)
    return out


def config_location():
    """Test platform-specific list of candidates for user configurtion
    locations for existing configurtion

    Will return an existing configuration or a place to create a new
    configuration"""
    paths = list_config_locations()

    for path in paths:
        try:
            f = open(path, 'r')
            f.close()
            return path
        except IOError:
            pass

    for path in paths:
        try:
            f = open(path, 'w')
            f.close()
            return path
        except IOError:
            pass

    raise ErrorNoConfiguration(paths)
