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

from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
)
from PyQt5.QtCore import (
    QUrl,
)
from PyQt5.QtGui import (
    QDesktopServices,
)
import subprocess


class pdfViewerWidget(QWidget):
    def __init__(self, config):
        super(pdfViewerWidget, self).__init__()
        self.config = config
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.btnOpenPdf = QPushButton(
            self.tr("Open PDF with external application"),
        )
        layout.addStretch()
        layout.addWidget(self.btnOpenPdf)
        layout.addStretch()
        self.filePath = ""
        self.btnOpenPdf.setEnabled(False)
        self.btnOpenPdf.clicked.connect(self.openFileExternal)

    def setFile(self, filePath):
        self.filePath = filePath
        self.btnOpenPdf.setEnabled(True)

    def openFileExternal(self):
        pdfViewer = self.config.getKey('pdfViewer', None)
        if pdfViewer:
            subprocess.Popen([pdfViewer, self.filePath])
        else:
            QDesktopServices.openUrl(
                QUrl("file:///{0}".format(self.filePath))
            )
