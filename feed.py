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

from entry import Entry

class Feed(object):
    def __init__(self):
        self._entries = set()
        self._title = ""
        self._author = ""
        self._updated = None
        self._url = ""

    def __hash__(self):
        return 3*hash(self.title)+5*hash(self.url)+7*hash(self.author)

    def gettitle(self):
        return self._title
    def settitle(self, title):
        self._title = title
    def deltitle(self):
        del self._title
    title = property(gettitle, settitle, deltitle, "Title of the feed")

    def getauthor(self):
        return self._author
    def setauthor(self, author):
        self._author = author
    def delauthor(self):
        del self._author
    author = property(getauthor, setauthor, delauthor, "Author of the feed")

    def geturl(self):
        return self._url
    def seturl(self, url):
        self._url = url
    def delurl(self):
        del self._url
    url = property(geturl, seturl, delurl, "Url of the feed")

    def getupdated(self):
        return self._updated
    def setupdated(self, updated):
        self._updated = updated
    def delupdated(self):
        del self._updated
    updated = property(getupdated, setupdated, delupdated, "Date of last update of the feed")

    def getentries(self):
        return self._entries
    def setentries(self, entries):
        self._entries = entries
    def delentries(self):
        del self._entries
    entries = property(getentries, setentries, delentries, "Entries of the feed")

    def load(self, store):
        self.title = store.getValue("Title")
        self.author = store.getValue("Author")
        self.updated = store.getValue("Updated")
        self.url = store.getValue("Url")
        for g in store.substores().values():
            e = Entry()
            e.load(g)
            self.entries.add(e)

    def save(self, store):
        from base64 import b64encode
        store.setValue("Title", self.title)
        store.setValue("Url", self.url)
        store.setValue("Updated", self.updated)
        store.setValue("Author", self.author)
        for entry in self._entries:
            entry.save(store.substores()["Entry_%s" %b64encode(entry.identity)])

if __name__ == "__main__":
    import sys
    print "Cannot run this module"
    sys.exit(1)

