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
from feedparserfactory import createFeedFromData
import feedparser
import sys


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        uic.loadUi("slimfeed.ui", self)
        self.feedMgr = FeedManager()

        # Restore settings, this includes feeds
        self._readSettings()

        self.feedModel = FeedModel(self.feedMgr, self)
        self.feedToolBar = QtGui.QToolBar(self.feedToolBarContainer)
        self.entryToolBar = QtGui.QToolBar(self.entryToolBarContainer)

        self.setupListToolBars()

        self.entryModel = EntryModel(parent=self)
        self.feedList.setModel(self.feedModel)
        self.entryList.setModel(self.entryModel)
        self.actionAbout.triggered.connect(self.showAbout)
        self.actionAboutQt.triggered.connect(QtGui.qApp.aboutQt)
        self.actionAdd.triggered.connect(self.addFeed)
        self.actionDeleteFeed.triggered.connect(self.deleteSelectedFeed)
        self.feedList.selectionModel().selectionChanged.connect(
                self.feedSelectionChanged)
        self.feedList.addAction(self.actionDeleteFeed)

    def setupListToolBars(self):
        self.feedToolBarContainer.setLayout(QtGui.QVBoxLayout())
        self.feedToolBarContainer.layout().setSpacing(0)
        self.feedToolBarContainer.layout().setContentsMargins(0, 0, 0, 0)
        self.feedToolBarContainer.layout().addWidget(self.feedToolBar)
        self.feedToolBar.addAction(self.actionDeleteFeed)
        self.feedToolBar.setIconSize(QtCore.QSize(8, 8))
        self.entryToolBarContainer.setLayout(QtGui.QVBoxLayout())
        self.entryToolBarContainer.layout().setSpacing(0)
        self.entryToolBarContainer.layout().setContentsMargins(0, 0, 0, 0)
        self.entryToolBarContainer.layout().addWidget(self.entryToolBar)
        self.entryToolBar.setIconSize(QtCore.QSize(8, 8))

    def feedSelectionChanged(self):
        selection = self.feedList.selectionModel().selectedRows()
        self.actionDeleteFeed.setEnabled((len(selection) > 0))

    def deleteSelectedFeed(self):
        selection = self.feedList.selectionModel().selectedRows()
        feed = self.feedModel.getFeed(selection[0])
        if QtGui.QMessageBox.question(self,
                "Delete Feed",
                "Do you really want to delete the feed '%s'" % (feed.title),
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
            self.feedModel.deleteFeed(feed)

    def _readSettings(self):
        settings = QtCore.QSettings("de.apaku", "Slimfeed")
        self.restoreGeometry(settings.value("geometry", QtCore.QByteArray()))
        self.restoreState(settings.value("state", QtCore.QByteArray()))
        settings.beginGroup("Feeds")
        self.feedMgr.load(settings)
        settings.endGroup()

    def _writeSettings(self):
        settings = QtCore.QSettings("de.apaku", "Slimfeed")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("state", self.saveState())
        settings.beginGroup("Feeds")
        # Clear out all stored feeds so we don't carry around
        # any that might have been deleted meanwhile
        for grp in settings.childGroups():
            settings.remove(grp)
        self.feedMgr.save(settings)
        settings.endGroup()
        settings.sync()

    def closeEvent(self, event):
        self._writeSettings()
        return QtGui.QMainWindow.closeEvent(self, event)

    def addFeed(self):
        dlg = uic.loadUi("addfeeddlg.ui", QtGui.QDialog(self))
        if dlg.exec_() == QtGui.QDialog.Accepted:
            data = feedparser.parse(dlg.url.text())
            feed = createFeedFromData(data)
            self.feedModel.addFeed(feed)

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
    icon.addFile("icons/slimfeed_16.png", QtCore.QSize(16, 16))
    icon.addFile("icons/slimfeed_22.png", QtCore.QSize(22, 22))
    icon.addFile("icons/slimfeed_32.png", QtCore.QSize(32, 32))
    icon.addFile("icons/slimfeed_32.png", QtCore.QSize(32, 32))
    icon.addFile("icons/slimfeed_64.png", QtCore.QSize(64, 64))
    icon.addFile("icons/slimfeed_128.png", QtCore.QSize(128, 128))
    app.setWindowIcon(icon)
    mainwin = MainWindow()
    mainwin.actionQuit.triggered.connect(mainwin.close)
    mainwin.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
