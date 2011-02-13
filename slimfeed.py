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

# Setup PyQt stuff.
import sip
sip.setapi("QString", 2)
sip.setapi("QDate", 2)
sip.setapi("QDateTime", 2)
sip.setapi("QTextStream", 2)
sip.setapi("QTime", 2)
sip.setapi("QUrl", 2)
sip.setapi("QVariant", 2)

from PyQt4 import QtCore, QtGui, uic
import sys

def main():
    app = QtGui.QApplication(sys.argv)
    mainwin = uic.loadUi("slimfeed.ui")
    mainwin.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())

