# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Options.ui'
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

class Ui_DialogOptions(object):
    def setupUi(self, DialogOptions):
        DialogOptions.setObjectName(_fromUtf8("DialogOptions"))
        DialogOptions.setWindowModality(QtCore.Qt.ApplicationModal)
        DialogOptions.resize(750, 550)
        DialogOptions.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        DialogOptions.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(DialogOptions)
        self.buttonBox.setGeometry(QtCore.QRect(390, 500, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayoutWidget = QtGui.QWidget(DialogOptions)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 731, 481))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.treeviewOptionAreas = KuraOptionsTreeView(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeviewOptionAreas.sizePolicy().hasHeightForWidth())
        self.treeviewOptionAreas.setSizePolicy(sizePolicy)
        self.treeviewOptionAreas.setObjectName(_fromUtf8("treeviewOptionAreas"))
        self.horizontalLayout.addWidget(self.treeviewOptionAreas)
        self.widgetCurrentOptions = QtGui.QWidget(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetCurrentOptions.sizePolicy().hasHeightForWidth())
        self.widgetCurrentOptions.setSizePolicy(sizePolicy)
        self.widgetCurrentOptions.setObjectName(_fromUtf8("widgetCurrentOptions"))
        self.horizontalLayout.addWidget(self.widgetCurrentOptions)

        self.retranslateUi(DialogOptions)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogOptions.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogOptions.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogOptions)

    def retranslateUi(self, DialogOptions):
        DialogOptions.setWindowTitle(_translate("DialogOptions", "Kura Options", None))

from kuraoptionstreeview import KuraOptionsTreeView
