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

from PyQt4.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt4.QtGui import QFont


# Disable 'method can be used as function' as it triggers on columnCount which
# indeed does not need the self, but we can't change that due to inheritance
# from Qt
#pylint: disable=R0201
class FeedModel(QAbstractTableModel):
    def __init__(self, feedmgr, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._feedmgr = feedmgr

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._feedmgr.feeds)

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return 3

    def data(self, idx, role=Qt.DisplayRole):
        if not idx.isValid() or \
                idx.row() < 0 or \
                idx.row() >= self.rowCount() or \
                idx.column() < 0 or \
                idx.column() >= self.columnCount():
            return None
        if role != Qt.DisplayRole and role != Qt.FontRole:
            return None

        feed = list(self._feedmgr.feeds)[idx.row()]
        if role == Qt.DisplayRole:
            if idx.column() == 0:
                return feed.title
            elif idx.column() == 1:
                return feed.unread
            elif idx.column() == 2:
                return len(feed.entries)
        elif role == Qt.FontRole:
            fnt = QFont()
            if feed.unread > 0:
                fnt.setBold(True)
            return fnt
        return None

    def headerData(self, col, orient, role=Qt.DisplayRole):
        if col < 0 or col >= self.columnCount() \
                or role != Qt.DisplayRole \
                or orient != Qt.Horizontal:
            return None
        if col == 0:
            return "Title"
        elif col == 1:
            return "New"
        elif col == 2:
            return "All"

    def getFeed(self, idx):
        if idx.row() < 0 \
            or idx.row() >= self.rowCount(idx.parent()) \
            or idx.parent().isValid():
            return None
        return self._feedmgr.feeds[idx.row()]

    def deleteFeed(self, feed):
        assert (feed in self._feedmgr.feeds)
        idx = self._feedmgr.feeds.index(feed)
        self.beginRemoveRows(QModelIndex(), idx, idx)
        self._feedmgr.feeds.remove(feed)
        self.endRemoveRows()

    def addFeed(self, feed):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._feedmgr.feeds.append(feed)
        self.endInsertRows()

    def feedsUpdated(self):
        self.dataChanged.emit(self.index(0, 0, QModelIndex()), self.index(self.columnCount()-1, self.rowCount()-1, QModelIndex()))

    def entriesUpdated(self, feed):
        if feed in self._feedmgr.feeds:
            idx1 = self.index(self._feedmgr.feeds.index(feed), 0, QModelIndex())
            idx2 = self.index(idx1.row(), 2, QModelIndex())
            self.dataChanged.emit(idx1, idx2)

if __name__ == "__main__":
    import sys
    print "Cannot run this module"
    sys.exit(1)
