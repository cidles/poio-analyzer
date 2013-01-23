# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NewFileGraid.ui'
#
# Created: Wed Jan 23 09:51:04 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

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
        self.comboDataStructureType = QtGui.QComboBox(NewFileGraid)
        self.comboDataStructureType.setObjectName(_fromUtf8("comboDataStructureType"))
        self.comboDataStructureType.addItem(_fromUtf8(""))
        self.comboDataStructureType.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.comboDataStructureType)
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
        NewFileGraid.setWindowTitle(_translate("NewFileGraid", "Create a new file", None))
        self.radiobuttonPlainText.setText(_translate("NewFileGraid", "Plain Text", None))
        self.radioButtoTbStyleText.setText(_translate("NewFileGraid", "Toolbox-Style Text", None))
        self.comboDataStructureType.setItemText(0, _translate("NewFileGraid", "GRAID", None))
        self.comboDataStructureType.setItemText(1, _translate("NewFileGraid", "GRAID2 (Diana)", None))

