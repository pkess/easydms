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

import datetime


class document(object):
    """Representation of a document"""
    def __init__(self, path=None, date=None):
        self.path = path
        if date is not None:
            self.date = date
        else:
            self.__date = None

    def __del__(self):
        pass

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        if not isinstance(date, datetime.date):
            raise TypeError("date should be of type datetime.date"
                            ", {0} given".format(type(date)))
        self.__date = date

    def guess_document_date(doc):
        """Guess the date of this document.
        This will check the content of a pdf for a usable date in common format

        Current implementation returns todays date.
        """
        return datetime.date.today()
