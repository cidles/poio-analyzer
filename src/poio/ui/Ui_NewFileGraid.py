# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NewFileGraid.ui'
#
# Created: Fri Jan 27 13:20:19 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_NewFileGraid(object):
    def setupUi(self, NewFileGraid):
        NewFileGraid.setObjectName(_fromUtf8("NewFileGraid"))
        NewFileGraid.resize(640, 480)
        self.verticalLayout_2 = QtGui.QVBoxLayout(NewFileGraid)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.radiobuttonPlainText = QtGui.QRadioButton(NewFileGraid)
        self.radiobuttonPlainText.setChecked(True)
        self.radiobuttonPlainText.setObjectName(_fromUtf8("radiobuttonPlainText"))
        self.horizontalLayout_2.addWidget(self.radiobuttonPlainText)
        self.radioButtoTbStyleText = QtGui.QRadioButton(NewFileGraid)
        self.radioButtoTbStyleText.setObjectName(_fromUtf8("radioButtoTbStyleText"))
        self.horizontalLayout_2.addWidget(self.radioButtoTbStyleText)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.textedit = QtGui.QPlainTextEdit(NewFileGraid)
        self.textedit.setObjectName(_fromUtf8("textedit"))
        self.verticalLayout.addWidget(self.textedit)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(NewFileGraid)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(NewFileGraid)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NewFileGraid.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NewFileGraid.reject)
        QtCore.QMetaObject.connectSlotsByName(NewFileGraid)

    def retranslateUi(self, NewFileGraid):
        NewFileGraid.setWindowTitle(QtGui.QApplication.translate("NewFileGraid", "Create a new file", None, QtGui.QApplication.UnicodeUTF8))
        self.radiobuttonPlainText.setText(QtGui.QApplication.translate("NewFileGraid", "Plain Text", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtoTbStyleText.setText(QtGui.QApplication.translate("NewFileGraid", "Toolbox-Style Text", None, QtGui.QApplication.UnicodeUTF8))

