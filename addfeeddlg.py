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
import feedparser
from feedparserfactory import createFeedFromData
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QTimer
from PyQt4 import uic


# Disable 'method can be used as function' as it triggers on columnCount which
# indeed does not need the self, but we can't change that due to inheritance
# from Qt
#pylint: disable=R0201
class AddFeedDlg(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        uic.loadUi("addfeeddlg.ui", self)
        self.url.textEdited.connect(self.urlChanged)
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.updateTitleFromUrl)

    def urlChanged(self):
        self.timer.stop()
        self.timer.start(500)

    def updateTitleFromUrl(self):
        data = feedparser.parse(self.url.text())
        if "title" in data.feed:
            self.title.setText(data.feed.title)

    @classmethod
    def open(cls, parentwin, feedmodel):
        dlg = AddFeedDlg(parentwin)
        if dlg.exec_() == QDialog.Accepted:
            feed = createFeedFromData(feedparser.parse(dlg.url.text()))
            if len(dlg.title.text()) > 0 and dlg.title.text() != feed.title:
                feed.title = dlg.title.text()
            feedmodel.addFeed(feed)

if __name__ == "__main__":
    import sys
    print "Cannot run this module"
    sys.exit(1)
