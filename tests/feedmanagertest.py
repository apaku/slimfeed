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

class FeedManagerTest(unittest.TestCase):
    def setUp(self):
        self.feedManager = FeedManager()

    def testAdd(self):
        self.assertEqual(len(self.feedManager.feeds()), 0)
        self.feedManager.addFeed(Feed())
        self.assertEqual(len(self.feedManager.feeds()), 1)

    def testRemove(self):
        self.assertEqual(len(self.feedManager.feeds()), 0)
        f = Feed()
        self.feedManager.addFeed(f)
        self.assertEqual(len(self.feedManager.feeds()), 1)
        self.feedManager.removeFeed(f) 
        self.assertEqual(len(self.feedManager.feeds()), 0)

    def testAddDuplicate(self):
        self.assertEqual(len(self.feedManager.feeds()), 0)
        f = Feed()
        self.feedManager.addFeed(f)
        self.assertEqual(len(self.feedManager.feeds()), 1)
        self.feedManager.addFeed(f)
        self.assertEqual(len(self.feedManager.feeds()), 1)

if __name__ == "__main__":
    unittest.main()

