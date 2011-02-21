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

from feedmanager import FeedManager
from feed import Feed

from storemock import StoreMock

class FeedManagerTest(unittest.TestCase):
    def setUp(self):
        self.feedManager = FeedManager()

    def testLoad(self):
        import time
        from base64 import b64encode
        s = StoreMock()
        t = time.time()
        s.beginGroup("Feed_%s" %b64encode("T1"))
        s.setValue("Title", "T1")
        s.setValue("Updated", t)
        s.setValue("Author", "Author1")
        s.setValue("Url", "Url1")
        s.endGroup()
        s.beginGroup("Feed_%s" %b64encode("T2"))
        s.setValue("Title", "T2")
        s.setValue("Updated", t)
        s.setValue("Author", "Author2")
        s.setValue("Url", "Url2")
        s.endGroup()
        self.feedManager.load(s)
        self.assertEqual(len(self.feedManager.feeds), 2)

    def testSave(self):
        s = StoreMock()
        f = Feed()
        f.title = "T1"
        self.feedManager.feeds.add(f)
        f = Feed()
        f.title = "T2"
        self.feedManager.feeds.add(f)
        self.feedManager.save(s)
        self.assertEqual(len(s.childGroups()), 2)

    def testAdd(self):
        self.assertEqual(len(self.feedManager.feeds), 0)
        self.feedManager.feeds.add(Feed())
        self.assertEqual(len(self.feedManager.feeds), 1)

    def testRemove(self):
        self.assertEqual(len(self.feedManager.feeds), 0)
        f = Feed()
        self.feedManager.feeds.add(f)
        self.assertEqual(len(self.feedManager.feeds), 1)
        self.feedManager.feeds.remove(f) 
        self.assertEqual(len(self.feedManager.feeds), 0)

    def testAddDuplicate(self):
        self.assertEqual(len(self.feedManager.feeds), 0)
        f = Feed()
        self.feedManager.feeds.add(f)
        self.assertEqual(len(self.feedManager.feeds), 1)
        self.feedManager.feeds.add(f)
        self.assertEqual(len(self.feedManager.feeds), 1)

if __name__ == "__main__":
    unittest.main()

