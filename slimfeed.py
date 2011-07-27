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
from PyQt4.QtCore import QModelIndex, QUrl, pyqtSignal
from PyQt4.QtGui import QItemSelectionModel
from feedmanager import FeedManager
from feedmodel import FeedModel
from entrymodel import EntryModel
from feedparserfactory import createFeedFromData
from threading import Thread
import feedparser
import sys


def updateFeeds(*args):
    mainwin = args[0]
    updated = mainwin.feedMgr.update()
    mainwin.updated.emit(updated)

class MainWindow(QtGui.QMainWindow):
    updated = pyqtSignal(list)
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        uic.loadUi("slimfeed.ui", self)
        self.feedMgr = FeedManager()

        # Restore settings, this includes feeds
        self._readSettings()

        self.feedModel = FeedModel(self.feedMgr, self)
        self.feedToolBar = QtGui.QToolBar(self.feedToolBarContainer)
        self.entryToolBar = QtGui.QToolBar(self.entryToolBarContainer)
        self.browserToolBar = QtGui.QToolBar(self.browserToolBarContainer)

        self.setupListToolBars()

        self.entryModel = EntryModel(parent=self)
        self.feedList.setModel(self.feedModel)
        self.entryList.setModel(self.entryModel)

        self.entryModel.entriesChanged.connect(self.feedModel.entriesUpdated)

        self.actionAbout.triggered.connect(self.showAbout)
        self.actionAboutQt.triggered.connect(QtGui.qApp.aboutQt)
        self.actionAdd.triggered.connect(self.addFeed)
        self.actionDeleteFeed.triggered.connect(self.deleteSelectedFeed)
        self.actionDeleteEntry.triggered.connect(self.deleteSelectedEntry)
        self.feedList.selectionModel().selectionChanged.connect(
                self.feedSelectionChanged)
        self.entryList.selectionModel().selectionChanged.connect(
                self.entrySelectionChanged)
        self.feedList.addAction(self.actionDeleteFeed)
        self.updateTimer = QtCore.QTimer()
        self.updateTimer.timeout.connect(self.updateFeeds)
        self.updateTimer.start(6000)
        # Need to do this async, _readSettings is done too early and
        # hence the size is being overwritten somehow later on
        QtCore.QTimer.singleShot(0, self._loadViewSizes)

        self.entryList.selectionModel().currentChanged.connect(self.currentEntryChanged)
        self.markReadTimer = QtCore.QTimer()
        self.markReadTimer.setSingleShot(True)
        self.markReadTimer.timeout.connect(self.markEntryRead)

        self.updated.connect(self.feedsUpdated, QtCore.Qt.QueuedConnection)

    def markEntryRead(self):
        if self.markReadIdx is not None and self.markReadIdx.isValid():
            self.entryModel.markRead(self.markReadIdx)

    def currentEntryChanged(self, idx1, idx2):
        self.markReadIdx = idx1
        self.markReadTimer.start(500)
        entry = self.entryModel.entryFromIndex(idx1)
        self.browser.setUrl(QUrl(entry.url))

    def updateFeeds(self):
        self.updateThread = Thread(target=updateFeeds, name="Updating Feeds", args=(self,))
        self.updateThread.start()

    @QtCore.pyqtSlot(list)
    def feedsUpdated(self, updated):
        self.updateThread = None
        feedModelRow = self.feedList.currentIndex().row()
        entryModelRow = self.entryList.currentIndex().row()
        self.feedModel.feedsUpdated(updated)
        self.entryModel.feedsUpdated(updated)
        self.updateTimer.start(6000)

    def _setupToolBar(self, toolbar, container, actions):
        container.setLayout(QtGui.QVBoxLayout())
        container.layout().setSpacing(0)
        container.layout().setContentsMargins(0, 0, 0, 0)
        container.layout().addWidget(toolbar)
        for action in actions:
            toolbar.addAction(action)
        toolbar.setIconSize(QtCore.QSize(8, 8))

    def setupListToolBars(self):
        self._setupToolBar(self.feedToolBar, self.feedToolBarContainer, [self.actionDeleteFeed,])
        self._setupToolBar(self.entryToolBar, self.entryToolBarContainer, [self.actionDeleteEntry, ])
        self._setupToolBar(self.browserToolBar, self.browserToolBarContainer, [self.actionBack,self.actionForward,self.actionStop,self.actionReload])

    def feedSelectionChanged(self):
        selection = self.feedList.selectionModel().selectedRows()
        self.actionDeleteFeed.setEnabled((len(selection) > 0))
        if len(selection) > 0:
            self.entryModel.feed = self.feedModel.getFeed(selection[0])
        else:
            self.entryModel.feed = None

    def entrySelectionChanged(self):
        selection = self.entryList.selectionModel().selectedRows()
        self.actionDeleteEntry.setEnabled((len(selection) > 0))

    def deleteSelectedEntry(self):
        selection = self.entryList.selectionModel().selectedRows()
        if len(selection) > 0:
            entry = self.entryModel.entryFromIndex(selection[0])
            if QtGui.QMessageBox.question(self,
                    "Delete Feed",
                    "Do you really want to delete the article '%s'" % (entry.title),
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                    QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
                self.entryModel.removeEntry(selection[0])


    def deleteSelectedFeed(self):
        selection = self.feedList.selectionModel().selectedRows()
        feed = self.feedModel.getFeed(selection[0])
        if QtGui.QMessageBox.question(self,
                "Delete Feed",
                "Do you really want to delete the feed '%s'" % (feed.title),
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
            self.feedModel.deleteFeed(feed)

    def _restoreHeaderView(self, settings, view):
        view.horizontalHeader().restoreState(
                settings.value("Horizontal Header State", QtCore.QByteArray()))
        for grp in settings.childGroups():
            if "Column" in grp:
                col = int(grp.split(" ")[1])
                settings.beginGroup(grp)
                size = view.horizontalHeader().sectionSize(col)
                newsize = int(settings.value("Width", size))
                view.horizontalHeader().resizeSection(col, newsize)
                settings.endGroup()

    def _loadViewSizes(self):
        settings = QtCore.QSettings("de.apaku", "Slimfeed")
        settings.beginGroup("EntryList")
        self._restoreHeaderView(settings, self.entryList)
        settings.endGroup()
        settings.beginGroup("FeedList")
        self._restoreHeaderView(settings, self.feedList)
        settings.endGroup()

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
        settings.beginGroup("EntryList")
        settings.setValue("Horizontal Header State", 
                self.entryList.horizontalHeader().saveState())
        for col in range(0, self.entryList.horizontalHeader().count()):
            settings.beginGroup("Column %d" % col)
            settings.setValue("Width", 
                    self.entryList.horizontalHeader().sectionSize(col))
            settings.endGroup()
        settings.endGroup()
        settings.beginGroup("FeedList")
        settings.setValue("Horizontal Header State", 
                self.feedList.horizontalHeader().saveState())
        for col in range(0, self.feedList.horizontalHeader().count()):
            settings.beginGroup("Column %d" % col)
            settings.setValue("Width", 
                    self.feedList.horizontalHeader().sectionSize(col))
            settings.endGroup()
        settings.endGroup()
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
