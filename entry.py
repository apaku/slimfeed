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

from qsettingsutils import _readQSettingsBoolEntry

class Entry(object):
    def __init__(self):
        self._url = None
        self._updated = None
        self._title = None
        self._id = None
        self._content = None
        self._author = None
        self._read = False
        self._important = False

    def __hash__(self):
        if not self._id is None and len(self._id) > 0:
            return hash(self._id)
        return 3 * hash(self._title) \
                + 5 * hash(self._author) \
                + 7 * hash(self._url) \
                + 13 * hash(self._important) \
                + 17 * hash(self._read)

    def _getread(self):
        return self._read

    def _setread(self, read):
        self._read = read

    read = property(_getread, _setread, None, \
            "Wether this entry was read already")

    def _geturl(self):
        return self._url

    def _seturl(self, url):
        self._url = url
    url = property(_geturl, _seturl, None, "Url of this entry")

    def _getimportant(self):
        return self._important

    def _setimportant(self, important):
        self._important = important
    important = property(_getimportant, _setimportant, None, "Important Mark")

    def _getupdated(self):
        return self._updated

    def _setupdated(self, updated):
        self._updated = updated

    updated = property(_getupdated, _setupdated, None, \
            "Date of last update of this entry")

    def _gettitle(self):
        return self._title

    def _settitle(self, title):
        self._title = title

    title = property(_gettitle, _settitle, None, "Title of this entry")

    def _getid(self):
        return self._id

    def _setid(self, identity):
        self._id = identity

    identity = property(_getid, _setid, None, "Id of this entry")

    def _getauthor(self):
        return self._author

    def _setauthor(self, author):
        self._author = author

    author = property(_getauthor, _setauthor, None, "Author of this entry")

    def _getcontent(self):
        return self._content

    def _setcontent(self, content):
        self._content = content

    content = property(_getcontent, _setcontent, None, "Content of this entry")

    def load(self, store):
        self.title = store.value("Title", None)
        self.author = store.value("Author", None)
        self.content = store.value("Content", None)
        self.updated = store.value("Updated", None)
        self.url = store.value("Url", None)
        self.identity = store.value("Id", None)
        self.read = _readQSettingsBoolEntry(store, "Read", False)
        self.important = _readQSettingsBoolEntry(store, "Important", False)

    def save(self, store):
        store.setValue("Title", self.title)
        store.setValue("Author", self.author)
        store.setValue("Content", self.content)
        store.setValue("Updated", self.updated)
        store.setValue("Url", self.url)
        store.setValue("Id", self.identity)
        store.setValue("Read", self.read)
        store.setValue("Important", self.important)

    def __lt__(self, other):
        return self.updated < other.updated

    def __eq__(self, other):
        if other is None:
            return False
        return (self.title == other.title \
                and self.author == other.author \
                and self.identity == other.identity \
                and self.url == other.url \
                and self.read == other.read \
                and self.important == other.important \
                and self.updated == other.updated \
                and self.content == other.content)

if __name__ == "__main__":
    import sys
    print "Cannot run this module"
    sys.exit(1)
