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
        self.updatetime = time.localtime()
        self.entrydatarss = {"summary":"This is the content", "title":"EntryTitle", "updated_parsed":self.updatetime,"link":"http://localhost/entry","id":"http://localhost/entry?p12", "author":"MeAgain"}
        self.entrydataatom = {"content":"This is the content", "title":"EntryTitle", "updated_parsed":self.updatetime,"link":"http://localhost/entry","id":"http://localhost/entry?p12", "author":"MeAgain"}

    def testInitFromDataRss(self):
        f = Entry(data=self.entrydatarss)
        self.assertEqual(f.title(),self.entrydatarss["title"])
        self.assertEqual(f.author(),self.entrydatarss["author"])
        self.assertEqual(f.updated(),self.entrydatarss["updated_parsed"])
        self.assertEqual(f.url(),self.entrydatarss["link"])
        self.assertEqual(f.content(),self.entrydatarss["summary"])
        self.assertEqual(f.id(),self.entrydatarss["id"])

    def testInitFromDataAtom(self):
        f = Entry(data=self.entrydataatom)
        self.assertEqual(f.title(),self.entrydataatom["title"])
        self.assertEqual(f.author(),self.entrydataatom["author"])
        self.assertEqual(f.updated(),self.entrydataatom["updated_parsed"])
        self.assertEqual(f.url(),self.entrydataatom["link"])
        self.assertEqual(f.content(),self.entrydataatom["content"])
        self.assertEqual(f.id(),self.entrydataatom["id"])

    def testSave(self):
        self.entry.save(StoreMock())

if __name__ == "__main__":
    unittest.main()

