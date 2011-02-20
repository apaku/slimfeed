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

class SubStoresMock(dict):
    def __getitem__(self, name):
        try:
            dict.__getitem__(self, name)
        except KeyError:
            dict.__setitem__(self, name, StoreMock())
            return dict.__getitem__(self, name)

class StoreMock:
    def __init__(self):
        self.data = {}
        self.subs = SubStoresMock()
    def setValue(self, key, value):
        self.data[key] = value
    def getValue(self, key):
        return self.data[key]
    def substores(self):
        return self.subs


