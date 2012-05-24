# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FindReplaceForm.ui'
#
# Created: Thu May 24 14:45:22 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FindReplaceForm(object):
    def setupUi(self, FindReplaceForm):
        FindReplaceForm.setObjectName(_fromUtf8("FindReplaceForm"))
        FindReplaceForm.resize(483, 288)
        FindReplaceForm.setWindowTitle(QtGui.QApplication.translate("FindReplaceForm", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout = QtGui.QGridLayout(FindReplaceForm)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label = QtGui.QLabel(FindReplaceForm)
        self.label.setText(QtGui.QApplication.translate("FindReplaceForm", "&Find:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.textToFind = QtGui.QLineEdit(FindReplaceForm)
        self.textToFind.setObjectName(_fromUtf8("textToFind"))
        self.gridLayout_3.addWidget(self.textToFind, 0, 1, 1, 1)
        self.replaceLabel = QtGui.QLabel(FindReplaceForm)
        self.replaceLabel.setText(QtGui.QApplication.translate("FindReplaceForm", "R&eplace with:", None, QtGui.QApplication.UnicodeUTF8))
        self.replaceLabel.setObjectName(_fromUtf8("replaceLabel"))
        self.gridLayout_3.addWidget(self.replaceLabel, 1, 0, 1, 1)
        self.textToReplace = QtGui.QLineEdit(FindReplaceForm)
        self.textToReplace.setObjectName(_fromUtf8("textToReplace"))
        self.gridLayout_3.addWidget(self.textToReplace, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_3)
        self.verticalLayout_5.addLayout(self.verticalLayout_2)
        self.errorLabel = QtGui.QLabel(FindReplaceForm)
        self.errorLabel.setText(QtGui.QApplication.translate("FindReplaceForm", "errorLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.errorLabel.setObjectName(_fromUtf8("errorLabel"))
        self.verticalLayout_5.addWidget(self.errorLabel)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(FindReplaceForm)
        self.groupBox.setTitle(QtGui.QApplication.translate("FindReplaceForm", "D&irection", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.downRadioButton = QtGui.QRadioButton(self.groupBox)
        self.downRadioButton.setText(QtGui.QApplication.translate("FindReplaceForm", "&Down", None, QtGui.QApplication.UnicodeUTF8))
        self.downRadioButton.setChecked(True)
        self.downRadioButton.setObjectName(_fromUtf8("downRadioButton"))
        self.verticalLayout_3.addWidget(self.downRadioButton)
        self.upRadioButton = QtGui.QRadioButton(self.groupBox)
        self.upRadioButton.setText(QtGui.QApplication.translate("FindReplaceForm", "&Up", None, QtGui.QApplication.UnicodeUTF8))
        self.upRadioButton.setObjectName(_fromUtf8("upRadioButton"))
        self.verticalLayout_3.addWidget(self.upRadioButton)
        self.horizontalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(FindReplaceForm)
        self.groupBox_2.setTitle(QtGui.QApplication.translate("FindReplaceForm", "&Options", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.caseCheckBox = QtGui.QCheckBox(self.groupBox_2)
        self.caseCheckBox.setText(QtGui.QApplication.translate("FindReplaceForm", "&Case sensitive", None, QtGui.QApplication.UnicodeUTF8))
        self.caseCheckBox.setObjectName(_fromUtf8("caseCheckBox"))
        self.verticalLayout_4.addWidget(self.caseCheckBox)
        self.wholeCheckBox = QtGui.QCheckBox(self.groupBox_2)
        self.wholeCheckBox.setText(QtGui.QApplication.translate("FindReplaceForm", "&Whole words only", None, QtGui.QApplication.UnicodeUTF8))
        self.wholeCheckBox.setObjectName(_fromUtf8("wholeCheckBox"))
        self.verticalLayout_4.addWidget(self.wholeCheckBox)
        self.regexCheckBox = QtGui.QCheckBox(self.groupBox_2)
        self.regexCheckBox.setToolTip(QtGui.QApplication.translate("FindReplaceForm", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">whether the text to search should be interpreted as a regular expression.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You may want to take a look at the syntax of regular expressions:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://doc.trolltech.com/qregexp.html\"><span style=\" text-decoration: underline; color:#0000ff;\">http://doc.trolltech.com/qregexp.html</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.regexCheckBox.setText(QtGui.QApplication.translate("FindReplaceForm", "R&egular Expression", None, QtGui.QApplication.UnicodeUTF8))
        self.regexCheckBox.setObjectName(_fromUtf8("regexCheckBox"))
        self.verticalLayout_4.addWidget(self.regexCheckBox)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_5, 0, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, -1, -1, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.findButton = QtGui.QPushButton(FindReplaceForm)
        self.findButton.setEnabled(False)
        self.findButton.setText(QtGui.QApplication.translate("FindReplaceForm", "&Find", None, QtGui.QApplication.UnicodeUTF8))
        self.findButton.setObjectName(_fromUtf8("findButton"))
        self.verticalLayout.addWidget(self.findButton)
        self.closeButton = QtGui.QPushButton(FindReplaceForm)
        self.closeButton.setText(QtGui.QApplication.translate("FindReplaceForm", "&Close", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.verticalLayout.addWidget(self.closeButton)
        self.replaceButton = QtGui.QPushButton(FindReplaceForm)
        self.replaceButton.setEnabled(False)
        self.replaceButton.setText(QtGui.QApplication.translate("FindReplaceForm", "&Replace", None, QtGui.QApplication.UnicodeUTF8))
        self.replaceButton.setObjectName(_fromUtf8("replaceButton"))
        self.verticalLayout.addWidget(self.replaceButton)
        self.replaceAllButton = QtGui.QPushButton(FindReplaceForm)
        self.replaceAllButton.setEnabled(False)
        self.replaceAllButton.setText(QtGui.QApplication.translate("FindReplaceForm", "Replace &All", None, QtGui.QApplication.UnicodeUTF8))
        self.replaceAllButton.setObjectName(_fromUtf8("replaceAllButton"))
        self.verticalLayout.addWidget(self.replaceAllButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.label.setBuddy(self.textToFind)
        self.replaceLabel.setBuddy(self.textToReplace)

        self.retranslateUi(FindReplaceForm)
        QtCore.QMetaObject.connectSlotsByName(FindReplaceForm)
        FindReplaceForm.setTabOrder(self.textToFind, self.textToReplace)
        FindReplaceForm.setTabOrder(self.textToReplace, self.downRadioButton)
        FindReplaceForm.setTabOrder(self.downRadioButton, self.upRadioButton)
        FindReplaceForm.setTabOrder(self.upRadioButton, self.caseCheckBox)
        FindReplaceForm.setTabOrder(self.caseCheckBox, self.wholeCheckBox)
        FindReplaceForm.setTabOrder(self.wholeCheckBox, self.regexCheckBox)
        FindReplaceForm.setTabOrder(self.regexCheckBox, self.findButton)
        FindReplaceForm.setTabOrder(self.findButton, self.closeButton)

    def retranslateUi(self, FindReplaceForm):
        pass

