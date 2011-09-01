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
from PyQt4.QtCore import QUrl, pyqtSignal
from feedmanager import FeedManager
from feedmodel import FeedModel
from entrymodel import EntryModel
from preferences import Preferences
from feedparserfactory import createFeedFromData
from threading import Thread
from qsettingsutils import _readQSettingsIntEntry, _readQSettingsBoolEntry
import feedparser
import sys

class UpdateThread(Thread):
    def __init__(self, mainwin):
        Thread.__init__(self, name="Update Feeds")
        self.mainwin = mainwin

    def run(self):
        updated = self.mainwin.feedMgr.update()
        self.mainwin.updated.emit(updated)

class SlimApp(QtGui.QApplication):
    def __init__(self, args):
        QtGui.QApplication.__init__(self, args)
        self._aboutToQuit = False

    def commitData(self, sessMgr):
        self._aboutToQuit = True

    def isAboutToQuit(self):
        return self._aboutToQuit

class MainWindow(QtGui.QMainWindow):
    updated = pyqtSignal(list)
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # To be able to just hide to systray when closing the window and restore
        # the window via the systray icon need to set this to false
        QtGui.QApplication.setQuitOnLastWindowClosed(False)

        uic.loadUi("slimfeed.ui", self)
        self.feedMgr = FeedManager()

        # Restore settings, this includes feeds
        self._readSettings()

        self.feedModel = FeedModel(self.feedMgr, self)
        self.feedToolBar = QtGui.QToolBar(self.feedToolBarContainer)
        self.entryToolBar = QtGui.QToolBar(self.entryToolBarContainer)
        self.browserToolBar = QtGui.QToolBar(self.browserToolBarContainer)

        self.setupListToolBars()
        self.entryList.sortByColumn(2, QtCore.Qt.AscendingOrder)

        self.entryModel = EntryModel(parent=self)
        self.entryProxyModel = QtGui.QSortFilterProxyModel()
        self.entryProxyModel.setDynamicSortFilter(True)
        self.entryProxyModel.setSourceModel(self.entryModel)
        self.feedList.setModel(self.feedModel)
        self.entryList.setModel(self.entryProxyModel)

        self.entryModel.entriesChanged.connect(self.feedModel.entriesUpdated)

        # Directly call quit from our quit-action instead of going through the close
        # event since that just hides to systray
        self.actionQuit.triggered.connect(self.quit)
        self.actionAbout.triggered.connect(self.showAbout)
        self.actionAboutQt.triggered.connect(QtGui.qApp.aboutQt)
        self.actionPreferences.triggered.connect(self.showPreferences)
        self.actionAdd.triggered.connect(self.addFeed)
        self.actionDeleteFeed.triggered.connect(self.deleteSelectedFeed)
        self.actionDeleteEntry.triggered.connect(self.deleteSelectedEntry)
        self.actionMarkEntryAsImportant.triggered.connect(self.markSelectedEntriesImportant)
        self.feedList.selectionModel().selectionChanged.connect(
                self.feedSelectionChanged)
        self.entryList.selectionModel().selectionChanged.connect(
                self.entrySelectionChanged)
        self.feedList.addAction(self.actionDeleteFeed)
        self.updateTimer = QtCore.QTimer()
        self.updateTimer.timeout.connect(self.updateFeeds)
        self.updateThread = None
        self._startUpdateTimer()
        # Need to do this async, _readSettings is done too early and
        # hence the size is being overwritten somehow later on
        QtCore.QTimer.singleShot(0, self._restoreViews)

        self.entryList.selectionModel().currentChanged.connect(self.currentEntryChanged)
        self.markReadTimer = QtCore.QTimer()
        self.markReadTimer.setSingleShot(True)
        self.markReadTimer.timeout.connect(self.markEntryRead)

        # Start archive-timer if necessary
        self.archiveTimer = None
        self.checkArchiveTimer()

        self.updated.connect(self.feedsUpdated, QtCore.Qt.QueuedConnection)

        # Set up systray
        self.sysTray = QtGui.QSystemTrayIcon(QtGui.qApp.windowIcon(), self)
        self.updateSystrayIcon()
        self.sysTray.show()
        self.sysTray.activated.connect(self.sysTrayActivated)
        self.showAction = QtGui.QAction("Restore", self)
        self.showAction.triggered.connect(self.doShow)
        self.sysTrayMenu = QtGui.QMenu(self)
        self.sysTrayMenu.addAction(self.showAction)
        self.sysTrayMenu.addSeparator()
        self.sysTrayMenu.addAction(self.actionQuit)
        self.sysTray.setContextMenu(self.sysTrayMenu)

    def _startUpdateTimer(self):
        self.updateTimer.start(self.updateTimeout * 1000)

    def doShow(self):
        self.show()
        self.activateWindow()

    def checkArchiveTimer(self):
        if self.enableArticleDeletion:
            if self.archiveTimer is None:
                self.archiveTimer = QtCore.QTimer()
                self.archiveTimer.timeout.connect(self.archiveArticles)
            # First check after enabling is done after 60 seconds, the archive
            # function will then re-schedule for longer timeout
            self.archiveTimer.start(6000)
        elif self.archiveTimer is not None:
                self.archiveTimer.stop()
                self.archiveTimer.timeout.disconnect(self.archiveArticles)
                self.archiveTimer = None

    def archiveArticles(self):
        deleteableinfo = self.feedMgr.checkForArchiveableEntries(self.numberOfDaysEnabled, self.numberOfDays, 
                                                                 self.numberOfArticlesEnabled, self.numberOfArticles)
        # Now update the feeds, this may need to go through the entrymodel so that the indexes are updated properly,
        # hence cannot do this directly in the archiving-method above
        for info in deleteableinfo:
            feed = info["feed"]
            entries = info["entries"]
            isentrymodelfeed = self.entryModel.feed == feed
            for entry in entries:
                if isentrymodelfeed:
                    self.entryModel.removeEntry(self.entryModel.indexForEntry(entry))
                else:
                    feed.entries.remove(entry)
            self.feedModel.entriesUpdated(feed)
        # Restart timer to run again after an hour
        self.archiveTimer.start(60 * 1000)

    def showPreferences(self):
        prefs = Preferences(self)
        prefs.setWindowTitle("Slimfeed Preferences")
        prefs.updateTimeout = self.updateTimeout
        prefs.markReadTimeout = self.markReadTimeout
        prefs.systrayFont = self.systrayFont
        prefs.systrayFontColor = self.systrayFontColor
        prefs.articleDeletionEnabled = self.enableArticleDeletion
        prefs.numberOfArticlesEnabled = self.numberOfArticlesEnabled
        prefs.numberOfArticles = self.numberOfArticles
        prefs.numberOfDaysEnabled = self.numberOfDaysEnabled
        prefs.numberOfDays = self.numberOfDays
        if prefs.exec_() == QtGui.QDialog.Accepted:
            self.updateTimeout = prefs.updateTimeout
            self.markReadTimeout = prefs.markReadTimeout
            self.systrayFont = prefs.systrayFont
            self.systrayFontColor = prefs.systrayFontColor
            self.enableArticleDeletion = prefs.articleDeletionEnabled
            self.numberOfArticlesEnabled = prefs.numberOfArticlesEnabled
            self.numberOfArticles = prefs.numberOfArticles
            self.numberOfDaysEnabled = prefs.numberOfDaysEnabled
            self.numberOfDays = prefs.numberOfDays
            self.updateSystrayIcon()
            self.checkArchiveTimer()


    def sysTrayActivated(self, reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.doShow()

    def markEntryRead(self):
        if self.markReadIdx is not None and self.markReadIdx.isValid():
            self.entryModel.markRead(self.markReadIdx)
        self.updateSystrayIcon()

    def currentEntryChanged(self, idx1, idx2):
        self.markReadIdx = self.entryProxyModel.mapToSource(idx1)
        self.markReadTimer.start(self.markReadTimeout)
        entry = self.entryModel.entryFromIndex(self.markReadIdx)
        self.browser.setUrl(QUrl(entry.url))

    def markSelectedEntriesImportant(self):
        selection = self.entryList.selectionModel().selectedRows()
        if len(selection) > 0:
            for idx in selection:
                srcIdx = self.entryProxyModel.mapToSource(idx)
                self.entryModel.markImportant(srcIdx)

    def updateFeeds(self):
        if self.updateThread is None or not self.updateThread.isAlive():
            self.updateThread = UpdateThread(self)
            self.updateThread.setDaemon(True)
            self.updateThread.start()

    def updateSystrayIcon(self):
        numUnread = 0
        for feed in self.feedMgr.feeds:
            numUnread += feed.unread
        pixmap = self.windowIcon().pixmap(self.sysTray.geometry().size())
        if not pixmap.isNull():
            painter = QtGui.QPainter()
            painter.begin(pixmap)
            painter.setFont(self.systrayFont)
            painter.setPen(self.systrayFontColor)
            painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter, str(numUnread));
            painter.end()
            self.sysTrayIcon = QtGui.QIcon(pixmap)
            self.sysTray.setIcon(self.sysTrayIcon)

    @QtCore.pyqtSlot(list)
    def feedsUpdated(self, updated):
        self.updateThread = None
        self.feedModel.feedsUpdated(updated)
        self.entryModel.feedsUpdated(updated)
        self.updateSystrayIcon()
        self._startUpdateTimer()

    def _setupToolBar(self, toolbar, container, actions):
        container.setLayout(QtGui.QVBoxLayout())
        container.layout().setSpacing(0)
        container.layout().setContentsMargins(0, 0, 0, 0)
        container.layout().addWidget(toolbar)
        for action in actions:
            toolbar.addAction(action)
        toolbar.setIconSize(QtCore.QSize(16, 16))

    def setupListToolBars(self):
        self._setupToolBar(self.feedToolBar, self.feedToolBarContainer, [self.actionDeleteFeed, ])
        self._setupToolBar(self.entryToolBar, self.entryToolBarContainer, [self.actionMarkEntryAsImportant, self.actionDeleteEntry])
        self._setupToolBar(self.browserToolBar, self.browserToolBarContainer, [self.actionBack, self.actionForward, self.actionStop, self.actionReload])

    def feedSelectionChanged(self):
        selection = self.feedList.selectionModel().selectedRows()
        self.actionDeleteFeed.setEnabled((len(selection) > 0))
        if len(selection) > 0:
            self.entryModel.feed = self.feedModel.feedFromIndex(selection[0])
        else:
            self.entryModel.feed = None

    def entrySelectionChanged(self):
        selection = self.entryList.selectionModel().selectedRows()
        self.actionDeleteEntry.setEnabled((len(selection) > 0))
        self.actionMarkEntryAsImportant.setEnabled((len(selection) > 0))

    def deleteSelectedEntry(self):
        selection = self.entryList.selectionModel().selectedRows()
        if len(selection) > 0:
            srcIdx = self.entryProxyModel.mapToSource(selection[0])
            entry = self.entryModel.entryFromIndex(srcIdx)
            if QtGui.QMessageBox.question(self,
                    "Delete Feed",
                    "Do you really want to delete the article '%s'" % (entry.title),
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                    QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
                self.entryModel.removeEntry(srcIdx)


    def deleteSelectedFeed(self):
        selection = self.feedList.selectionModel().selectedRows()
        if len(selection) > 0:
            feed = self.feedModel.feedFromIndex(selection[0])
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

    def _restoreViews(self):
        settings = QtCore.QSettings("de.apaku", "Slimfeed")
        settings.beginGroup("FeedList")
        self._restoreHeaderView(settings, self.feedList)
        currentFeedId = settings.value("CurrentFeedUrl", None)
        currentFeed = None
        if currentFeedId is not None:
            for feed in self.feedMgr.feeds:
                if feed.url == currentFeedId:
                    currentFeed = feed
                    break
        if currentFeed is not None:
            # Make sure to select the complete row, to be consistent with what the user
            # can select
            topleft = self.feedModel.indexForFeed(currentFeed)
            self.feedList.selectionModel().select(topleft, QtGui.QItemSelectionModel.ClearAndSelect | QtGui.QItemSelectionModel.Rows)
            self.feedList.selectionModel().setCurrentIndex(topleft, QtGui.QItemSelectionModel.Current)
        settings.endGroup()
        settings.beginGroup("EntryList")
        self._restoreHeaderView(settings, self.entryList)
        # Ensure that the sort indicator is always shown on the entryList, even if restoring from
        # a state before this property was used
        self.entryList.horizontalHeader().setSortIndicatorShown(True)
        currentEntryId = settings.value("CurrentEntryId", None)
        currentEntry = None
        if currentEntryId is not None and currentFeed is not None:
            for entry in currentFeed.entries:
                if entry.identity == currentEntryId:
                    currentEntry = entry
                    break
        if currentEntry is not None:
            # Make sure to select the complete row, to be consistent with what the user
            # can select
            topleft = self.entryProxyModel.mapFromSource(self.entryModel.indexForEntry(currentEntry))
            self.entryList.selectionModel().select(topleft, QtGui.QItemSelectionModel.ClearAndSelect | QtGui.QItemSelectionModel.Rows)
            self.entryList.selectionModel().setCurrentIndex(topleft, QtGui.QItemSelectionModel.Current)
        settings.endGroup()

    def _readSettings(self):
        settings = QtCore.QSettings("de.apaku", "Slimfeed")
        self.restoreGeometry(settings.value("geometry", QtCore.QByteArray()))
        self.restoreState(settings.value("state", QtCore.QByteArray()))
        self.updateTimeout = _readQSettingsIntEntry(settings, "UpdateTimeout", 300)
        self.markReadTimeout = _readQSettingsIntEntry(settings, "MarkReadTimeout", 500)
        settings.beginGroup("ArticleDeletion")

        self.enableArticleDeletion = _readQSettingsBoolEntry(settings, "Enabled", False)
        self.numberOfArticlesEnabled = _readQSettingsBoolEntry(settings, "NumberOfArticlesEnabled", False)
        self.numberOfArticles = _readQSettingsIntEntry(settings, "NumberOfArticles", 100)
        self.numberOfDaysEnabled = _readQSettingsBoolEntry(settings, "NumberOfDaysEnabled", True)
        self.numberOfDays = _readQSettingsIntEntry(settings, "NumberOfDays", 60)
        settings.endGroup()

        self.systrayFontColor = settings.value("SystrayFontColor", QtGui.qApp.palette().color(QtGui.QPalette.Active, QtGui.QPalette.Text))
        # The default font for the systray overlay text should be bold
        defFont = QtGui.qApp.font()
        defFont.setBold(True)
        self.systrayFont = settings.value("SystrayFont", defFont)
        settings.beginGroup("Feeds")
        self.feedMgr.load(settings)
        settings.endGroup()

    def _writeSettings(self):
        settings = QtCore.QSettings("de.apaku", "Slimfeed")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("state", self.saveState())
        settings.setValue("UpdateTimeout", self.updateTimeout)
        settings.setValue("MarkReadTimeout", self.markReadTimeout)

        settings.beginGroup("ArticleDeletion")
        settings.setValue("Enabled", self.enableArticleDeletion)
        settings.setValue("NumberOfArticlesEnabled", self.numberOfArticlesEnabled)
        settings.setValue("NumberOfArticles", self.numberOfArticles)
        settings.setValue("NumberOfDaysEnabled", self.numberOfDaysEnabled)
        settings.setValue("NumberOfDays", self.numberOfDays)
        settings.endGroup()

        settings.setValue("SystrayFont", self.systrayFont)
        settings.setValue("SystrayFontColor", self.systrayFontColor)
        settings.beginGroup("EntryList")
        currentEntry = self.entryModel.entryFromIndex(self.entryProxyModel.mapToSource(
                       self.entryList.selectionModel().currentIndex()))
        if currentEntry is not None:
            settings.setValue("CurrentEntryId", currentEntry.identity)
        else:
            settings.setValue("CurrentEntryId", None)
        settings.setValue("Horizontal Header State",
                self.entryList.horizontalHeader().saveState())
        for col in range(0, self.entryList.horizontalHeader().count()):
            settings.beginGroup("Column %d" % col)
            settings.setValue("Width",
                    self.entryList.horizontalHeader().sectionSize(col))
            settings.endGroup()
        settings.endGroup()
        settings.beginGroup("FeedList")
        currentFeed = self.feedModel.feedFromIndex(self.feedList.selectionModel().currentIndex())
        if currentFeed is not None:
            settings.setValue("CurrentFeedUrl", currentFeed.url)
        else:
            settings.setValue("CurrentFeedUrl", None)
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

    def quit(self):
        # Really Quit from here
        self._writeSettings()
        QtGui.QApplication.quit()

    def closeEvent(self, event):
        # If we're closed by the user, lets just hide
        # but if the close comes due to session-shutdown lets really quit
        if not QtGui.qApp.isAboutToQuit():
            self.hide()
            event.ignore()
        else:
            event.accept()
            quit()

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
    QtGui.qApp = app = SlimApp(sys.argv)
    icon = QtGui.QIcon()
    icon.addFile("icons/slimfeed_16.png", QtCore.QSize(16, 16))
    icon.addFile("icons/slimfeed_22.png", QtCore.QSize(22, 22))
    icon.addFile("icons/slimfeed_32.png", QtCore.QSize(32, 32))
    icon.addFile("icons/slimfeed_32.png", QtCore.QSize(32, 32))
    icon.addFile("icons/slimfeed_64.png", QtCore.QSize(64, 64))
    icon.addFile("icons/slimfeed_128.png", QtCore.QSize(128, 128))
    app.setWindowIcon(icon)
    mainwin = MainWindow()
    mainwin.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
