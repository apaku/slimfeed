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

class Entry(object):
    def __init__(self):
        self._url = ""
        self._updated = None
        self._title = ""
        self._id = ""
        self._content = ""
        self._author = ""

    def __hash__(self):
        if len(self._id) > 0:
            return hash(self._id)
        return 3*hash(self._title)+5*hash(self._author)+7*hash(self._url)
        
    def geturl(self):
        return self._url
    def seturl(self, url):
        self._url = url
    def delurl(self):
        del self._url
    url = property(geturl, seturl, delurl, "Url of this entry")

    def getupdated(self):
        return self._updated
    def setupdated(self, updated):
        self._updated = updated
    def delupdated(self):
        del self._updated
    updated = property(getupdated, setupdated, delupdated, "Date of last update of this entry")

    def gettitle(self):
        return self._title
    def settitle(self, title):
        self._title = title
    def deltitle(self):
        del self._title
    title = property(gettitle, settitle, deltitle, "Title of this entry")

    def getid(self):
        return self._id
    def setid(self, id):
        self._id = id
    def delid(self):
        del self._id
    identity = property(getid, setid, delid, "Id of this entry")

    def getauthor(self):
        return self._author
    def setauthor(self, author):
        self._author = author
    def delauthor(self):
        del self._author
    author = property(getauthor, setauthor, delauthor, "Author of this entry")

    def getcontent(self):
        return self._content
    def setcontent(self, content):
        self._content = content
    def delcontent(self):
        del self._content
    content = property(getcontent, setcontent, delcontent, "Content of this entry")

    def load(self, store):
        self.title = store.getValue("Title")
        self.author = store.getValue("Author")
        self.content = store.getValue("Content")
        self.updated = store.getValue("Updated")
        self.url = store.getValue("Url")
        self.identity = store.getValue("Id")

    def save(self, store):
        store.setValue("Title", self.title)
        store.setValue("Author", self.author)
        store.setValue("Content", self.content)
        store.setValue("Updated", self.updated)
        store.setValue("Url", self.url)
        store.setValue("Id", self.identity)

if __name__ == "__main__":
    import sys
    print "Cannot run this module"
    sys.exit(1)

