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
import time
sys.path.append("..")
sys.path.append(".")

from feedparserfactory import createFeedFromData, createEntryFromData


class FeedParserFactoryTest(unittest2.TestCase):
    def setUp(self):
        updated = time.time()
        self.rssfeeddata = {"feed": {"title": "rsstitle",
                            "author": "myauthor",
                            "updated_parsed": updated},
                            "href": "feedurl",
                            "entries": [{"title": "entrytitle1",
                                         "id": "id1",
                                         "link": "url1",
                                         "author": "author1",
                                         "summary": "content1",
                                         "updated_parsed": updated},
                                        {"title": "entrytitle1",
                                         "id": "id1",
                                         "link": "url1",
                                         "author": "author1",
                                         "summary": "content1",
                                         "updated_parsed": updated}]}
        self.atomfeeddata = {"feed": {"title": "atomtitle",
                             "author": "myauthor",
                             "updated_parsed": updated},
                             "href": "feedurl",
                             "entries": [{"title": "entrytitle1",
                                          "id": "id1",
                                          "link": "url1",
                                          "author": "author1",
                                          "content": "content1",
                                          "updated_parsed": updated},
                                         {"title": "entrytitle1",
                                          "id": "id1",
                                          "link": "url1",
                                          "author": "author1",
                                          "content": "content1",
                                          "updated_parsed": updated}]}

    def testAtomInitFeed(self):
        feed = createFeedFromData(data=self.atomfeeddata)
        self.assertEqual(feed.title, self.atomfeeddata["feed"]["title"])
        self.assertEqual(feed.updated, \
                self.atomfeeddata["feed"]["updated_parsed"])
        self.assertEqual(feed.author, \
                self.atomfeeddata["feed"]["author"])
        self.assertEqual(feed.url, self.atomfeeddata["href"])

    def testRssInitFeed(self):
        feed = createFeedFromData(data=self.rssfeeddata)
        self.assertEqual(feed.title, self.rssfeeddata["feed"]["title"])
        self.assertEqual(feed.updated, \
                self.rssfeeddata["feed"]["updated_parsed"])
        self.assertEqual(feed.author, \
                self.rssfeeddata["feed"]["author"])
        self.assertEqual(feed.url, self.rssfeeddata["href"])

    def testRssInitEntry(self):
        data = self.rssfeeddata["entries"][0]
        entry = createEntryFromData(data=data)
        self.assertEqual(entry.title, data["title"])
        self.assertEqual(entry.author, data["author"])
        self.assertEqual(entry.url, data["link"])
        self.assertEqual(entry.identity, data["id"])
        self.assertEqual(entry.updated, data["updated_parsed"])
        self.assertEqual(entry.content, data["summary"])

    def testAtomInitEntry(self):
        data = self.atomfeeddata["entries"][0]
        entry = createEntryFromData(data=data)
        self.assertEqual(entry.title, data["title"])
        self.assertEqual(entry.author, data["author"])
        self.assertEqual(entry.url, data["link"])
        self.assertEqual(entry.identity, data["id"])
        self.assertEqual(entry.updated, data["updated_parsed"])
        self.assertEqual(entry.content, data["content"])

    def testMissingDataFeed(self):
        data = {"feed":{}, "entries":[]}
        feed = createFeedFromData(data=data)
        self.assertEqual(feed.title, "No Title provided")
        self.assertEqual(feed.author, "No Author provided")
        self.assertIsNone(feed.updated)
        self.assertIsNone(feed.url)

    def testMissingDataEntry(self):
        data = {}
        entry = createEntryFromData(data=data)
        self.assertEqual(entry.title, "No Title provided")
        self.assertEqual(entry.author, "No Author provided")
        self.assertEqual(entry.content, "No Content provided")
        self.assertIsNone(entry.updated)
        self.assertIsNone(entry.identity)
        self.assertIsNone(entry.url)

if __name__ == "__main__":
    unittest2.main()
