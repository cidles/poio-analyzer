# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TabWidgetSearch.ui'
#
# Created: Fri Feb 17 10:35:53 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TabWidgetSearch(object):
    def setupUi(self, TabWidgetSearch):
        TabWidgetSearch.setObjectName(_fromUtf8("TabWidgetSearch"))
        TabWidgetSearch.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(TabWidgetSearch)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_2 = QtGui.QLabel(TabWidgetSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setSizeIncrement(QtCore.QSize(1, 0))
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.lineeditSearchUtterances = QtGui.QLineEdit(TabWidgetSearch)
        self.lineeditSearchUtterances.setSizeIncrement(QtCore.QSize(2, 0))
        self.lineeditSearchUtterances.setObjectName(_fromUtf8("lineeditSearchUtterances"))
        self.gridLayout_2.addWidget(self.lineeditSearchUtterances, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(TabWidgetSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setSizeIncrement(QtCore.QSize(1, 0))
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.lineeditSearchWords = QtGui.QLineEdit(TabWidgetSearch)
        self.lineeditSearchWords.setSizeIncrement(QtCore.QSize(2, 0))
        self.lineeditSearchWords.setObjectName(_fromUtf8("lineeditSearchWords"))
        self.gridLayout_2.addWidget(self.lineeditSearchWords, 1, 1, 1, 1)
        self.label_4 = QtGui.QLabel(TabWidgetSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setSizeIncrement(QtCore.QSize(1, 0))
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.lineeditSearchMorphemes = QtGui.QLineEdit(TabWidgetSearch)
        self.lineeditSearchMorphemes.setSizeIncrement(QtCore.QSize(2, 0))
        self.lineeditSearchMorphemes.setObjectName(_fromUtf8("lineeditSearchMorphemes"))
        self.gridLayout_2.addWidget(self.lineeditSearchMorphemes, 2, 1, 1, 1)
        self.label_5 = QtGui.QLabel(TabWidgetSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setSizeIncrement(QtCore.QSize(1, 0))
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 1)
        self.lineeditSearchGlosses = QtGui.QLineEdit(TabWidgetSearch)
        self.lineeditSearchGlosses.setSizeIncrement(QtCore.QSize(2, 0))
        self.lineeditSearchGlosses.setObjectName(_fromUtf8("lineeditSearchGlosses"))
        self.gridLayout_2.addWidget(self.lineeditSearchGlosses, 3, 1, 1, 1)
        self.label_6 = QtGui.QLabel(TabWidgetSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setSizeIncrement(QtCore.QSize(1, 0))
        self.label_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 4, 0, 1, 1)
        self.lineeditSearchTranslations = QtGui.QLineEdit(TabWidgetSearch)
        self.lineeditSearchTranslations.setSizeIncrement(QtCore.QSize(2, 0))
        self.lineeditSearchTranslations.setObjectName(_fromUtf8("lineeditSearchTranslations"))
        self.gridLayout_2.addWidget(self.lineeditSearchTranslations, 4, 1, 1, 1)
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
        self.checkboxContained.setObjectName(_fromUtf8("checkboxContained"))
        self.verticalLayout_4.addWidget(self.checkboxContained)
        self.gridLayout_2.addWidget(self.groupBox, 0, 3, 5, 1)
        self.line_2 = QtGui.QFrame(TabWidgetSearch)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout_2.addWidget(self.line_2, 0, 2, 5, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)

        self.retranslateUi(TabWidgetSearch)
        QtCore.QMetaObject.connectSlotsByName(TabWidgetSearch)

    def retranslateUi(self, TabWidgetSearch):
        TabWidgetSearch.setWindowTitle(QtGui.QApplication.translate("TabWidgetSearch", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("TabWidgetSearch", "Utterances:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("TabWidgetSearch", "Words:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("TabWidgetSearch", "Morphemes:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("TabWidgetSearch", "Glosses:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("TabWidgetSearch", "Translations:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("TabWidgetSearch", "Search Options", None, QtGui.QApplication.UnicodeUTF8))
        self.radiobuttonAnd.setText(QtGui.QApplication.translate("TabWidgetSearch", "AND", None, QtGui.QApplication.UnicodeUTF8))
        self.radiobuttonOr.setText(QtGui.QApplication.translate("TabWidgetSearch", "OR", None, QtGui.QApplication.UnicodeUTF8))
        self.checkboxInvert.setText(QtGui.QApplication.translate("TabWidgetSearch", "NOT", None, QtGui.QApplication.UnicodeUTF8))
        self.checkboxContained.setText(QtGui.QApplication.translate("TabWidgetSearch", "contained matches", None, QtGui.QApplication.UnicodeUTF8))

