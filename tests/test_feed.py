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

from feed import Feed
from entry import Entry
from storemock import StoreMock


class FeedTest(unittest2.TestCase):
    def setUp(self):
        import time
        self.feed = Feed()
        self.savefeed = Feed()
        self.savefeed.title = "MyTitle"
        self.savefeed.author = "MyAuthor"
        self.savefeed.url = "MyUrl"
        self.savefeed.updated = time.time()

    def testLoad(self):
        import time
        from base64 import b64encode
        updated = time.time()
        store = StoreMock()
        store.setValue("Title", "TestTitle")
        store.setValue("Url", "TestUrl")
        store.setValue("Author", "TestAuthor")
        store.setValue("Updated", updated)
        store.beginGroup("Entry_%s" % b64encode("Id1"))
        store.setValue("Title", "T1")
        store.setValue("Updated", updated)
        store.setValue("Author", "Author1")
        store.setValue("Url", "Url1")
        store.setValue("Id", "Id1")
        store.setValue("Content", "Content1")
        store.setValue("Read", True)
        store.endGroup()
        store.beginGroup("Entry_%s" % b64encode("Id2"))
        store.setValue("Title", "T2")
        store.setValue("Updated", updated)
        store.setValue("Author", "Author2")
        store.setValue("Url", "Url2")
        store.setValue("Id", "Id2")
        store.setValue("Content", "Content2")
        store.endGroup()
        self.savefeed.load(store)
        self.assertEqual(self.savefeed.title, "TestTitle")
        self.assertEqual(self.savefeed.updated, updated)
        self.assertEqual(self.savefeed.url, "TestUrl")
        self.assertEqual(self.savefeed.author, "TestAuthor")
        self.assertEqual(self.savefeed.unread, 1)
        self.assertEqual(len(self.savefeed.entries), 2)

    def testSave(self):
        entry = Entry()
        store = StoreMock()
        self.savefeed.entries.append(entry)
        self.savefeed.save(store)
        self.assertEqual(len(store.childGroups()), 1)
        self.assertEqual(self.savefeed.title, store.value("Title"))
        self.assertEqual(self.savefeed.author, store.value("Author"))
        self.assertEqual(self.savefeed.url, store.value("Url"))
        self.assertEqual(self.savefeed.updated, store.value("Updated"))

    def testTitle(self):
        self.assertIsNone(self.feed.title)
        self.feed.title = "test"
        self.assertEqual(self.feed.title, "test")

    def testAuthor(self):
        self.assertIsNone(self.feed.author)
        self.feed.author = "test"
        self.assertEqual(self.feed.author, "test")

    def testUrl(self):
        self.assertIsNone(self.feed.url)
        self.feed.url = "test"
        self.assertEqual(self.feed.url, "test")

    def testUpdated(self):
        import time
        self.assertEqual(self.feed.updated, None)
        updated = time.time()
        self.feed.updated = updated
        self.assertEqual(self.feed.updated, updated)

    def testAdd(self):
        self.assertEqual(len(self.feed.entries), 0)
        self.feed.entries.append(Entry())
        self.assertEqual(len(self.feed.entries), 1)

    def testRemove(self):
        self.assertEqual(len(self.feed.entries), 0)
        feed = Entry()
        self.feed.entries.append(feed)
        self.assertEqual(len(self.feed.entries), 1)
        self.feed.entries.remove(feed)
        self.assertEqual(len(self.feed.entries), 0)

if __name__ == "__main__":
    unittest2.main()
