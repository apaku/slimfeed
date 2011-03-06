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
        self._entries = []
        self._title = None
        self._author = None
        self._updated = None
        self._url = None
        self._homepage = None

    def __hash__(self):
        return 3 * hash(self.title) \
                + 5 * hash(self.url) \
                + 7 * hash(self.author)

    def _gettitle(self):
        return self._title

    def _settitle(self, title):
        self._title = title

    title = property(_gettitle, _settitle, None, "Title of the feed")

    def _getunread(self):
        return len([e for e in self.entries if not e.read])
    unread = property(_getunread, None, None, "Number of unread entries")

    def _getauthor(self):
        return self._author

    def _setauthor(self, author):
        self._author = author

    author = property(_getauthor, _setauthor, "Author of the feed")

    def _gethomepage(self):
        return self._homepage

    def _sethomepage(self, homepage):
        self._homepage = homepage

    homepage = property(_gethomepage, _sethomepage, None,
                        "Homepage of the feed")

    def _geturl(self):
        return self._url

    def _seturl(self, url):
        self._url = url

    url = property(_geturl, _seturl, None, "Url of the feed")

    def _getupdated(self):
        return self._updated

    def _setupdated(self, updated):
        self._updated = updated

    updated = property(_getupdated, _setupdated, None, \
            "Date of last update of the feed")

    def _getentries(self):
        return self._entries

    def _setentries(self, entries):
        self._entries = entries

    entries = property(_getentries, _setentries, None, "Entries of the feed")

    def __eq__(self, other):
        if other is None:
            return False
        return (self.title == other.title \
                and self.author == other.author \
                and self.entries == other.entries \
                and self.updated == other.updated \
                and self.url == other.url)

    def load(self, store):
        self.title = store.value("Title", None)
        self.author = store.value("Author", None)
        self.updated = store.value("Updated", None)
        self.url = store.value("Url", None)
        self.homepage = store.value("Homepage", None)
        for group in store.childGroups():
            store.beginGroup(group)
            entry = Entry()
            entry.load(store)
            self.entries.append(entry)
            store.endGroup()

    def save(self, store):
        from base64 import b64encode
        store.setValue("Title", self.title)
        store.setValue("Url", self.url)
        store.setValue("Homepage", self.homepage)
        store.setValue("Updated", self.updated)
        store.setValue("Author", self.author)
        for entry in self._entries:
            store.beginGroup("Entry_%s" % b64encode(str(hash(entry.identity))))
            entry.save(store)
            store.endGroup()

if __name__ == "__main__":
    import sys
    print "Cannot run this module"
    sys.exit(1)
