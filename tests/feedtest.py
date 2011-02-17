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

class StoreMock:
    pass

class EntryMock:
    def __init__(self, data=None):
        if data is not None:
            self._data = data

    def save(self, store):
        self._stored = True

    def load(self, store):
        self._loaded = True

class FeedTest(unittest.TestCase):
    def setUp(self):
        self.feed = Feed()

    def testSave(self):
        e = EntryMock()
        self.feed.entries.add(e)
        self.feed.save(StoreMock())
        self.assertEqual(e._stored, True)

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
        self.feed.entries.add(EntryMock())
        self.assertEqual(len(self.feed.entries), 1)

    def testRemove(self):
        self.assertEqual(len(self.feed.entries), 0)
        f = EntryMock()
        self.feed.entries.add(f)
        self.assertEqual(len(self.feed.entries), 1)
        self.feed.entries.remove(f) 
        self.assertEqual(len(self.feed.entries), 0)

    def testAddDuplicate(self):
        self.assertEqual(len(self.feed.entries), 0)
        f = EntryMock()
        self.feed.entries.add(f)
        self.assertEqual(len(self.feed.entries), 1)
        self.feed.entries.add(f)
        self.assertEqual(len(self.feed.entries), 1)


if __name__ == "__main__":
    unittest.main()

