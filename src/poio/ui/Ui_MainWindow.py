# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Wed Aug 22 09:40:33 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(977, 747)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayoutMain = QtGui.QVBoxLayout()
        self.verticalLayoutMain.setObjectName(_fromUtf8("verticalLayoutMain"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayoutUtterances = QtGui.QVBoxLayout()
        self.verticalLayoutUtterances.setObjectName(_fromUtf8("verticalLayoutUtterances"))
        self.labelUtterances = QtGui.QLabel(self.centralWidget)
        self.labelUtterances.setObjectName(_fromUtf8("labelUtterances"))
        self.verticalLayoutUtterances.addWidget(self.labelUtterances)
        self.listwidgetUtterances = QtGui.QListWidget(self.centralWidget)
        self.listwidgetUtterances.setMaximumSize(QtCore.QSize(16777215, 150))
        self.listwidgetUtterances.setObjectName(_fromUtf8("listwidgetUtterances"))
        self.verticalLayoutUtterances.addWidget(self.listwidgetUtterances)
        self.pushbuttonNewTierUtterances = QtGui.QPushButton(self.centralWidget)
        self.pushbuttonNewTierUtterances.setObjectName(_fromUtf8("pushbuttonNewTierUtterances"))
        self.verticalLayoutUtterances.addWidget(self.pushbuttonNewTierUtterances)
        self.horizontalLayout.addLayout(self.verticalLayoutUtterances)
        self.verticalLayoutWords = QtGui.QVBoxLayout()
        self.verticalLayoutWords.setObjectName(_fromUtf8("verticalLayoutWords"))
        self.labelWords = QtGui.QLabel(self.centralWidget)
        self.labelWords.setObjectName(_fromUtf8("labelWords"))
        self.verticalLayoutWords.addWidget(self.labelWords)
        self.listwidgetWords = QtGui.QListWidget(self.centralWidget)
        self.listwidgetWords.setEnabled(True)
        self.listwidgetWords.setMaximumSize(QtCore.QSize(16777215, 150))
        self.listwidgetWords.setObjectName(_fromUtf8("listwidgetWords"))
        self.verticalLayoutWords.addWidget(self.listwidgetWords)
        self.pushbuttonNewTierWords = QtGui.QPushButton(self.centralWidget)
        self.pushbuttonNewTierWords.setObjectName(_fromUtf8("pushbuttonNewTierWords"))
        self.verticalLayoutWords.addWidget(self.pushbuttonNewTierWords)
        self.horizontalLayout.addLayout(self.verticalLayoutWords)
        self.verticalLayoutMorphemes = QtGui.QVBoxLayout()
        self.verticalLayoutMorphemes.setObjectName(_fromUtf8("verticalLayoutMorphemes"))
        self.labelMorphemes = QtGui.QLabel(self.centralWidget)
        self.labelMorphemes.setObjectName(_fromUtf8("labelMorphemes"))
        self.verticalLayoutMorphemes.addWidget(self.labelMorphemes)
        self.listwidgetMorphemes = QtGui.QListWidget(self.centralWidget)
        self.listwidgetMorphemes.setMaximumSize(QtCore.QSize(16777215, 150))
        self.listwidgetMorphemes.setBaseSize(QtCore.QSize(0, 0))
        self.listwidgetMorphemes.setObjectName(_fromUtf8("listwidgetMorphemes"))
        self.verticalLayoutMorphemes.addWidget(self.listwidgetMorphemes)
        self.pushbuttonNewTierMorphemes = QtGui.QPushButton(self.centralWidget)
        self.pushbuttonNewTierMorphemes.setObjectName(_fromUtf8("pushbuttonNewTierMorphemes"))
        self.verticalLayoutMorphemes.addWidget(self.pushbuttonNewTierMorphemes)
        self.horizontalLayout.addLayout(self.verticalLayoutMorphemes)
        self.verticalLayoutFunctions = QtGui.QVBoxLayout()
        self.verticalLayoutFunctions.setObjectName(_fromUtf8("verticalLayoutFunctions"))
        self.labelFunctions = QtGui.QLabel(self.centralWidget)
        self.labelFunctions.setObjectName(_fromUtf8("labelFunctions"))
        self.verticalLayoutFunctions.addWidget(self.labelFunctions)
        self.listwidgetFunctions = QtGui.QListWidget(self.centralWidget)
        self.listwidgetFunctions.setMaximumSize(QtCore.QSize(16777215, 150))
        self.listwidgetFunctions.setObjectName(_fromUtf8("listwidgetFunctions"))
        self.verticalLayoutFunctions.addWidget(self.listwidgetFunctions)
        self.pushbuttonNewTierFunctions = QtGui.QPushButton(self.centralWidget)
        self.pushbuttonNewTierFunctions.setObjectName(_fromUtf8("pushbuttonNewTierFunctions"))
        self.verticalLayoutFunctions.addWidget(self.pushbuttonNewTierFunctions)
        self.horizontalLayout.addLayout(self.verticalLayoutFunctions)
        self.verticalLayoutTranslations = QtGui.QVBoxLayout()
        self.verticalLayoutTranslations.setObjectName(_fromUtf8("verticalLayoutTranslations"))
        self.labelTranslations = QtGui.QLabel(self.centralWidget)
        self.labelTranslations.setObjectName(_fromUtf8("labelTranslations"))
        self.verticalLayoutTranslations.addWidget(self.labelTranslations)
        self.listwidgetTranslations = QtGui.QListWidget(self.centralWidget)
        self.listwidgetTranslations.setMaximumSize(QtCore.QSize(16777215, 150))
        self.listwidgetTranslations.setObjectName(_fromUtf8("listwidgetTranslations"))
        self.verticalLayoutTranslations.addWidget(self.listwidgetTranslations)
        self.pushbuttonNewTierTranslations = QtGui.QPushButton(self.centralWidget)
        self.pushbuttonNewTierTranslations.setObjectName(_fromUtf8("pushbuttonNewTierTranslations"))
        self.verticalLayoutTranslations.addWidget(self.pushbuttonNewTierTranslations)
        self.horizontalLayout.addLayout(self.verticalLayoutTranslations)
        self.verticalLayoutMain.addLayout(self.horizontalLayout)
        self.line = QtGui.QFrame(self.centralWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayoutMain.addWidget(self.line)
        self.horizontalLayoutEditArea = QtGui.QHBoxLayout()
        self.horizontalLayoutEditArea.setObjectName(_fromUtf8("horizontalLayoutEditArea"))
        self.verticalLayoutProjectFiles = QtGui.QVBoxLayout()
        self.verticalLayoutProjectFiles.setObjectName(_fromUtf8("verticalLayoutProjectFiles"))
        self.label_6 = QtGui.QLabel(self.centralWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayoutProjectFiles.addWidget(self.label_6)
        self.listwidgetFiles = QtGui.QListWidget(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listwidgetFiles.sizePolicy().hasHeightForWidth())
        self.listwidgetFiles.setSizePolicy(sizePolicy)
        self.listwidgetFiles.setObjectName(_fromUtf8("listwidgetFiles"))
        self.verticalLayoutProjectFiles.addWidget(self.listwidgetFiles)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.toolbuttonAddFile = QtGui.QToolButton(self.centralWidget)
        self.toolbuttonAddFile.setEnabled(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/pixmaps/fileopen.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolbuttonAddFile.setIcon(icon)
        self.toolbuttonAddFile.setAutoRaise(False)
        self.toolbuttonAddFile.setObjectName(_fromUtf8("toolbuttonAddFile"))
        self.horizontalLayout_4.addWidget(self.toolbuttonAddFile)
        self.toolbuttonNewFile = QtGui.QToolButton(self.centralWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/pixmaps/filenew.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolbuttonNewFile.setIcon(icon1)
        self.toolbuttonNewFile.setAutoRaise(False)
        self.toolbuttonNewFile.setObjectName(_fromUtf8("toolbuttonNewFile"))
        self.horizontalLayout_4.addWidget(self.toolbuttonNewFile)
        self.toolbuttonExportFile = QtGui.QToolButton(self.centralWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/pixmaps/fileexport.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolbuttonExportFile.setIcon(icon2)
        self.toolbuttonExportFile.setAutoRaise(False)
        self.toolbuttonExportFile.setObjectName(_fromUtf8("toolbuttonExportFile"))
        self.horizontalLayout_4.addWidget(self.toolbuttonExportFile)
        self.toolbuttonRemoveFile = QtGui.QToolButton(self.centralWidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/pixmaps/fileclose.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolbuttonRemoveFile.setIcon(icon3)
        self.toolbuttonRemoveFile.setAutoRaise(False)
        self.toolbuttonRemoveFile.setObjectName(_fromUtf8("toolbuttonRemoveFile"))
        self.horizontalLayout_4.addWidget(self.toolbuttonRemoveFile)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayoutProjectFiles.addLayout(self.horizontalLayout_4)
        self.horizontalLayoutEditArea.addLayout(self.verticalLayoutProjectFiles)
        self.texteditInterlinear = PoioIlTextEdit(self.centralWidget)
        self.texteditInterlinear.setObjectName(_fromUtf8("texteditInterlinear"))
        self.horizontalLayoutEditArea.addWidget(self.texteditInterlinear)
        self.verticalLayoutMain.addLayout(self.horizontalLayoutEditArea)
        self.verticalLayoutMain.setStretch(2, 1)
        self.verticalLayout.addLayout(self.verticalLayoutMain)
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 977, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuEdit = QtGui.QMenu(self.menuBar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuAbout = QtGui.QMenu(self.menuBar)
        self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
        MainWindow.setMenuBar(self.menuBar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionOpen = QtGui.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/pixmaps/projectopen.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon4)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/pixmaps/filesave.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon5)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSaveAs = QtGui.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/pixmaps/filesaveas.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSaveAs.setIcon(icon6)
        self.actionSaveAs.setObjectName(_fromUtf8("actionSaveAs"))
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionNew = QtGui.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/pixmaps/projectnew.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon7)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionDeleteUtterance = QtGui.QAction(MainWindow)
        self.actionDeleteUtterance.setEnabled(True)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/pixmaps/removeutterance.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDeleteUtterance.setIcon(icon8)
        self.actionDeleteUtterance.setObjectName(_fromUtf8("actionDeleteUtterance"))
        self.actionInsertUtterance = QtGui.QAction(MainWindow)
        self.actionInsertUtterance.setEnabled(True)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/pixmaps/insertutterance.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionInsertUtterance.setIcon(icon9)
        self.actionInsertUtterance.setObjectName(_fromUtf8("actionInsertUtterance"))
        self.actionCopyUtterance = QtGui.QAction(MainWindow)
        self.actionCopyUtterance.setObjectName(_fromUtf8("actionCopyUtterance"))
        self.actionInsertWord = QtGui.QAction(MainWindow)
        self.actionInsertWord.setEnabled(True)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/pixmaps/insertword.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionInsertWord.setIcon(icon10)
        self.actionInsertWord.setObjectName(_fromUtf8("actionInsertWord"))
        self.actionDeleteWord = QtGui.QAction(MainWindow)
        self.actionDeleteWord.setEnabled(True)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/pixmaps/removeword.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDeleteWord.setIcon(icon11)
        self.actionDeleteWord.setObjectName(_fromUtf8("actionDeleteWord"))
        self.actionAboutPoioILE = QtGui.QAction(MainWindow)
        self.actionAboutPoioILE.setObjectName(_fromUtf8("actionAboutPoioILE"))
        self.actionOptions = QtGui.QAction(MainWindow)
        self.actionOptions.setObjectName(_fromUtf8("actionOptions"))
        self.actionAddFile = QtGui.QAction(MainWindow)
        self.actionAddFile.setEnabled(True)
        self.actionAddFile.setIcon(icon)
        self.actionAddFile.setObjectName(_fromUtf8("actionAddFile"))
        self.actionExportFile = QtGui.QAction(MainWindow)
        self.actionExportFile.setEnabled(True)
        self.actionExportFile.setIcon(icon2)
        self.actionExportFile.setObjectName(_fromUtf8("actionExportFile"))
        self.actionRemoveFile = QtGui.QAction(MainWindow)
        self.actionRemoveFile.setEnabled(True)
        self.actionRemoveFile.setIcon(icon3)
        self.actionRemoveFile.setObjectName(_fromUtf8("actionRemoveFile"))
        self.actionNewFile = QtGui.QAction(MainWindow)
        self.actionNewFile.setEnabled(True)
        self.actionNewFile.setIcon(icon1)
        self.actionNewFile.setObjectName(_fromUtf8("actionNewFile"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionAddFile)
        self.menuFile.addAction(self.actionNewFile)
        self.menuFile.addAction(self.actionExportFile)
        self.menuFile.addAction(self.actionRemoveFile)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuEdit.addAction(self.actionCopyUtterance)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionInsertUtterance)
        self.menuEdit.addAction(self.actionDeleteUtterance)
        self.menuEdit.addAction(self.actionInsertWord)
        self.menuEdit.addAction(self.actionDeleteWord)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionOptions)
        self.menuAbout.addAction(self.actionAboutPoioILE)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())
        self.menuBar.addAction(self.menuAbout.menuAction())
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionInsertUtterance)
        self.toolBar.addAction(self.actionDeleteUtterance)
        self.toolBar.addAction(self.actionInsertWord)
        self.toolBar.addAction(self.actionDeleteWord)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "PoioILE", None, QtGui.QApplication.UnicodeUTF8))
        self.labelUtterances.setText(QtGui.QApplication.translate("MainWindow", "Utterance tiers", None, QtGui.QApplication.UnicodeUTF8))
        self.pushbuttonNewTierUtterances.setText(QtGui.QApplication.translate("MainWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.labelWords.setText(QtGui.QApplication.translate("MainWindow", "Word tiers", None, QtGui.QApplication.UnicodeUTF8))
        self.pushbuttonNewTierWords.setText(QtGui.QApplication.translate("MainWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.labelMorphemes.setText(QtGui.QApplication.translate("MainWindow", "Morpheme tiers", None, QtGui.QApplication.UnicodeUTF8))
        self.pushbuttonNewTierMorphemes.setText(QtGui.QApplication.translate("MainWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFunctions.setText(QtGui.QApplication.translate("MainWindow", "Gloss tiers", None, QtGui.QApplication.UnicodeUTF8))
        self.pushbuttonNewTierFunctions.setText(QtGui.QApplication.translate("MainWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTranslations.setText(QtGui.QApplication.translate("MainWindow", "Translation tiers", None, QtGui.QApplication.UnicodeUTF8))
        self.pushbuttonNewTierTranslations.setText(QtGui.QApplication.translate("MainWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Project Files:", None, QtGui.QApplication.UnicodeUTF8))
        self.toolbuttonAddFile.setToolTip(QtGui.QApplication.translate("MainWindow", "Add File...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolbuttonAddFile.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolbuttonNewFile.setToolTip(QtGui.QApplication.translate("MainWindow", "New File", None, QtGui.QApplication.UnicodeUTF8))
        self.toolbuttonNewFile.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolbuttonExportFile.setToolTip(QtGui.QApplication.translate("MainWindow", "Export File...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolbuttonExportFile.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolbuttonRemoveFile.setToolTip(QtGui.QApplication.translate("MainWindow", "Remove File", None, QtGui.QApplication.UnicodeUTF8))
        self.toolbuttonRemoveFile.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAbout.setTitle(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "Open Project...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "Save Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveAs.setText(QtGui.QApplication.translate("MainWindow", "Save File as...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveAs.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Alt+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setText(QtGui.QApplication.translate("MainWindow", "New Project...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setToolTip(QtGui.QApplication.translate("MainWindow", "Create a new annotation project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDeleteUtterance.setText(QtGui.QApplication.translate("MainWindow", "Delete utterance", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInsertUtterance.setText(QtGui.QApplication.translate("MainWindow", "Insert new utterance", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInsertUtterance.setToolTip(QtGui.QApplication.translate("MainWindow", "Insert new utterance", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopyUtterance.setText(QtGui.QApplication.translate("MainWindow", "Copy utterance", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopyUtterance.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+C", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInsertWord.setText(QtGui.QApplication.translate("MainWindow", "Insert new word", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDeleteWord.setText(QtGui.QApplication.translate("MainWindow", "Delete word", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAboutPoioILE.setText(QtGui.QApplication.translate("MainWindow", "About PoioILE...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOptions.setText(QtGui.QApplication.translate("MainWindow", "Options...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddFile.setText(QtGui.QApplication.translate("MainWindow", "Add File...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExportFile.setText(QtGui.QApplication.translate("MainWindow", "Export File...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRemoveFile.setText(QtGui.QApplication.translate("MainWindow", "Remove File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewFile.setText(QtGui.QApplication.translate("MainWindow", "New File..", None, QtGui.QApplication.UnicodeUTF8))

from PoioIlTextEdit import PoioIlTextEdit
import poio_rc
