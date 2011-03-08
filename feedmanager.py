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
import feedparser
from feedparserfactory import createFeedFromData


class FeedManager(object):
    def __init__(self):
        self._feeds = []

    def load(self, store):
        for group in store.childGroups():
            store.beginGroup(group)
            feed = Feed()
            feed.load(store)
            self.feeds.append(feed)
            store.endGroup()

    def save(self, store):
        from base64 import b64encode
        for feed in self._feeds:
            store.beginGroup("Feed_%s" % b64encode(str(hash(feed))))
            feed.save(store)
            store.endGroup()

    def update(self):
        for feed in self.feeds:
            newfeed = createFeedFromData(feedparser.parse(feed.url))
            feed.title = newfeed.title
            feed.url = newfeed.url
            feed.author = newfeed.author
            feed.homepage = newfeed.homepage
            feed.updated = newfeed.updated
            for entry in newfeed.entries:
                if not entry in feed.entries:
                    feed.entries.append(entry)

    def getfeeds(self):
        return self._feeds

    def setfeeds(self, feeds):
        self._feeds = feeds

    feeds = property(getfeeds, setfeeds, None, "Feeds managed by this object")

if __name__ == "__main__":
    import sys
    print "Cannot run this module"
    sys.exit(1)
