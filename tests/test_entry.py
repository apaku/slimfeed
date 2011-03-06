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
#pylint: disable=R0904

import unittest2
import sys
sys.path.append("..")
sys.path.append(".")

from entry import Entry
from storemock import StoreMock


class EntryTest(unittest2.TestCase):
    def setUp(self):
        import time
        self.entry = Entry()
        self.saveentry = Entry()
        self.saveentry.title = "TestTitle"
        self.saveentry.author = "TestAuthor"
        self.saveentry.url = "TestUrl"
        self.saveentry.content = "TestContent"
        self.saveentry.identity = "TestId"
        self.saveentry.updated = time.time()
        self.saveentry.read = True

    def testTitle(self):
        self.assertIsNone(self.entry.title)
        self.entry.title = "test"
        self.assertEqual(self.entry.title, "test")

    def testUrl(self):
        self.assertIsNone(self.entry.url)
        self.entry.url = "test"
        self.assertEqual(self.entry.url, "test")

    def testAuthor(self):
        self.assertIsNone(self.entry.author)
        self.entry.author = "test"
        self.assertEqual(self.entry.author, "test")

    def testContent(self):
        self.assertIsNone(self.entry.content)
        self.entry.content = "test"
        self.assertEqual(self.entry.content, "test")

    def testIdentity(self):
        self.assertIsNone(self.entry.identity)
        self.entry.identity = "test"
        self.assertEqual(self.entry.identity, "test")

    def testUpdated(self):
        import time
        self.assertEqual(self.entry.updated, None)
        update = time.time()
        self.entry.updated = update
        self.assertEqual(self.entry.updated, update)

    def testRead(self):
        self.assertEqual(self.entry.read, False)
        self.entry.read = True
        self.assertEqual(self.entry.read, True)

    def testLoad(self):
        import time
        store = StoreMock()
        store.setValue("Title", "MyTitle")
        store.setValue("Content", "MyContent")
        updated = time.time()
        store.setValue("Updated", updated)
        store.setValue("Url", "MyUrl")
        store.setValue("Id", "MyId")
        store.setValue("Author", "MyAuthor")
        store.setValue("Read", False)
        self.saveentry.load(store)
        self.assertEqual(self.saveentry.title, "MyTitle")
        self.assertEqual(self.saveentry.author, "MyAuthor")
        self.assertEqual(self.saveentry.url, "MyUrl")
        self.assertEqual(self.saveentry.identity, "MyId")
        self.assertEqual(self.saveentry.updated, updated)
        self.assertEqual(self.saveentry.content, "MyContent")
        self.assertEqual(self.saveentry.read, False)

    def testSave(self):
        store = StoreMock()
        self.saveentry.save(store)
        self.assertEqual(store.value("Title"), self.saveentry.title)
        self.assertEqual(store.value("Url"), self.saveentry.url)
        self.assertEqual(store.value("Author"), self.saveentry.author)
        self.assertEqual(store.value("Content"), self.saveentry.content)
        self.assertEqual(store.value("Updated"), self.saveentry.updated)
        self.assertEqual(store.value("Id"), self.saveentry.identity)
        self.assertEqual(store.value("Read"), self.saveentry.read)

    def testEqual(self):
        entry = Entry()
        entry.title = self.entry.title
        entry.updated = self.entry.updated
        entry.identity = self.entry.identity
        entry.content = self.entry.content
        entry.read = self.entry.read
        entry.url = self.entry.url
        entry.author = self.entry.author
        self.assertEqual(self.entry, entry)

if __name__ == "__main__":
    unittest2.main()
