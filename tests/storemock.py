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

class StoreMock:
    def __init__(self):
        self.data = {}
        self.currentGroup = []

    def setValue(self, key, value):
        if len(self.currentGroup) > 0:
            self.data['/'.join(self.currentGroup + [key])] = value
        else:
            self.data[key] = value

    def value(self, key, default=None):
        try:
            if len(self.currentGroup) > 0:
                return self.data['/'.join(self.currentGroup + [key])]
            else:
                return self.data[key]
        except KeyError:
            return default

    def childGroups(self):
        l = []
        for k in self.data.keys():
            if len(self.currentGroup) > 0:
                if k.startswith('/'.join(self.currentGroup)):
                    k = k[len('/'.join(self.currentGroup))+1:]
                else:
                    continue
            if '/' in k:
                k = k[0:k.index('/')]
                if not k in l:
                    l.append(k)
        return l

    def beginGroup(self, grpname):
        self.currentGroup.append(grpname)

    def endGroup(self):
        self.currentGroup.pop()

