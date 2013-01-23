# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TabWidgetSearch.ui'
#
# Created: Wed Jan 23 12:30:40 2013
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

class Ui_TabWidgetSearch(object):
    def setupUi(self, TabWidgetSearch):
        TabWidgetSearch.setObjectName(_fromUtf8("TabWidgetSearch"))
        TabWidgetSearch.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(TabWidgetSearch)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.layoutLabels = QtGui.QVBoxLayout()
        self.layoutLabels.setObjectName(_fromUtf8("layoutLabels"))
        self.horizontalLayout.addLayout(self.layoutLabels)
        self.layoutLineedits = QtGui.QVBoxLayout()
        self.layoutLineedits.setObjectName(_fromUtf8("layoutLineedits"))
        self.horizontalLayout.addLayout(self.layoutLineedits)
        self.line_2 = QtGui.QFrame(TabWidgetSearch)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.horizontalLayout.addWidget(self.line_2)
        self.groupBox = QtGui.QGroupBox(TabWidgetSearch)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.radiobuttonAnd = QtGui.QRadioButton(self.groupBox)
        self.radiobuttonAnd.setChecked(True)
        self.radiobuttonAnd.setObjectName(_fromUtf8("radiobuttonAnd"))
        self.verticalLayout_4.addWidget(self.radiobuttonAnd)
        self.radiobuttonOr = QtGui.QRadioButton(self.groupBox)
        self.radiobuttonOr.setObjectName(_fromUtf8("radiobuttonOr"))
        self.verticalLayout_4.addWidget(self.radiobuttonOr)
        self.checkboxInvert = QtGui.QCheckBox(self.groupBox)
        self.checkboxInvert.setObjectName(_fromUtf8("checkboxInvert"))
        self.verticalLayout_4.addWidget(self.checkboxInvert)
        self.checkboxContained = QtGui.QCheckBox(self.groupBox)
        self.checkboxContained.setEnabled(False)
        self.checkboxContained.setObjectName(_fromUtf8("checkboxContained"))
        self.verticalLayout_4.addWidget(self.checkboxContained)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.groupBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(TabWidgetSearch)
        QtCore.QMetaObject.connectSlotsByName(TabWidgetSearch)

    def retranslateUi(self, TabWidgetSearch):
        TabWidgetSearch.setWindowTitle(_translate("TabWidgetSearch", "Form", None))
        self.groupBox.setTitle(_translate("TabWidgetSearch", "Search Options", None))
        self.radiobuttonAnd.setText(_translate("TabWidgetSearch", "AND", None))
        self.radiobuttonOr.setText(_translate("TabWidgetSearch", "OR", None))
        self.checkboxInvert.setText(_translate("TabWidgetSearch", "NOT", None))
        self.checkboxContained.setText(_translate("TabWidgetSearch", "contained matches", None))

