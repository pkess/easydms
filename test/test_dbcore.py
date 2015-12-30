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

"""Test code in dbcore.py"""

from _common import testDataPath, TestCase
import tempfile
import os
import datetime

import easydms.dbcore


class TestDatabase(TestCase):
    def setUp(self):
        super(TestDatabase, self).setUp()
        self.io.install()

    def test_create_db_memory(self):
        """Check creation of new database without file
        Also used in other tests to create a database
        """
        self.db = easydms.dbcore.Database(":memory:")
        self.db.create_db()

    def test_create_db_file(self):
        """Check creation of new database with file"""
        try:
            tempdb = tempfile.NamedTemporaryFile(
                suffix=".db", delete=False)
            tempdb.close()
            db = easydms.dbcore.Database(tempdb.name)
            db.create_db()
        finally:
            os.remove(tempdb.name)

    def test_create_table(self):
        """Check creation of user defined tables

        A new table will be created with 4 cols
        The schema will be extended and created again
        A row will be changed and created again
        """
        db = easydms.dbcore.Database(":memory:")
        table = "tablename"
        primary = ("id", "INTEGER")
        fields = [
            ("col1", "INTEGER"),
            ("col2", "TEXT"),
            ("col3", "TEXT"),
        ]
        extended_fields = fields[:]
        extended_fields.append(("newCol", "INTEGER"))
        changed_fields = fields[:]
        changed_fields[2] = ("col4", "INTEGER")
        db.create_table(table, primary, fields)
        db.create_table(table, primary, fields)
        with self.assertRaises(Exception):
            db.create_table(table, primary, extended_fields)
        with self.assertRaises(easydms.dbcore.ErrorDatabaseStructure):
            db.create_table(table, primary, changed_fields)

    def test_add(self):
        self.test_create_db_memory()
        date = datetime.date(2015, 12, 30)
        doc = os.path.join(testDataPath, 'simplepdf.pdf')
        self.db.insert_document(doc, date)
        with self.assertRaises(TypeError):
            self.db.insert_document(doc, "Test")
