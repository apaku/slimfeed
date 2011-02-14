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

class Entry:
    def __init__(self,data=None):
        if data is not None:
            if "summary" in data.keys():
                self._content = data["summary"]
            else:
                self._content = data["content"]
            self._title = data["title"]
            self._author = data["author"]
            self._updated = data["updated_parsed"]
            self._url = data["link"]
            self._id = data["id"]

    def url(self):
        return self._url
    def updated(self):
        return self._updated
    def id(self):
        return self._id
    def author(self):
        return self._author
    def title(self):
        return self._title
    def content(self):
        return self._content

    def load(self, store):
        pass

    def save(self, store):
        pass

if __name__ == "__main__":
    import sys
    print "Cannot run this module"
    sys.exit(1)

