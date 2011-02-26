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
    if data["feed"].has_key("title"):
        feed.title = data["feed"]["title"]
    else:
        feed.title = "No Title provided"
    if data.has_key("href"):
        feed.url = data["href"]
    if data["feed"].has_key("author"):
        feed.author = data["feed"]["author"]
    else:
        feed.author = "No Author provided"
    if data["feed"].has_key("updated_parsed"):
        feed.updated = data["feed"]["updated_parsed"]
    for edata in data["entries"]:
        feed.entries.add(createEntryFromData(data=edata, entryclz=entryclz))
    return feed


def createEntryFromData(data, entryclz=Entry):
    entry = entryclz()
    if data.has_key("title"):
        entry.title = data["title"]
    else:
        entry.title = "No Title provided"
    if data.has_key("author"):
        entry.author = data["author"]
    else:
        entry.author = "No Author provided"
    if "summary" in data.keys():
        entry.content = data["summary"]
    elif data.has_key("content"):
        entry.content = data["content"]
    else:
        entry.content = "No Content provided"
    if data.has_key("updated_parsed"):
        entry.updated = data["updated_parsed"]
    if data.has_key("link"):
        entry.url = data["link"]
    if data.has_key("id"):
        entry.identity = data["id"]
    return entry

if __name__ == "__main__":
    import sys
    print "Cannot run this module"
    sys.exit(1)
