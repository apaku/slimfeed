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
    def save(self, store):
        self._stored = True

    def load(self, store):
        self._loaded = True

class FeedTest(unittest.TestCase):
    def setUp(self):
        self.feed = Feed()

    def testSave(self):
        e = EntryMock()
        self.feed.addEntry(e)
        self.feed.save(StoreMock())
        self.assertEqual(e._stored, True)

    def testAdd(self):
        self.assertEqual(len(self.feed.entries()), 0)
        self.feed.addEntry(EntryMock())
        self.assertEqual(len(self.feed.entries()), 1)

    def testRemove(self):
        self.assertEqual(len(self.feed.entries()), 0)
        f = EntryMock()
        self.feed.addEntry(f)
        self.assertEqual(len(self.feed.entries()), 1)
        self.feed.removeEntry(f) 
        self.assertEqual(len(self.feed.entries()), 0)

    def testAddDuplicate(self):
        self.assertEqual(len(self.feed.entries()), 0)
        f = EntryMock()
        self.feed.addEntry(f)
        self.assertEqual(len(self.feed.entries()), 1)
        self.feed.addEntry(f)
        self.assertEqual(len(self.feed.entries()), 1)


if __name__ == "__main__":
    unittest.main()

