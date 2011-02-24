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
sys.path.append("..")
sys.path.append(".")

from feed import Feed
from entry import Entry
from storemock import StoreMock

class FeedTest(unittest.TestCase):
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
        t = time.time()
        s = StoreMock()
        s.setValue("Title", "TestTitle")
        s.setValue("Url", "TestUrl")
        s.setValue("Author", "TestAuthor")
        s.setValue("Updated", t)
        s.beginGroup("Entry_%s" %b64encode("Id1"))
        s.setValue("Title", "T1")
        s.setValue("Updated", t)
        s.setValue("Author", "Author1")
        s.setValue("Url", "Url1")
        s.setValue("Id", "Id1")
        s.setValue("Content", "Content1")
        s.setValue("Read", True)
        s.endGroup()
        s.beginGroup("Entry_%s" %b64encode("Id2"))
        s.setValue("Title", "T2")
        s.setValue("Updated", t)
        s.setValue("Author", "Author2")
        s.setValue("Url", "Url2")
        s.setValue("Id", "Id2")
        s.setValue("Content", "Content2")
        s.endGroup()
        self.savefeed.load(s)
        self.assertEqual(self.savefeed.title, "TestTitle")
        self.assertEqual(self.savefeed.updated, t)
        self.assertEqual(self.savefeed.url, "TestUrl")
        self.assertEqual(self.savefeed.author, "TestAuthor")
        self.assertEqual(self.savefeed.unread, 1)
        self.assertEqual(len(self.savefeed.entries), 2)

    def testSave(self):
        e = Entry()
        s = StoreMock()
        self.savefeed.entries.add(e)
        self.savefeed.save(s)
        self.assertEqual(len(s.childGroups()), 1)
        self.assertEqual(self.savefeed.title, s.value("Title"))
        self.assertEqual(self.savefeed.author, s.value("Author"))
        self.assertEqual(self.savefeed.url, s.value("Url"))
        self.assertEqual(self.savefeed.updated, s.value("Updated"))

    def testTitle(self):
        self.assertEqual(len(self.feed.title), 0)
        self.feed.title="test"
        self.assertEqual(len(self.feed.title), len("test"))
        self.assertEqual(self.feed.title, "test")
        del self.feed.title
        self.assertFalse(hasattr(self.feed, "title"))

    def testAuthor(self):
        self.assertEqual(len(self.feed.author), 0)
        self.feed.author="test"
        self.assertEqual(len(self.feed.author), len("test"))
        self.assertEqual(self.feed.author, "test")
        del self.feed.author
        self.assertFalse(hasattr(self.feed, "author"))

    def testUrl(self):
        self.assertEqual(len(self.feed.url), 0)
        self.feed.url="test"
        self.assertEqual(len(self.feed.url), len("test"))
        self.assertEqual(self.feed.url, "test")
        del self.feed.url
        self.assertFalse(hasattr(self.feed, "url"))

    def testUpdated(self):
        import time
        self.assertEqual(self.feed.updated, None)
        t = time.time()
        self.feed.updated=t
        self.assertEqual(self.feed.updated, t)
        del self.feed.updated
        self.assertFalse(hasattr(self.feed, "updated"))

    def testAdd(self):
        self.assertEqual(len(self.feed.entries), 0)
        self.feed.entries.add(Entry())
        self.assertEqual(len(self.feed.entries), 1)

    def testRemove(self):
        self.assertEqual(len(self.feed.entries), 0)
        f = Entry()
        self.feed.entries.add(f)
        self.assertEqual(len(self.feed.entries), 1)
        self.feed.entries.remove(f) 
        self.assertEqual(len(self.feed.entries), 0)

    def testAddDuplicate(self):
        self.assertEqual(len(self.feed.entries), 0)
        f = Entry()
        self.feed.entries.add(f)
        self.assertEqual(len(self.feed.entries), 1)
        self.feed.entries.add(f)
        self.assertEqual(len(self.feed.entries), 1)


if __name__ == "__main__":
    unittest.main()

