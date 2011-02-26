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

import unittest2
import sys
sys.path.append("..")
sys.path.append(".")

from feedmanager import FeedManager
from feed import Feed

from storemock import StoreMock


class TestFeedManager(unittest2.TestCase):
    def setUp(self):
        self.feedManager = FeedManager()

    def testLoad(self):
        import time
        from base64 import b64encode
        updated = time.time()
        store = StoreMock()
        store.beginGroup("Feed_%s" % b64encode("T1"))
        store.setValue("Title", "T1")
        store.setValue("Updated", updated)
        store.setValue("Author", "Author1")
        store.setValue("Url", "Url1")
        store.endGroup()
        store.beginGroup("Feed_%s" % b64encode("T2"))
        store.setValue("Title", "T2")
        store.setValue("Updated", updated)
        store.setValue("Author", "Author2")
        store.setValue("Url", "Url2")
        store.endGroup()
        self.feedManager.load(store)
        self.assertEqual(len(self.feedManager.feeds), 2)

    def testSave(self):
        store = StoreMock()
        feed = Feed()
        feed.title = "T1"
        self.feedManager.feeds.append(feed)
        feed = Feed()
        feed.title = "T2"
        self.feedManager.feeds.append(feed)
        feed = Feed()
        self.feedManager.feeds.append(feed)
        self.feedManager.save(store)
        self.assertEqual(len(store.childGroups()), 3)

    def testAdd(self):
        self.assertEqual(len(self.feedManager.feeds), 0)
        self.feedManager.feeds.append(Feed())
        self.assertEqual(len(self.feedManager.feeds), 1)

    def testRemove(self):
        self.assertEqual(len(self.feedManager.feeds), 0)
        feed = Feed()
        self.feedManager.feeds.append(feed)
        self.assertEqual(len(self.feedManager.feeds), 1)
        self.feedManager.feeds.remove(feed)
        self.assertEqual(len(self.feedManager.feeds), 0)


if __name__ == "__main__":
    unittest2.main()
