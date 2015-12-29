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

import sqlite3


class ErrorDatabaseStructure(Exception):
    """Existing database structure does not match programmed structure"""


class Database(object):
    """Central Database abstraction layer of easydms"""
    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(self.path)

    def __del__(self):
        self.conn.close()

    def create_db(self):
        self.create_table(
            u"document", (u"id", u"INTEGER"),
            [(u"path", u"TEXT"), (u"date", u"TEXT")])
        self.conn.commit()

    def create_table(self, name, primary, fields):
        """Create a table if not already existing

        Will extend existing table automatically if new rows columns are
        requested"""
        query = """CREATE TABLE IF NOT EXISTS {0}
                ({1} {2} PRIMARY KEY""".format(
                name, primary[0], primary[1])
        for field in fields:
            query = "{0}, {1} {2}".format(query, field[0], field[1])
        query = "{0})".format(query)
        self.conn.execute(query)
        fields.insert(0, primary)
        self.check_table(name, fields)

    def check_table(self, table, fields):
        """Check if table layout in db matches expected layout"""
        query = "PRAGMA table_info({0})".format(table)
        result = self.conn.execute(query)
        rows = result.fetchall()
        rowmap = dict()
        for row in rows:
            rowmap[row[1]] = row[2]
        fieldmap = dict()
        for field in fields:
            fieldmap[field[0]] = field[1]
        rowmap = rowmap.viewitems()
        fieldmap = fieldmap.viewitems()
        newFields = fieldmap - rowmap
        changedFields = rowmap ^ fieldmap
        if len(changedFields) != 0:
            if newFields == changedFields:
                self.add_columns(table, newFields)
            elif len(changedFields) != 0:
                raise ErrorDatabaseStructure(changedFields, rowmap, fieldmap)

    def add_columns(self, table, cols):
        raise Exception("Not implemented: extend db")
