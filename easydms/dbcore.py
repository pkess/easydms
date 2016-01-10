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

import easydms


class ErrorDatabaseStructure(Exception):
    """Existing database structure does not match programmed structure"""


class ErrorDatabaseContent(Exception):
    """Database is corrupted with wrong data"""


class ErrorDatabaseInsert(Exception):
    """Unable to insert into db"""


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
        self.create_table(u"tag", (u"name", u"TEXT"), [])
        self.create_table(
            u"tagalternative", (u"name", u"TEXT"), [(u"tag", u"TEXT")])
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
        rowmap = rowmap.items()
        fieldmap = fieldmap.items()
        newFields = fieldmap - rowmap
        changedFields = rowmap ^ fieldmap
        if len(changedFields) != 0:
            if newFields == changedFields:
                self.add_columns(table, newFields)
            elif len(changedFields) != 0:
                raise ErrorDatabaseStructure(changedFields, rowmap, fieldmap)

    def add_columns(self, table, cols):
        """Add defined number of columns to a table"""
        raise Exception("Not implemented: extend db")

    def get_primary_tag(self, tag):
        """Get the primary tag to be used as reference
        in other tables from db

        returns None if key does not exist
        """
        query = """SELECT * FROM
                       (SELECT tag.name as tagname,
                               tagalternative.name as tagalt
                        FROM tagalternative INNER JOIN tag
                        ON tag.name = tagalternative.tag
                        UNION
                        SELECT tag.name as tagname, tag.name as tagalt
                        FROM tag
                        WHERE tagalt = "{0}"
                       )
                   WHERE tagalt = "{0}" """.format(tag)
        result = self.conn.execute(query)
        row = result.fetchone()
        if row is not None:
            tagname = row[0]
            if len(result.fetchall()) > 0:
                raise ErrorDatabaseContent("Tag '{0}' is defined "
                                           "more than once but should "
                                           "be unique".format(tag))
            return tagname
        return None

    def get_tag_alternatives(self, tag):
        """Get alternative names for tag from db

        returns list of alternatives for tag
        """
        query = """SELECT tagalternative.name as tagalt
                FROM tagalternative INNER JOIN tag
                ON tag.name = tagalternative.tag
                WHERE tag.name = "{0}" """.format(tag)
        result = self.conn.execute(query)
        ret = []
        for res in result:
            ret.append(res[0])
        return ret

    def get_tag(self, tag):
        """Get a tag with its alternative names from db

        return a documentTag or None if tag does not exist
        """
        ret = documentTag()
        ret.primary = self.get_primary_tag(tag)
        if ret.primary is not None:
            ret.alternatives = self.get_tag_alternatives(ret.primary)
            return ret
        return None

    def insert_tag(self, tag, alternatives=[]):
        """Insert a tag or alternative names for tag to database

        return a documentTag for tag like get_tag would do
        """
        docTag = self.get_tag(tag)
        if docTag is None:
            query = """INSERT INTO tag (name) VALUES ('{0}')""".format(tag)
            self.conn.execute(query)
            docTag = documentTag()
            docTag.primary = tag

        for alt in alternatives:
            if self.get_tag(alt) is not None:
                raise ErrorDatabaseInsert("Cannot insert alternative name "
                                          "'{0}'. Tag already "
                                          "defined".format(alt))
            query = """INSERT INTO tagalternative (name, tag)
                       VALUES ('{0}', '{1}')""".format(alt, docTag.primary)
            self.conn.execute(query)
            docTag.alternatives.append(alt)

        self.conn.commit()
        return docTag

    def insert_document(self, doc):
        """Insert a document to database"""
        if not isinstance(doc, easydms.document):
            raise TypeError("doc should be of type easydms.document"
                            ", {0} given".format(type(doc)))

        query = """INSERT INTO document (path, date) VALUES
        ('{0}','{1}')""".format(doc.path, str(doc.date))
        self.conn.execute(query)
        self.conn.commit()


class documentTag():
    """Class to represent a tag"""
    def __init__(self, primary=None, alternatives=[]):
        self.primary = primary
        self.alternatives = alternatives

    def __str__(self):
        return "documentTag ({0}): {1}".format(self.primary, self.alternatives)
