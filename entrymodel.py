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
from entry import Entry
from PyQt4.QtCore import QAbstractTableModel, Qt, QVariant, QModelIndex

class EntryModel(QAbstractTableModel):
    def __init__(self, feed=None, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._feed = feed

    def setfeed(self, feed):
        self._feed = feed
    def getfeed(self):
        return self._feed
    feed = property(getfeed, setfeed, None, "Feed that the model displays entries for")

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid() or self._feed is None:
            return 0
        return len(self._feed.entries)

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return 3

    def data(self, idx, role=Qt.DisplayRole):
        if not idx.isValid() or \
                idx.row() < 0 or \
                idx.row() >= self.rowCount() or \
                idx.column() < 0 or \
                idx.column() >= self.columnCount() or \
                self._feed is None:
            return None
        if role != Qt.DisplayRole:
            return None

        f = list(self._feed.entries)[idx.row()]
        if idx.column() == 0:
            return f.title
        elif idx.column() == 1:
            return f.author
        elif idx.column() == 2:
            return f.updated
        return None

    def headerData(self, col, orient, role=Qt.DisplayRole):
        if col < 0 or col >= self.columnCount() or role != Qt.DisplayRole or orient != Qt.Horizontal:
            return None
        if col == 0:
            return "Title"
        elif col == 1:
            return "Author"
        elif col == 2:
            return "Updated"

if __name__ == "__main__":
    import sys
    print "Cannot run this module"
    sys.exit(1)

