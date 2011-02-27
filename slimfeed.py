#!/usr/bin/env python
#    Copyright 2011 by Andreas Pakulat <apaku@gmx.de>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
#    02110-1301  USA.

import initsip
initsip.setupSipApi()
from PyQt4 import QtCore, QtGui, uic
from feedmanager import FeedManager
from feedmodel import FeedModel
from entrymodel import EntryModel
from addfeeddlg import AddFeedDlg
import sys


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        uic.loadUi("slimfeed.ui", self)
        self.feedMgr = FeedManager()
        self.feedModel = FeedModel(self.feedMgr, self)
        self.entryModel = EntryModel(parent=self)
        self.feedList.setModel(self.feedModel)
        self.entryList.setModel(self.entryModel)
        self.actionAbout.triggered.connect(self.showAbout)
        self.actionAboutQt.triggered.connect(QtGui.qApp.aboutQt)
        self.actionAdd.triggered.connect(self.addFeed)

    def addFeed(self):
        AddFeedDlg.open(self,self.feedModel)

    def showAbout(self):
        txt = """
<b>Slimfeed</b><br />
<br />
Version: 1.0.0<br />
A samll and fast feed reader<br />
<br />
Copyright 2011 Andreas Pakulat <apaku@gmx.de>
"""
        QtGui.QMessageBox.about(self, "About Slimfeed", txt)
    

def main():
    app = QtGui.QApplication(sys.argv)
    icon = QtGui.QIcon()
    icon.addFile("icons/slimfeed_16.png", QtCore.QSize(16,16))
    icon.addFile("icons/slimfeed_22.png", QtCore.QSize(22,22))
    icon.addFile("icons/slimfeed_32.png", QtCore.QSize(32,32))
    icon.addFile("icons/slimfeed_32.png", QtCore.QSize(32,32))
    icon.addFile("icons/slimfeed_64.png", QtCore.QSize(64,64))
    icon.addFile("icons/slimfeed_128.png", QtCore.QSize(128,128))
    app.setWindowIcon(icon)
    mainwin = MainWindow()
    mainwin.actionQuit.triggered.connect(app.quit)
    mainwin.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
