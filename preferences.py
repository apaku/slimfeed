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
        self.systrayColorChooser.clicked.connect(self.chooseColor)

    def chooseColor(self):
        dlg = QtGui.QColorDialog(self)
        dlg.setCurrentColor(self._systraycolor)
        if dlg.exec_() == QtGui.QDialog.Accepted:
            self.systrayFontColor = dlg.selectedColor()

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

    def _setSystrayFontColor(self, color):
        # size needs to match the one from the button
        self._systraycolor = color
        pixmap = QtGui.QPixmap(16,16)
        pixmap.fill(color)
        self._systraycolorchooseIcon = QtGui.QIcon(pixmap)
        self.systrayColorChooser.setIcon(self._systraycolorchooseIcon)
    def _systrayFontColor(self):
        return self._systraycolor
    systrayFontColor = property(_systrayFontColor, _setSystrayFontColor, None, "Font color to be used for the system tray")

    def _setSystrayFont(self, font):
        self.systrayFontCombo.setCurrentFont(font)
    def _systrayFont(self):
        return self.systrayFontCombo.currentFont()
    systrayFont = property(_systrayFont, _setSystrayFont, None, "Font to be used for the system tray")
