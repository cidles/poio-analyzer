# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2012 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://www.cidles.eu/ltll/poio>
# For license information, see LICENSE.TXT

from PyQt4 import QtCore, QtGui
from Ui_FindReplaceForm import Ui_FindReplaceForm

class FindReplaceForm(QtGui.QWidget):

    def __init__(self, parent):
        """
        Initializes the find & replace form
        """
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_FindReplaceForm()
        self.ui.setupUi(self)

        self.ui.errorLabel.setText("")

        self.ui.textToFind.textChanged.connect(self.text_to_find_changed)
        self.ui.textToFind.textChanged.connect(self.validate_regexp)

        self.ui.regexCheckBox.toggled.connect(self.regexp_selected)

        self.ui.findButton.clicked.connect(self.find)
        self.ui.closeButton.clicked.connect(parent.close)

        self.ui.replaceButton.clicked.connect(self.replace)
        self.ui.replaceAllButton.clicked.connect(self.replace_all)

        self.textedit = None
        self.regexp = QtCore.QRegExp()
        self.textcursor = None

    def hide_replace_widgets(self):
        """
        Hide widgets used to replace
        """
        self.ui.replaceLabel.setVisible(False)
        self.ui.textToReplace.setVisible(False)
        self.ui.replaceButton.setVisible(False)
        self.ui.replaceAllButton.setVisible(False)

    def set_text_edit(self, textedit):
        """
        Set the text edit and enable the buttons
        """
        self.textedit = textedit
        self.textedit.copyAvailable.connect(self.ui.replaceButton.setEnabled)
        self.textedit.copyAvailable.connect(
            self.ui.replaceAllButton.setEnabled)

        self.textcursor = self.textedit.textCursor()

    def changeEvent(self, event):
        """
        If the language has changed retranlate the UI accordingly
        """
        QtGui.QWidget.changeEvent(self, event)
        if event.type() == QtCore.QEvent.LanguageChange:
            self.ui.retranslateUi(self)

    def text_to_find_changed(self, _):
        """
        Enable the find button if text to find is not null
        """
        self.ui.findButton.setEnabled(self.ui.textToFind.size() > 0)

    def regexp_selected(self, sel):
        """
        Validate rege xp
        """
        if sel:
            self.validate_regexp(self.ui.textToFind.text())
        else:
            self.validate_regexp("")

    def validate_regexp(self, regexp):
        """
        Check if regexp is valid
        """
        if (not self.ui.regexCheckBox.isChecked()) or regexp.size() == 0:
            self.ui.errorLabel.setText("")

        self.regexp = QtCore.QRegExp(regexp,
            QtCore.Qt.CaseSensitive
            if self.ui.caseCheckBox.isChecked() else QtCore.Qt.CaseInsensitive)

        if self.regexp.isValid():
            self.show_error("")
        else:
            self.show_error(unicode(regexp.errorString()))

    def show_error(self, error):
        """
        Diplay error message
        """
        if (error == ""):
            self.ui.errorLabel.setText("")
        else:
            self.ui.errorLabel.setText("<span style=\"font-weight:600; color:#ff0000;\">{0}</span>".format(error))

    def show_message(self, message):
        """
        Display message
        """
        if (message == ""):
            self.ui.errorLabel.setText("")
        else:
            self.ui.errorLabel.setText("<span style=\"font-weight:600; color:green;\">{0}</span>".format(message))

    def find(self, next = None):
        """
        Parameters
        ----------
        next = bool
        back : bool
        toSearch : str
        result : bool
        flags : Flags
        """

        if not self.textedit:
            return

        if not next:
            next = self.ui.downRadioButton.isChecked()

        back = not next
        toSearch = self.ui.textToFind.text()
        result = False

        flags = QtGui.QTextDocument.FindFlags()
        if (back):
            flags |= QtGui.QTextDocument.FindBackward
        if self.ui.caseCheckBox.isChecked():
            flags |= QtGui.QTextDocument.FindCaseSensitively
        if self.ui.wholeCheckBox.isChecked():
            flags |= QtGui.QTextDocument.FindWholeWords

        if self.ui.regexCheckBox.isChecked():
            self.regexp = QtCore.QRegExp(toSearch,
                QtCore.Qt.CaseSensitive
                if self.ui.caseCheckBox.isChecked()
                else QtCore.Qt.CaseInsensitive)
            self.textcursor = self.textedit.document().find(regexp, self.textcursor, flags)
            self.textedit.setTextCursor(self.textcursor)
            result = not self.textcursor.isNull()
        else:
            result = self.textedit.find(toSearch, flags)

        if result:
            self.show_error("")
        else:
            self.show_error(self.tr("no text found"))
            self.textcursor.setPosition(0)
            self.textedit.setTextCursor(self.textcursor)

    def replace(self):
        """
        Replaces text
        """
        if not self.textedit.textCursor().hasSelection():
            self.find()
        else:
            self.textedit.textCursor().insertText(self.ui.textToReplace.text())
            self.find()

    def replace_all(self):
        """
        Replaces all the given text
        """
        i = 0
        while self.textedit.textCursor().hasSelection():
            self.textedit.textCursor().insertText(self.ui.textToReplace.text())
            self.find()
            i += 1
        self.show_message(unicode(self.tr("Replaced {0} occurrence(s)")).format(i))

