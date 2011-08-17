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
from PyQt4 import QtCore

def _readQSettingsBoolEntry(store, key, defValue):
    if QtCore.PYQT_VERSION >= 0x040800:
        return store.value(key, defValue, bool)
    else:
        # Workaround for QSettings returning wrong type from
        # value if its not been used to set the value in this
        # python interpreter instance
        # In PyQt 4.8 and later there's a new overload for value to
        # specify the return type
        data = store.value(key, defValue)
        if isinstance(data, str) or isinstance(data, unicode):
            if data.lower() in ["true", "1"]:
                data = True
            elif data.lower() in ["false", "0"]:
                data = False
            else:
                assert None, "Cannot convert string to bool: %s" % data
        return data
