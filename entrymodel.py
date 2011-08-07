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

from PyQt4.QtCore import QAbstractTableModel, Qt, QModelIndex, pyqtSignal
from PyQt4.QtGui import QFont
from datetimeutils import qDateTimeFromTimeStruct
from feed import Feed


# Disable 'method can be used as function' as it triggers on columnCount which
# indeed does not need the self, but we can't change that due to inheritance
# from Qt
#pylint: disable=R0201
class EntryModel(QAbstractTableModel):

    entriesChanged = pyqtSignal(Feed)

    def __init__(self, feed=None, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._feed = feed

    def _setfeed(self, feed):
        self._feed = feed
        self.reset()

    def _getfeed(self):
        return self._feed

    feed = property(_getfeed, _setfeed, None, \
            "Feed that the model displays entries for")

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid() or self._feed is None:
            return 0
        return len(self._feed.entries)

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return 4

    def data(self, idx, role=Qt.DisplayRole):
        if not idx.isValid() or \
                idx.row() < 0 or \
                idx.row() >= self.rowCount() or \
                idx.column() < 0 or \
                idx.column() >= self.columnCount() or \
                self._feed is None:
            return None
        if role != Qt.DisplayRole and role != Qt.FontRole:
            return None

        entry = list(self._feed.entries)[idx.row()]
        if role == Qt.DisplayRole:
            if idx.column() == 0:
                if entry.important:
                    return "!"
                return ""
            elif idx.column() == 1:
                return entry.title
            elif idx.column() == 2:
                return entry.author
            elif idx.column() == 3:
                return qDateTimeFromTimeStruct(entry.updated)
        elif role == Qt.FontRole:
            fnt = QFont()
            if not entry.read:
                fnt.setBold(True)
            if entry.important:
                fnt.setItalic(True)
            return fnt
        return None

    def headerData(self, col, orient, role=Qt.DisplayRole):
        if col < 0 or col >= self.columnCount() or \
                role != Qt.DisplayRole or \
                orient != Qt.Horizontal:
            return None
        if col == 0:
            return ""
        elif col == 1:
            return "Title"
        elif col == 2:
            return "Author"
        elif col == 3:
            return "Updated"

    def markRead(self, idx):
        if idx.isValid() and idx.row() >= 0 and idx.row() < self.rowCount(idx.parent()):
            e = self._feed.entries[idx.row()]
            if e.read == False:
                e.read = True
                self.dataChanged.emit(self.index(idx.row(), 0, idx.parent()), 
                                      self.index(idx.row(), self.columnCount(idx.parent()) - 1, idx.parent()))
                self.entriesChanged.emit(self._feed)
    def markImportant(self, idx):
        if idx.isValid() and idx.row() >= 0 and idx.row() < self.rowCount(idx.parent()):
            e = self._feed.entries[idx.row()]
            e.important = not e.important
            self.dataChanged.emit(self.index(idx.row(), 0, idx.parent()), 
                                  self.index(idx.row(), self.columnCount(idx.parent()) - 1, idx.parent()))
            self.entriesChanged.emit(self._feed)

    def feedsUpdated(self, updated):
        for info in updated:
            if self._feed is not None and info["title"] == self._feed.title and len(info["entries"]) > 0:
                self.beginInsertRows(QModelIndex(), len(self._feed.entries)-len(info["entries"]), len(self._feed.entries)-1)
                self.endInsertRows()

    def entryFromIndex(self, idx):
        if not idx.isValid() or idx.row() < 0 or idx.row() >= self.rowCount(idx.parent()):
            return None

        return self._feed.entries[idx.row()]

    def removeEntry(self, idx):
        if not idx.isValid() or idx.row() < 0 or idx.row() >= self.rowCount(idx.parent()):
            return
        
        self.beginRemoveRows(idx.parent(), idx.row(), idx.row())
        del self._feed.entries[idx.row()]
        self.endRemoveRows()
        self.entriesChanged.emit(self._feed)

    def indexForFeed(self, entry):
        if self._feed is None:
            return None
        for i in range(0, len(self._feed.entries)):
            if self._feed.entries[i] == entry:
                return self.index(i, 0, QModelIndex())
        return None

if __name__ == "__main__":
    import sys
    print "Cannot run this module"
    sys.exit(1)
