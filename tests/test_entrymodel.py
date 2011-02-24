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

import unittest
import sys
import os
sys.path.append("..")
sys.path.append(".")
sys.path.append(os.path.join(os.getcwd(), "modeltest"))
sys.path.append(os.path.join(os.getcwd(), "tests", "modeltest"))

from entrymodel import EntryModel
from feed import Feed
from modeltest import ModelTest
from PyQt4.QtCore import Qt, QModelIndex

class EntryMock(object):
    def __init__(self):
        import time
        self.entries = []
        self.title = "Title"
        self.author = "Author"
        self.url = "Url"
        self.updated = time.time()
        self.unread = 0

class EntryModelTest(unittest.TestCase):
    def setUp(self):
        import time
        self.feed = Feed()
        f = EntryMock()
        f.title = "Title1"
        f.author = "Author1"
        f.updated = time.time()
        self.feed.entries.add(f)
        f = EntryMock()
        f.title = "Title2"
        f.author = "Author2"
        f.updated = time.time()
        self.feed.entries.add(f)
        self.entryModel = EntryModel(self.feed)
        self.modeltest = ModelTest(self.entryModel,self.entryModel)

    def testData(self):
        self.assertEqual(self.entryModel.rowCount(), 2)
        self.assertEqual(self.entryModel.data(self.entryModel.index(0, 0, QModelIndex()), Qt.DisplayRole), "Title2")
        self.assertEqual(self.entryModel.data(self.entryModel.index(0, 1, QModelIndex()), Qt.DisplayRole), "Author2")
        self.assertEqual(self.entryModel.data(self.entryModel.index(0, 2, QModelIndex()), Qt.DisplayRole), list(self.feed.entries)[0].updated)
        self.assertEqual(self.entryModel.data(self.entryModel.index(1, 0, QModelIndex()), Qt.DisplayRole), "Title1")
        self.assertEqual(self.entryModel.data(self.entryModel.index(1, 1, QModelIndex()), Qt.DisplayRole), "Author1")
        self.assertEqual(self.entryModel.data(self.entryModel.index(1, 2, QModelIndex()), Qt.DisplayRole), list(self.feed.entries)[1].updated)

if __name__ == "__main__":
    unittest.main()

