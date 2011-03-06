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
    if "title" in data["feed"]:
        feed.title = data["feed"]["title"]
    else:
        feed.title = "No Title provided"

    if "links" in data["feed"]:
        for link in data["feed"]["links"]:
            if "rel" in link and link["rel"] == "self":
                feed.url = link["href"]
    if "link" in data["feed"]:
        feed.homepage = data["feed"]["link"]
    if "author" in data["feed"]:
        feed.author = data["feed"]["author"]
    else:
        feed.author = "No Author provided"
    if "updated_parsed" in data["feed"]:
        feed.updated = data["feed"]["updated_parsed"]
    for edata in data["entries"]:
        feed.entries.append(createEntryFromData(data=edata, entryclz=entryclz))
    return feed


def createEntryFromData(data, entryclz=Entry):
    entry = entryclz()
    if "title" in data:
        entry.title = data["title"]
    else:
        entry.title = "No Title provided"
    if "author" in data:
        entry.author = data["author"]
    else:
        entry.author = "No Author provided"
    if "summary" in data.keys():
        entry.content = data["summary"]
    elif "content" in data:
        entry.content = data["content"]
    else:
        entry.content = "No Content provided"
    if "updated_parsed" in data:
        entry.updated = data["updated_parsed"]
    if "link" in data:
        entry.url = data["link"]
    if "id" in data:
        entry.identity = data["id"]
    return entry

if __name__ == "__main__":
    import sys
    print "Cannot run this module"
    sys.exit(1)
