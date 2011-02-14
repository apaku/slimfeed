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

class Feed:
    def __init__(self, data=None, entryClz=Entry):
        self._entries = []
        if data is not None:
            self._title = data["feed"]["title"]
            self._author = data["feed"]["author"]
            self._updated = data["feed"]["updated_parsed"]
            self._url = data["href"]
            for e in data["entries"]:
                self.addEntry(entryClz(data=e))

    def title(self):
        return self._title

    def author(self):
        return self._author

    def updated(self):
        return self._updated

    def url(self):
        return self._url

    def load(self, store):
        pass

    def save(self, store):
        for entry in self._entries:
            entry.save(store)

    def entries(self):
        return self._entries

    def addEntry(self, entry):
        if not entry in self._entries:
            self._entries.append(entry)

    def removeEntry(self, entry):
        if entry in self._entries:
            self._entries.remove(entry)

if __name__ == "__main__":
    import sys
    print "Cannot run this module"
    sys.exit(1)

