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

from entry import Entry

class StoreMock:
    pass

class EntryTest(unittest.TestCase):
    def setUp(self):
        import time
        self.entry = Entry()

    def testTitle(self):
        self.assertEqual(len(self.entry.title), 0)
        self.entry.title = "test"
        self.assertEqual(self.entry.title, "test")
        del self.entry.title
        self.assertFalse(hasattr(self.entry, "title"))

    def testUrl(self):
        self.assertEqual(len(self.entry.url), 0)
        self.entry.url = "test"
        self.assertEqual(self.entry.url, "test")
        del self.entry.url
        self.assertFalse(hasattr(self.entry, "url"))

    def testAuthor(self):
        self.assertEqual(len(self.entry.author), 0)
        self.entry.author = "test"
        self.assertEqual(self.entry.author, "test")
        del self.entry.author
        self.assertFalse(hasattr(self.entry, "author"))

    def testContent(self):
        self.assertEqual(len(self.entry.content), 0)
        self.entry.content = "test"
        self.assertEqual(self.entry.content, "test")
        del self.entry.content
        self.assertFalse(hasattr(self.entry, "content"))

    def testIdentity(self):
        self.assertEqual(len(self.entry.identity), 0)
        self.entry.identity = "test"
        self.assertEqual(self.entry.identity, "test")
        del self.entry.identity
        self.assertFalse(hasattr(self.entry, "identity"))

    def testUpdated(self):
        import time
        self.assertEqual(self.entry.updated, None)
        t = time.time()
        self.entry.updated = t
        self.assertEqual(self.entry.updated, t)
        del self.entry.updated
        self.assertFalse(hasattr(self.entry, "updated"))

    def testSave(self):
        self.entry.save(StoreMock())

if __name__ == "__main__":
    unittest.main()

