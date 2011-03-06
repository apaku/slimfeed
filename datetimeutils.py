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

from initsip import setupSipApi

setupSipApi()

from PyQt4.QtCore import Qt, QDateTime


def qDateTimeFromTimeStruct(time):
    return QDateTime(time.tm_year, time.tm_mon,
                     time.tm_mday, time.tm_hour,
                     time.tm_min, time.tm_sec,
                     0, Qt.UTC)

if __name__ == "__main__":
    import sys
    print "Cannot run this module"
    sys.exit(1)
