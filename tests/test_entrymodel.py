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
# Disable complaints about our mock-object and the impossibility to import
# modeltest both are ignorable here
#pylint: disable=R0903,F0401,R0904

import unittest2
import sys
import os
from minimock import Mock
sys.path.append("..")
sys.path.append(".")
sys.path.append(os.path.join(os.getcwd(), "modeltest"))
sys.path.append(os.path.join(os.getcwd(), "tests", "modeltest"))

from entrymodel import EntryModel
from feed import Feed
from modeltest import ModelTest
from datetimeutils import qDateTimeFromTimeStruct
from PyQt4.QtCore import Qt, QModelIndex
from PyQt4.QtGui import QFont
from signalspy import SignalSpy

class EntryModelTest(unittest2.TestCase):
    def setUp(self):
        import time
        self.feed = Feed()
        entry = Mock("Entry")
        entry.title = "Title1"
        entry.author = "Author1"
        entry.read = False
        entry.important = False
        entry.updated = time.gmtime(time.time())
        self.feed.entries.append(entry)
        entry = Mock("Entry")
        entry.title = "Title2"
        entry.author = "Author2"
        entry.read = True
        entry.important = True
        entry.updated = time.gmtime(time.time())
        self.feed.entries.append(entry)
        self.entryModel = EntryModel(self.feed)
        self.modeltest = ModelTest(self.entryModel, self.entryModel)

    def testUpdateImportantStatus(self):
        model = self.entryModel
        spyEntriesChanged = SignalSpy(model.entriesChanged)
        spyDataChanged = SignalSpy(model.dataChanged)
        idx = model.index(0, 0, QModelIndex())
        self.assertEqual(model.data(idx, Qt.DisplayRole), "")
        model.markImportant(idx)
        self.assertEqual(spyEntriesChanged.slotTriggered, 1)
        self.assertEqual(spyEntriesChanged.arguments[0][0], self.feed)
        self.assertEqual(spyDataChanged.slotTriggered, 1)
        self.assertEqual(spyDataChanged.arguments[0][0].row(), model.index(0, 0, QModelIndex()).row())
        self.assertEqual(spyDataChanged.arguments[0][1].row(), model.index(0, 2, QModelIndex()).row())
        self.assertEqual(model.data(idx, Qt.DisplayRole), "!")
        spyEntriesChanged = SignalSpy(model.entriesChanged)
        spyDataChanged = SignalSpy(model.dataChanged)
        idx = model.index(0, 0, QModelIndex())
        model.markImportant(idx)
        self.assertEqual(spyEntriesChanged.slotTriggered, 1)
        self.assertEqual(spyEntriesChanged.arguments[0][0], self.feed)
        self.assertEqual(spyDataChanged.slotTriggered, 1)
        self.assertEqual(spyDataChanged.arguments[0][0].row(), model.index(0, 0, QModelIndex()).row())
        self.assertEqual(spyDataChanged.arguments[0][1].row(), model.index(0, 2, QModelIndex()).row())
        self.assertEqual(model.data(idx, Qt.DisplayRole), "")


    def testUpdateReadStatus(self):
        model = self.entryModel
        spyEntriesChanged = SignalSpy(model.entriesChanged)
        spyDataChanged = SignalSpy(model.dataChanged)
        idx = model.index(0, 0, QModelIndex())
        model.markRead(idx)
        self.assertEqual(spyEntriesChanged.slotTriggered, 1)
        self.assertEqual(spyEntriesChanged.arguments[0][0], self.feed)
        self.assertEqual(spyDataChanged.slotTriggered, 1)
        self.assertEqual(spyDataChanged.arguments[0][0].row(), model.index(0, 0, QModelIndex()).row())
        self.assertEqual(spyDataChanged.arguments[0][1].row(), model.index(0, 2, QModelIndex()).row())

    def testHeader(self):
        self.assertEqual(self.entryModel.headerData(0, Qt.Horizontal, Qt.DisplayRole), "")
        self.assertEqual(self.entryModel.headerData(1, Qt.Horizontal, Qt.DisplayRole), "Title")
        self.assertEqual(self.entryModel.headerData(2, Qt.Horizontal, Qt.DisplayRole), "Author")
        self.assertEqual(self.entryModel.headerData(3, Qt.Horizontal, Qt.DisplayRole), "Updated")

    def testData(self):
        self.assertEqual(self.entryModel.rowCount(), 2)
        self.assertEqual(self.entryModel.columnCount(), 4)
        self.assertEqual(self.entryModel.data(
                self.entryModel.index(0, 0, QModelIndex()), 
                    Qt.DisplayRole), "")
        self.assertEqual(self.entryModel.data(
                self.entryModel.index(0, 0, QModelIndex()),
                    Qt.FontRole).italic(), False)
        self.assertEqual(self.entryModel.data(
                self.entryModel.index(0, 1, QModelIndex()),
                    Qt.DisplayRole), "Title1")
        self.assertEqual(self.entryModel.data(
                self.entryModel.index(0, 2, QModelIndex()),
                    Qt.DisplayRole), "Author1")
        self.assertEqual(self.entryModel.data(
                self.entryModel.index(0, 3, QModelIndex()),
                    Qt.DisplayRole), qDateTimeFromTimeStruct(
                        list(self.feed.entries)[0].updated))
        self.assertEqual(self.entryModel.data(
                self.entryModel.index(0, 1, QModelIndex()),
                    Qt.FontRole).bold(), True)
        self.assertEqual(self.entryModel.data(
                self.entryModel.index(1, 1, QModelIndex()),
                    Qt.DisplayRole), "Title2")
        self.assertEqual(self.entryModel.data(
                self.entryModel.index(1, 0, QModelIndex()), 
                    Qt.DisplayRole), "!")
        self.assertEqual(self.entryModel.data(
                self.entryModel.index(1, 0, QModelIndex()),
                    Qt.FontRole).italic(), True)
        self.assertEqual(self.entryModel.data(
                self.entryModel.index(1, 2, QModelIndex()),
                    Qt.DisplayRole), "Author2")
        self.assertEqual(self.entryModel.data(
                self.entryModel.index(1, 3, QModelIndex()),
                    Qt.DisplayRole), qDateTimeFromTimeStruct(
                        list(self.feed.entries)[1].updated))
        self.assertEqual(self.entryModel.data(
                self.entryModel.index(1, 1, QModelIndex()),
                    Qt.FontRole).bold(), False)

    def testIndexFromEntry(self):
        self.assertEqual(self.entryModel.indexForFeed(self.feed.entries[0]), self.entryModel.index(0, 0, QModelIndex()))
        self.assertEqual(self.entryModel.indexForFeed(self.feed.entries[1]), self.entryModel.index(1, 0, QModelIndex()))

if __name__ == "__main__":
    unittest2.main()
