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

import initsip
initsip.setupSipApi()
from PyQt4 import QtGui, uic

class Preferences(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        uic.loadUi("preferences.ui", self)
    
    def _setUpdateTimeout(self, timeout):
        self.updateTimeoutBox.setValue(timeout)
    def _updateTimeout(self):
        return self.updateTimeoutBox.value()
    updateTimeout = property(_updateTimeout, _setUpdateTimeout, None, "Timeout after which feeds are updated")
        
    def _setMarkReadTimeout(self, timeout):
        self.markReadTimeoutBox.setValue(timeout)
    def _markReadTimeout(self):
        return self.markReadTimeoutBox.value()
    markReadTimeout = property(_markReadTimeout, _setMarkReadTimeout, None, "Timeout after which is marked as read")
        