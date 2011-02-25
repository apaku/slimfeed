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
        self.current_group = []

    def setValue(self, key, value):
        if len(self.current_group) > 0:
            self.data['/'.join(self.current_group + [key])] = value
        else:
            self.data[key] = value

    def value(self, key, default=None):
        try:
            if len(self.current_group) > 0:
                return self.data['/'.join(self.current_group + [key])]
            else:
                return self.data[key]
        except KeyError:
            return default

    def childGroups(self):
        cgroups = []
        for k in self.data.keys():
            if len(self.current_group) > 0:
                if k.startswith('/'.join(self.current_group)):
                    k = k[len('/'.join(self.current_group)) + 1:]
                else:
                    continue
            if '/' in k:
                k = k[0:k.index('/')]
                if not k in cgroups:
                    cgroups.append(k)
        return cgroups

    def beginGroup(self, grpname):
        self.current_group.append(grpname)

    def endGroup(self):
        self.current_group.pop()
