# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Options.ui'
#
# Created: Wed Feb  2 17:03:18 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DialogOptions(object):
    def setupUi(self, DialogOptions):
        DialogOptions.setObjectName("DialogOptions")
        DialogOptions.setWindowModality(QtCore.Qt.ApplicationModal)
        DialogOptions.resize(750, 550)
        DialogOptions.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        DialogOptions.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(DialogOptions)
        self.buttonBox.setGeometry(QtCore.QRect(390, 500, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayoutWidget = QtGui.QWidget(DialogOptions)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 731, 481))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.treeviewOptionAreas = KuraOptionsTreeView(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeviewOptionAreas.sizePolicy().hasHeightForWidth())
        self.treeviewOptionAreas.setSizePolicy(sizePolicy)
        self.treeviewOptionAreas.setObjectName("treeviewOptionAreas")
        self.horizontalLayout.addWidget(self.treeviewOptionAreas)
        self.widgetCurrentOptions = QtGui.QWidget(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetCurrentOptions.sizePolicy().hasHeightForWidth())
        self.widgetCurrentOptions.setSizePolicy(sizePolicy)
        self.widgetCurrentOptions.setObjectName("widgetCurrentOptions")
        self.horizontalLayout.addWidget(self.widgetCurrentOptions)

        self.retranslateUi(DialogOptions)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), DialogOptions.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), DialogOptions.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogOptions)

    def retranslateUi(self, DialogOptions):
        DialogOptions.setWindowTitle(QtGui.QApplication.translate("DialogOptions", "Kura Options", None, QtGui.QApplication.UnicodeUTF8))

from kuraoptionstreeview import KuraOptionsTreeView
