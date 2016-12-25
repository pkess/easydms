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
import easydms.config
from PyQt5.QtCore import (
    QDate,
    QDir,
)
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMessageBox,
    QFormLayout, QHBoxLayout, QPushButton,
    QLineEdit, QDateEdit, QFileDialog
)
from .pdfViewerWidget import pdfViewerWidget


class mainWidget(QWidget):
    def __init__(self, config):
        super(mainWidget, self).__init__()
        self.config = config
        layout = QHBoxLayout(self)
        self.setLayout(layout)
        self.layLeftPane = QFormLayout()

        self.wdgViewer = pdfViewerWidget(self.config)
        self.wdgViewer.setMinimumSize(200, 200)
        self.wdgLeftPane = QWidget()
        self.wdgLeftPane.setMaximumWidth(200)
        self.wdgLeftPane.setLayout(self.layLeftPane)
        layout.addWidget(self.wdgLeftPane)
        layout.addWidget(self.wdgViewer)
        self.btnLoadDoc = QPushButton(self.tr("Load document"))
        self.btnLoadDoc.clicked.connect(self.loadDoc)
        self.inpCompanyName = QLineEdit()
        self.inpDate = QDateEdit()
        self.inpDate.setDate(QDate.currentDate())
        self.btnStoreDoc = QPushButton(self.tr("Store document"))
        self.btnStoreDoc.clicked.connect(self.storeDoc)
        self.layLeftPane.addRow(self.btnLoadDoc)
        self.layLeftPane.addRow(self.tr("Company Name"), self.inpCompanyName)
        self.layLeftPane.addRow(self.tr("Date"), self.inpDate)
        self.layLeftPane.addRow(self.btnStoreDoc)

    def loadDoc(self):
        defaultDir = self.config.getKey('default_import_dir', None)
        if defaultDir:
            defaultDir = os.path.expanduser(defaultDir)
        else:
            defaultDir = QDir.homePath()

        (filepath, filt) = QFileDialog.getOpenFileName(
            caption=self.tr("Load document"),
            directory=defaultDir,
            filter=self.tr("Documents (*.pdf)")
        )
        if filepath:
            self.wdgViewer.setFile(filepath)

    def storeDoc(self):
        pass


def main():
    try:
        config = easydms.config.Config()

        a = QApplication(sys.argv)
        w = mainWidget(config)
        w.show()

        dmsdirectory = config.getRequiredKey('directory')
        dmsdirectory = os.path.expanduser(dmsdirectory)
        if not os.path.exists(dmsdirectory):
            reply = QMessageBox.question(
                w, "easydms",
                "Directory \"{0}\" does not exist. Create?".format(
                    dmsdirectory),
                defaultButton=QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                os.makedirs(dmsdirectory)
            else:
                sys.exit("Abort due to not existing directory")

        sys.exit(a.exec_())

    except easydms.config.ErrorNoConfiguration as e:
        msg = ("Error: Could not load configuration\n"
               "following path(s) were searched:\n"
               "{0}").format(e)
        sys.exit(msg)


if __name__ == '__main__':
    main()
