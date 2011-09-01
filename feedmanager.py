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
from datetime import datetime, date
import time

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
        updated = []
        for feed in self.feeds:
            newfeed = createFeedFromData(feedparser.parse(feed.url))
            if newfeed is not None:
                updateinfo = {'title':feed.title, 'keys':[], 'entries':[]}
                # These things should actually not be set from the update
                # the user may have changed at least the title
                #feed.title = newfeed.title
                #feed.url = newfeed.url
                #feed.author = newfeed.author
                #feed.homepage = newfeed.homepage
                if feed.updated != newfeed.updated:
                    feed.updated = newfeed.updated
                    updateinfo["keys"].append("updated")
                for entry in newfeed.entries:
                    if not entry in feed.entries and not entry.identity in feed.deleted_entry_ids:
                        updateinfo["entries"].append(entry)
                        feed.entries.append(entry)
                updated.append(updateinfo)
        return updated

    def getfeeds(self):
        return self._feeds

    def setfeeds(self, feeds):
        self._feeds = feeds

    feeds = property(getfeeds, setfeeds, None, "Feeds managed by this object")

    # Expose a list of entries to archive, necessary since direct deletion can cause inconsistency
    # between a possibly showing list of entries for one of the feeds
    def checkForArchiveableEntries(self, numberOfDaysEnabled, numberOfDays, numberOfArticlesEnabled, numberOfArticles):
        removedinfo = []
        for feed in self.feeds:
            feedinfo = {'feed': feed, 'entries':[]}
            if numberOfArticlesEnabled:
                sortedentries = sorted(feed.entries)
                if len(feed.entries) > numberOfArticles:
                    for entry in sortedentries[:numberOfArticles]:
                        feedinfo['entries'].append(entry)
            elif numberOfDaysEnabled:
                today = date.today()
                # Make sure to iterate over a copy so we do not step over entries if one is removed
                for entry in list(feed.entries):
                    # Need to convert since entries usually carry a time_struct
                    entrydatetime = datetime.fromtimestamp(time.mktime(entry.updated))
                    if (today - entrydatetime.date()).days > numberOfDays:
                        feedinfo['entries'].append(entry)
            removedinfo.append(feedinfo)
        return removedinfo


if __name__ == "__main__":
    import sys
    print "Cannot run this module"
    sys.exit(1)
