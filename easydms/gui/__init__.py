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
import shutil
import sys
import easydms.config
from PyQt5.QtCore import (
    Qt,
    QDate,
    QDir,
    QThread,
    QObject, pyqtSignal, pyqtSlot,
    QStringListModel,
)
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMessageBox,
    QFormLayout, QHBoxLayout, QPushButton,
    QLineEdit, QDateEdit, QFileDialog,
    QLabel,
    QCompleter,
)
from .pdfViewerWidget import pdfViewerWidget
from .. import ocrmypdfwrapper


class mainWidget(QWidget):
    procOcr = None
    fileToOcr = pyqtSignal(str)
    styleLblOCRrunning = "background: yellow"
    styleLblOCRfinished = "background: green"

    def __init__(self, config):
        super(mainWidget, self).__init__()
        self.dmsDirectory = ""

        if not mainWidget.procOcr:
            mainWidget.procOcr = QThread(self)
            mainWidget.procOcr.start()

        self.ocrW = ocrWorker()
        self.fileToOcr.connect(self.ocrW.do, Qt.QueuedConnection)
        self.ocrW.finished.connect(self.ocrFinished)
        self.ocrW.moveToThread(self.procOcr)

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
        self.compNames = QStringListModel()
        self.inpCompanyNameCompleter = QCompleter(self.compNames, self)
        self.inpCompanyNameCompleter.setCaseSensitivity(Qt.CaseInsensitive)
        self.inpCompanyName.setCompleter(self.inpCompanyNameCompleter)
        self.inpDate = QDateEdit()
        self.inpDate.setDate(QDate.currentDate())
        self.btnStoreDoc = QPushButton(self.tr("Store document"))
        self.btnStoreDoc.clicked.connect(self.storeDoc)
        self.btnStoreDoc.setEnabled(False)
        self.lblOcrProgress = QLabel(self.tr("OCR not started"))
        self.lblOcrProgress.setAlignment(Qt.AlignCenter)
        self.layLeftPane.addRow(self.btnLoadDoc)
        self.layLeftPane.addRow(self.tr("Company Name"), self.inpCompanyName)
        self.layLeftPane.addRow(self.tr("Date"), self.inpDate)
        self.layLeftPane.addRow(self.btnStoreDoc)
        self.layLeftPane.addRow(self.lblOcrProgress)

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
            self.ocrDoc(filepath)
            self.origFilePath = filepath

    def ocrDoc(self, filepath):
        try:
            self.btnLoadDoc.setEnabled(False)
            self.btnStoreDoc.setEnabled(False)
            self.fileToOcr.emit(filepath)
            self.wdgViewer.setFile(filepath)
            self.lblOcrProgress.setStyleSheet(self.styleLblOCRrunning)
            self.lblOcrProgress.setText(self.tr("OCR running"))
            self.ocrFileName = None
        except:
            print("Error during ocr")
            print(sys.exc_info())

    def ocrFinished(self, newFilename):
        self.btnLoadDoc.setEnabled(True)
        self.btnStoreDoc.setEnabled(True)
        self.lblOcrProgress.setStyleSheet(self.styleLblOCRfinished)
        self.lblOcrProgress.setText(self.tr("OCR finished"))
        self.ocrFileName = newFilename
        self.wdgViewer.setFile(self.ocrFileName)

    def storeDoc(self):
        if not self.ocrFileName:
            QMessageBox.warning(
                self, "easydms", self.tr(
                    "No file was prcessed"
                )
            )
            return
        compName = self.inpCompanyName.text()
        if self.dmsDirectory == "":
            raise Exception("dmsDirectory was not set")
        if compName == "":
            QMessageBox.warning(
                self, "easydms", self.tr(
                    "Company name is empty"
                )
            )
            return
        self.btnStoreDoc.setEnabled(False)
        date = self.inpDate.date()
        year = date.year()
        month = date.month()
        day = date.day()
        nr = 1
        while True:
            path = os.path.join(
                self.dmsDirectory,
                "{:04d}".format(year),
                compName
            )
            newFileName = os.path.join(
                path,
                "{0:04d}-{1:02d}-{2:02d}_{3:03d}.pdf".format(
                    year, month, day, nr
                )
            )
            if os.path.exists(newFileName):
                nr = nr + 1
                continue
            break
        os.makedirs(path, exist_ok=True)
        shutil.copyfile(self.ocrFileName, newFileName)
        os.remove(self.ocrFileName)
        os.remove(self.origFilePath)
        self.wdgViewer.setFile("")
        self.ocrFileName = ""
        self.origFilePath = ""
        self.determineCompanyAutoCompletion()

    def setDmsDirectory(self, path):
        self.dmsDirectory = path
        self.determineCompanyAutoCompletion()

    @pyqtSlot()
    def determineCompanyAutoCompletion(self):
        compNames = set()
        dirs = os.listdir(self.dmsDirectory)
        for d in dirs:
            paths = os.path.join(self.dmsDirectory, d)
            names = os.listdir(paths)
            for n in names:
                compNames.add(n)
        self.compNames.setStringList(compNames)


class ocrWorker(QObject):
    finished = pyqtSignal(str)

    def __init__(self):
        super(ocrWorker, self).__init__()

    @pyqtSlot(str)
    def do(self, filepath):
        newName = ocrmypdfwrapper.ocr(filepath)
        self.finished.emit(newName)


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
        w.setDmsDirectory(dmsdirectory)

        sys.exit(a.exec_())

    except easydms.config.ErrorNoConfiguration as e:
        msg = ("Error: Could not load configuration\n"
               "following path(s) were searched:\n"
               "{0}").format(e)
        sys.exit(msg)


if __name__ == '__main__':
    main()
