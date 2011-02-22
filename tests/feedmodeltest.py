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

from feedmodel import FeedModel
from feedmanager import FeedManager
from modeltest import ModelTest
from PyQt4.QtCore import Qt, QModelIndex

class FeedMock(object):
    def __init__(self):
        import time
        self.entries = []
        self.title = "Title"
        self.author = "Author"
        self.url = "Url"
        self.updated = time.time()
        self.unread = 0

class FeedModelTest(unittest.TestCase):
    def setUp(self):
        import time
        self.feedMgr = FeedManager()
        f = FeedMock()
        f.title = "Title1"
        f.author = "Author1"
        f.url = "Url1"
        f.updated = time.time()
        f.unread = 1
        f.entries = [1,2,3]
        self.feedMgr.feeds.add(f)
        f = FeedMock()
        f.title = "Title2"
        f.author = "Author2"
        f.url = "Url2"
        f.updated = time.time()
        f.unread = 2
        f.entries = [1,2]
        self.feedMgr.feeds.add(f)
        self.feedModel = FeedModel(self.feedMgr)
        self.modeltest = ModelTest(self.feedModel,self.feedModel)

    def testData(self):
        self.assertEqual(self.feedModel.rowCount(), 2)
        self.assertEqual(self.feedModel.data(self.feedModel.index(0, 0, QModelIndex()), Qt.DisplayRole), "Title2")
        self.assertEqual(self.feedModel.data(self.feedModel.index(0, 1, QModelIndex()), Qt.DisplayRole), 2)
        self.assertEqual(self.feedModel.data(self.feedModel.index(0, 2, QModelIndex()), Qt.DisplayRole), 2)
        self.assertEqual(self.feedModel.data(self.feedModel.index(1, 0, QModelIndex()), Qt.DisplayRole), "Title1")
        self.assertEqual(self.feedModel.data(self.feedModel.index(1, 1, QModelIndex()), Qt.DisplayRole), 1)
        self.assertEqual(self.feedModel.data(self.feedModel.index(1, 2, QModelIndex()), Qt.DisplayRole), 3)

if __name__ == "__main__":
    unittest.main()

