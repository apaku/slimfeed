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
from feed import Feed

def createFeedFromData(data, entryclz=Entry):
    feed = Feed()
    feed.title = data["feed"]["title"]
    feed.url = data["href"]
    feed.author = data["feed"]["author"]
    feed.updated = data["feed"]["updated_parsed"]
    for edata in data["entries"]:
        feed.entries.add(createEntryFromData(data=edata, entryclz=entryclz))
    return feed

def createEntryFromData(data, entryclz=Entry):
    entry = entryclz()
    entry.title = data["title"]
    entry.author = data["author"]
    if "summary" in data.keys():
        entry.content = data["summary"]
    else:
        entry.content = data["content"]
    entry.updated = data["updated_parsed"]
    entry.url = data["link"]
    entry.identity = data["id"]
    return entry

if __name__ == "__main__":
    import sys
    print "Cannot run this module"
    sys.exit(1)

