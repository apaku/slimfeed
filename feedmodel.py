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

from feed import Feed
from PyQt4.QtCore import QAbstractTableModel, Qt, QVariant, QModelIndex

class FeedModel(QAbstractTableModel):
    def __init__(self, feedMgr, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._feedmgr = feedMgr

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
            return QVariant()
        if role != Qt.DisplayRole:
            return QVariant()

        f = list(self._feedmgr.feeds)[idx.row()]
        if idx.column() == 0:
            return f.title
        elif idx.column() == 1:
            return f.unread
        elif idx.column() == 2:
            return len(f.entries)
        return QVariant()

    def headerData(self, col, orient, role=Qt.DisplayRole):
        if col < 0 or col >= self.columnCount() or role != Qt.DisplayRole or orient != Qt.Horizontal:
            return QVariant()
        if col == 0:
            return "Title"
        elif col == 1:
            return "New"
        elif col == 2:
            return "All"

if __name__ == "__main__":
    import sys
    print "Cannot run this module"
    sys.exit(1)

