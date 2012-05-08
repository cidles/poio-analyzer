# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2012 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://www.cidles.eu/ltll/poio>
# For license information, see LICENSE.TXT

from PyQt4 import QtCore, QtGui
from FindReplaceDialog import FindReplaceDialog

class FindDialog(FindReplaceDialog):

    def __init__(self, parent):
        FindReplaceDialog.__init__(self, parent)
        self.ui.findReplaceForm.hide_replace_widgets()
        self.setWindowTitle(self.tr("Find"))
