# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainAnalyzerHTML.ui'
#
# Created: Mon Aug 20 14:09:37 2012
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
        MainWindow.resize(800, 600)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineeditQuickSearch = QtGui.QLineEdit(self.centralWidget)
        self.lineeditQuickSearch.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineeditQuickSearch.sizePolicy().hasHeightForWidth())
        self.lineeditQuickSearch.setSizePolicy(sizePolicy)
        self.lineeditQuickSearch.setObjectName(_fromUtf8("lineeditQuickSearch"))
        self.gridLayout.addWidget(self.lineeditQuickSearch, 14, 4, 1, 2)
        self.label_7 = QtGui.QLabel(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setSizeIncrement(QtCore.QSize(1, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 12, 1, 1, 2)
        self.line = QtGui.QFrame(self.centralWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 11, 1, 1, 5)
        self.buttonRemoveFiles = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonRemoveFiles.sizePolicy().hasHeightForWidth())
        self.buttonRemoveFiles.setSizePolicy(sizePolicy)
        self.buttonRemoveFiles.setObjectName(_fromUtf8("buttonRemoveFiles"))
        self.gridLayout.addWidget(self.buttonRemoveFiles, 14, 2, 1, 1)
        self.listFiles = QtGui.QListView(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listFiles.sizePolicy().hasHeightForWidth())
        self.listFiles.setSizePolicy(sizePolicy)
        self.listFiles.setSizeIncrement(QtCore.QSize(1, 0))
        self.listFiles.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listFiles.setObjectName(_fromUtf8("listFiles"))
        self.gridLayout.addWidget(self.listFiles, 13, 1, 1, 2)
        self.buttonSearch = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonSearch.sizePolicy().hasHeightForWidth())
        self.buttonSearch.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.buttonSearch.setFont(font)
        self.buttonSearch.setObjectName(_fromUtf8("buttonSearch"))
        self.gridLayout.addWidget(self.buttonSearch, 3, 4, 1, 2)
        self.tabWidget = QtGui.QTabWidget(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabNewSearch = QtGui.QWidget()
        self.tabNewSearch.setObjectName(_fromUtf8("tabNewSearch"))
        self.tabWidget.addTab(self.tabNewSearch, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 2, 1, 1, 5)
        self.buttonClearThisSearch = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonClearThisSearch.sizePolicy().hasHeightForWidth())
        self.buttonClearThisSearch.setSizePolicy(sizePolicy)
        self.buttonClearThisSearch.setObjectName(_fromUtf8("buttonClearThisSearch"))
        self.gridLayout.addWidget(self.buttonClearThisSearch, 3, 1, 1, 1)
        self.buttonCloseThisSearch = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonCloseThisSearch.sizePolicy().hasHeightForWidth())
        self.buttonCloseThisSearch.setSizePolicy(sizePolicy)
        self.buttonCloseThisSearch.setObjectName(_fromUtf8("buttonCloseThisSearch"))
        self.gridLayout.addWidget(self.buttonCloseThisSearch, 3, 2, 1, 1)
        self.buttonSaveSearches = QtGui.QPushButton(self.centralWidget)
        self.buttonSaveSearches.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonSaveSearches.sizePolicy().hasHeightForWidth())
        self.buttonSaveSearches.setSizePolicy(sizePolicy)
        self.buttonSaveSearches.setObjectName(_fromUtf8("buttonSaveSearches"))
        self.gridLayout.addWidget(self.buttonSaveSearches, 3, 3, 1, 1)
        self.label_8 = QtGui.QLabel(self.centralWidget)
        self.label_8.setSizeIncrement(QtCore.QSize(2, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 12, 3, 1, 1)
        self.label_9 = QtGui.QLabel(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 14, 3, 1, 1)
        self.buttonAddFiles = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonAddFiles.sizePolicy().hasHeightForWidth())
        self.buttonAddFiles.setSizePolicy(sizePolicy)
        self.buttonAddFiles.setObjectName(_fromUtf8("buttonAddFiles"))
        self.gridLayout.addWidget(self.buttonAddFiles, 14, 1, 1, 1)
        self.webviewResult = QtWebKit.QWebView(self.centralWidget)
        self.webviewResult.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webviewResult.setObjectName(_fromUtf8("webviewResult"))
        self.gridLayout.addWidget(self.webviewResult, 13, 3, 1, 3)
        self.horizontalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFiel = QtGui.QMenu(self.menuBar)
        self.menuFiel.setObjectName(_fromUtf8("menuFiel"))
        self.menuEdit = QtGui.QMenu(self.menuBar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuAbout = QtGui.QMenu(self.menuBar)
        self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
        self.menuView = QtGui.QMenu(self.menuBar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        MainWindow.setMenuBar(self.menuBar)
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionNewProject = QtGui.QAction(MainWindow)
        self.actionNewProject.setEnabled(False)
        self.actionNewProject.setObjectName(_fromUtf8("actionNewProject"))
        self.actionSaveProject = QtGui.QAction(MainWindow)
        self.actionSaveProject.setEnabled(False)
        self.actionSaveProject.setObjectName(_fromUtf8("actionSaveProject"))
        self.actionSaveProjectAs = QtGui.QAction(MainWindow)
        self.actionSaveProjectAs.setEnabled(False)
        self.actionSaveProjectAs.setObjectName(_fromUtf8("actionSaveProjectAs"))
        self.actionEditWordClasses = QtGui.QAction(MainWindow)
        self.actionEditWordClasses.setEnabled(False)
        self.actionEditWordClasses.setObjectName(_fromUtf8("actionEditWordClasses"))
        self.actionSearches = QtGui.QAction(MainWindow)
        self.actionSearches.setEnabled(False)
        self.actionSearches.setObjectName(_fromUtf8("actionSearches"))
        self.actionAboutPoioAnalyzer = QtGui.QAction(MainWindow)
        self.actionAboutPoioAnalyzer.setObjectName(_fromUtf8("actionAboutPoioAnalyzer"))
        self.actionQuickSearch = QtGui.QAction(MainWindow)
        self.actionQuickSearch.setEnabled(False)
        self.actionQuickSearch.setObjectName(_fromUtf8("actionQuickSearch"))
        self.actionExportSearchResult = QtGui.QAction(MainWindow)
        self.actionExportSearchResult.setObjectName(_fromUtf8("actionExportSearchResult"))
        self.actionZoom_In = QtGui.QAction(MainWindow)
        self.actionZoom_In.setObjectName(_fromUtf8("actionZoom_In"))
        self.actionZoom_Out = QtGui.QAction(MainWindow)
        self.actionZoom_Out.setObjectName(_fromUtf8("actionZoom_Out"))
        self.actionReset_Zoom = QtGui.QAction(MainWindow)
        self.actionReset_Zoom.setObjectName(_fromUtf8("actionReset_Zoom"))
        self.actionPrint = QtGui.QAction(MainWindow)
        self.actionPrint.setObjectName(_fromUtf8("actionPrint"))
        self.menuFiel.addAction(self.actionNewProject)
        self.menuFiel.addAction(self.actionSaveProject)
        self.menuFiel.addSeparator()
        self.menuFiel.addAction(self.actionPrint)
        self.menuFiel.addAction(self.actionExportSearchResult)
        self.menuFiel.addSeparator()
        self.menuFiel.addAction(self.actionSaveProjectAs)
        self.menuFiel.addAction(self.actionQuit)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionEditWordClasses)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionSearches)
        self.menuEdit.addAction(self.actionQuickSearch)
        self.menuAbout.addAction(self.actionAboutPoioAnalyzer)
        self.menuView.addAction(self.actionZoom_In)
        self.menuView.addAction(self.actionReset_Zoom)
        self.menuView.addAction(self.actionZoom_Out)
        self.menuBar.addAction(self.menuFiel.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())
        self.menuBar.addAction(self.menuView.menuAction())
        self.menuBar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.tabWidget, self.buttonClearThisSearch)
        MainWindow.setTabOrder(self.buttonClearThisSearch, self.buttonSearch)
        MainWindow.setTabOrder(self.buttonSearch, self.listFiles)
        MainWindow.setTabOrder(self.listFiles, self.buttonAddFiles)
        MainWindow.setTabOrder(self.buttonAddFiles, self.buttonRemoveFiles)
        MainWindow.setTabOrder(self.buttonRemoveFiles, self.lineeditQuickSearch)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "PoioAnalyzer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Files:", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonRemoveFiles.setText(QtGui.QApplication.translate("MainWindow", "Remove files", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonSearch.setText(QtGui.QApplication.translate("MainWindow", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabNewSearch), QtGui.QApplication.translate("MainWindow", "New Search...", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonClearThisSearch.setText(QtGui.QApplication.translate("MainWindow", "Clear This Search", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonCloseThisSearch.setText(QtGui.QApplication.translate("MainWindow", "Close This Search", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonSaveSearches.setText(QtGui.QApplication.translate("MainWindow", "Save Searches...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Result:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("MainWindow", "Quick Search:", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonAddFiles.setText(QtGui.QApplication.translate("MainWindow", "Add files...", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFiel.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAbout.setTitle(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setTitle(QtGui.QApplication.translate("MainWindow", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewProject.setText(QtGui.QApplication.translate("MainWindow", "New Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewProject.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveProject.setText(QtGui.QApplication.translate("MainWindow", "Save Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveProject.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveProjectAs.setText(QtGui.QApplication.translate("MainWindow", "Save Project As...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditWordClasses.setText(QtGui.QApplication.translate("MainWindow", "Edit Word Classes...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSearches.setText(QtGui.QApplication.translate("MainWindow", "Saved Searches...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAboutPoioAnalyzer.setText(QtGui.QApplication.translate("MainWindow", "About PoioAnalyzer...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuickSearch.setText(QtGui.QApplication.translate("MainWindow", "Quick Search", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuickSearch.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+F", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExportSearchResult.setText(QtGui.QApplication.translate("MainWindow", "Export Search Result...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExportSearchResult.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+E", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoom_In.setText(QtGui.QApplication.translate("MainWindow", "Zoom In", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoom_In.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl++", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoom_Out.setText(QtGui.QApplication.translate("MainWindow", "Zoom Out", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoom_Out.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+-", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReset_Zoom.setText(QtGui.QApplication.translate("MainWindow", "Reset Zoom", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReset_Zoom.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+0", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPrint.setText(QtGui.QApplication.translate("MainWindow", "Print", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPrint.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+P", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
import poioanalyzer_rc
