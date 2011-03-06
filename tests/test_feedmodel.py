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

from feedmodel import FeedModel
from feedmanager import FeedManager
from modeltest import ModelTest
from PyQt4.QtCore import Qt, QModelIndex
import time


class FeedModelTest(unittest2.TestCase):
    def setUp(self):
        self.feedMgr = FeedManager()
        feed = Mock("Feed")
        feed.title = "Title1"
        feed.author = "Author1"
        feed.url = "Url1"
        feed.updated = time.gmtime(time.time())
        feed.unread = 1
        feed.entries = [1, 2, 3]
        self.feedMgr.feeds.append(feed)
        feed = Mock("Feed")
        feed.title = "Title2"
        feed.author = "Author2"
        feed.url = "Url2"
        feed.updated = time.gmtime(time.time())
        feed.unread = 2
        feed.entries = [1, 2]
        self.feedMgr.feeds.append(feed)
        self.feedModel = FeedModel(self.feedMgr)
        self.modeltest = ModelTest(self.feedModel, self.feedModel)

    def testData(self):
        model = self.feedModel
        self.assertEqual(model.rowCount(), 2)
        self.assertEqual(model.data(model.index(0, 0, QModelIndex()), \
                Qt.DisplayRole), "Title1")
        self.assertEqual(model.data(model.index(0, 1, QModelIndex()), \
                Qt.DisplayRole), 1)
        self.assertEqual(model.data(model.index(0, 2, QModelIndex()), \
                Qt.DisplayRole), 3)
        self.assertEqual(model.data(model.index(1, 0, QModelIndex()), \
                Qt.DisplayRole), "Title2")
        self.assertEqual(model.data(model.index(1, 1, QModelIndex()), \
                Qt.DisplayRole), 2)
        self.assertEqual(model.data(model.index(1, 2, QModelIndex()), \
                Qt.DisplayRole), 2)

    def testGetFeed(self):
        model = self.feedModel
        feed = model.getFeed(model.index(0, 0, QModelIndex()))
        self.assertEqual(self.feedMgr.feeds[0], feed)
        feed = model.getFeed(model.index(1, 0, QModelIndex()))
        self.assertEqual(self.feedMgr.feeds[1], feed)

    def testDeleteFeed(self):
        model = self.feedModel
        model.deleteFeed(self.feedMgr.feeds[0])
        self.assertEqual(model.rowCount(), 1)

    def testAddFeed(self):
        model = self.feedModel
        feed = Mock("Feed")
        feed.title = "Title3"
        feed.author = "Author3"
        feed.updated = time.gmtime(time.time())
        feed.unread = 2
        feed.entries = [1, 4]
        self.assertEqual(model.rowCount(), 2)
        model.addFeed(feed)
        self.assertEqual(model.rowCount(), 3)

if __name__ == "__main__":
    unittest2.main()
