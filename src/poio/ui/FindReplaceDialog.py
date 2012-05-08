# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2012 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://www.cidles.eu/ltll/poio>
# For license information, see LICENSE.TXT

from PyQt4 import QtCore, QtGui
from Ui_FindReplaceDialog import Ui_FindReplaceDialog

class FindReplaceDialog(QtGui.QDialog):

    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_FindReplaceDialog()
        self.ui.setupUi(self)

    def set_text_edit(self, textedit):
        self.ui.findReplaceForm.set_text_edit(textedit)

    def changeEvent(self, event):
        QtGui.QDialog.changeEvent(self, event)
        if event.type() == QtCore.QEvent.LanguageChange:
            self.ui.retranslateUi(self)
