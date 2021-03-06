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
#pylint: disable=R0904


class SignalSpy(object):
    def __init__(self, signal):
        signal.connect(self.slot)
        self.slotTriggered = 0
        self.arguments = []
    def slot(self, *args):
        self.slotTriggered += 1
        self.arguments.append(args)

if __name__ == "__main__":
    import sys
    print "Cannot run this module"
    sys.exit(1)

