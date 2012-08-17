# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NewTier.ui'
#
# Created: Fri Aug 17 11:06:21 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DialogNewTier(object):
    def setupUi(self, DialogNewTier):
        DialogNewTier.setObjectName(_fromUtf8("DialogNewTier"))
        DialogNewTier.resize(414, 251)
        DialogNewTier.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.buttonBox = QtGui.QDialogButtonBox(DialogNewTier)
        self.buttonBox.setGeometry(QtCore.QRect(60, 200, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayoutWidget = QtGui.QWidget(DialogNewTier)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 391, 161))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineeditTierId = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineeditTierId.setObjectName(_fromUtf8("lineeditTierId"))
        self.gridLayout.addWidget(self.lineeditTierId, 1, 1, 1, 1)
        self.lineeditTierType = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineeditTierType.setObjectName(_fromUtf8("lineeditTierType"))
        self.gridLayout.addWidget(self.lineeditTierType, 2, 1, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.labelParentTier = QtGui.QLabel(self.gridLayoutWidget)
        self.labelParentTier.setText(_fromUtf8(""))
        self.labelParentTier.setObjectName(_fromUtf8("labelParentTier"))
        self.gridLayout.addWidget(self.labelParentTier, 0, 1, 1, 1)
        self.lineeditDefaultLocale = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineeditDefaultLocale.setObjectName(_fromUtf8("lineeditDefaultLocale"))
        self.gridLayout.addWidget(self.lineeditDefaultLocale, 3, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.lineeditParticipant = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineeditParticipant.setObjectName(_fromUtf8("lineeditParticipant"))
        self.gridLayout.addWidget(self.lineeditParticipant, 4, 1, 1, 1)

        self.retranslateUi(DialogNewTier)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogNewTier.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogNewTier.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogNewTier)

    def retranslateUi(self, DialogNewTier):
        DialogNewTier.setWindowTitle(QtGui.QApplication.translate("DialogNewTier", "Create a new tier", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DialogNewTier", "Tier ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("DialogNewTier", "Tier type:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DialogNewTier", "Parent tier:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("DialogNewTier", "Default locale:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("DialogNewTier", "Participant:", None, QtGui.QApplication.UnicodeUTF8))

