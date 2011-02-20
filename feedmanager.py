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

from feed import Feed

class FeedManager(object):
    def __init__(self):
        self._feeds = set()

    def load(self, store):
        for g in store.substores().values():
            f = Feed()
            f.load(g)
            self.feeds.add(f)

    def save(self, store):
        from base64 import b64encode
        for feed in self._feeds:
            feed.save(store.substores()["Feed_%s" %b64encode(feed.title)])

    def getfeeds(self):
        return self._feeds
    def setfeeds(self, feeds):
        self._feeds = feeds
    def delfeeds(self):
        del self._feeds
    feeds = property(getfeeds, setfeeds, delfeeds, "Feeds managed by this object")

if __name__ == "__main__":
    import sys
    print "Cannot run this module"
    sys.exit(1)

