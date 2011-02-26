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
from PyQt4 import QtGui, uic
from feedmanager import FeedManager
from feedmodel import FeedModel
from entrymodel import EntryModel
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


def main():
    app = QtGui.QApplication(sys.argv)
    mainwin = MainWindow()
    mainwin.actionQuit.triggered.connect(app.quit)
    mainwin.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
