# -*- coding: utf-8 -*-
# (C) 2009 copyright by Peter Bouda

import sys, os.path, re, copy
import time
from PyQt4 import QtCore, QtGui
from PyQt4.QtDeclarative import QDeclarativeView

from pyannotation.toolbox.data import ToolboxAnnotationFileObject
from pyannotation.elan.data import EafAnnotationFileObject
from pyannotation.data import AnnotationTree, AnnotationTreeFilter
import pyannotation.data

from pyannotation.corpusreader import GlossCorpusReader

from poio.ui.Ui_MainAnalyzerQML import Ui_MainWindow
#from poio.ui.PoioIlTextEdit import PoioIlTextEdit
from poio.ui.Ui_TabWidgetSearch import Ui_TabWidgetSearch

from poio.poioproject import PoioProject


class PoioAnalyzer(QtGui.QMainWindow):
    """The main window of the PoioAnalyzer application."""

    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.initConnects()
        self.initSettings()
        self.project = PoioProject(os.getcwd())
        self.ui.listFiles.setModel(self.project)
        self.initCorpusReader()
        
        # init DeclarativeView
        self.ui.declarativeviewResult.setResizeMode(QDeclarativeView.SizeRootObjectToView)
        context = self.ui.declarativeviewResult.rootContext()
        context.setContextProperty("resultModel", [])

        self.ui.declarativeviewResult.setSource(QtCore.QUrl.fromLocalFile("qml/PoioIlView.qml"))

        self.addSearchTab()
        
    def initCorpusReader(self):
        self.corpusreader = GlossCorpusReader(utterancetierTypes = self.arrUtteranceTierTypes,
                                              wordtierTypes = self.arrWordTierTypes,
                                              translationtierTypes = self.arrTranslationTierTypes,
                                              morphemetierTypes = self.arrMorphemeTierTypes,
                                              glosstierTypes = self.arrGlossTierTypes)
        
    def updateCorpusReader(self):
        itemsCount = self.project.rowCount()
        progress = QtGui.QProgressDialog(self.tr("Loading Files..."), self.tr("Abort"), 0, itemsCount, self.parent())
        progress.setWindowModality(QtCore.Qt.WindowModal)
        for i in range(itemsCount):
            progress.setValue(i)
            poiofile = self.project.poioFileAt(i)
            if poiofile.isNew:
                self.corpusreader.addFile(poiofile.filepath, poiofile.type)
                poiofile.setIsNew(False)
            if (progress.wasCanceled()):
                initCorpusReader()
                break
        progress.setValue(itemsCount)
        #self.updateCorpusReaderFilter()
        
    def initConnects(self):
        QtCore.QObject.connect(self.ui.buttonAddFiles, QtCore.SIGNAL("pressed()"), self.addFiles)
        QtCore.QObject.connect(self.ui.buttonRemoveFiles, QtCore.SIGNAL("pressed()"), self.removeFiles)
        
        # Filter and Search
        QtCore.QObject.connect(self.ui.buttonSearch, QtCore.SIGNAL("pressed()"), self.applyFilter)
        QtCore.QObject.connect(self.ui.buttonCloseThisSearch, QtCore.SIGNAL("pressed()"), self.searchTabClosed)
        QtCore.QObject.connect(self.ui.tabWidget, QtCore.SIGNAL("currentChanged(int)"), self.searchTabChanged)
        
        #QtCore.QObject.connect(self.ui.lineeditSearchUtterances, QtCore.SIGNAL("returnPressed()"), self.applyFilter)
        #QtCore.QObject.connect(self.ui.lineeditSearchWords, QtCore.SIGNAL("returnPressed()"), self.applyFilter)
        #QtCore.QObject.connect(self.ui.lineeditSearchMorphemes, QtCore.SIGNAL("returnPressed()"), self.applyFilter)
        #QtCore.QObject.connect(self.ui.lineeditSearchGlosses, QtCore.SIGNAL("returnPressed()"), self.applyFilter)
        #QtCore.QObject.connect(self.ui.lineeditSearchTranslations, QtCore.SIGNAL("returnPressed()"), self.applyFilter)
        
        # Quick Search
        #QtCore.QObject.connect(self.ui.actionQuickSearch, QtCore.SIGNAL("triggered()"), self.ui.lineeditQuickSearch.setFocus)
        #QtCore.QObject.connect(self.ui.lineeditQuickSearch, QtCore.SIGNAL("textChanged(const QString &)"), self.findFromStart)
        #QtCore.QObject.connect(self.ui.lineeditQuickSearch, QtCore.SIGNAL("returnPressed()"), self.findNext)

    def initSettings(self):
        QtCore.QCoreApplication.setOrganizationName("Interdisciplinary Centre for Social and Language Documentation");
        QtCore.QCoreApplication.setOrganizationDomain("cidles.eu");
        QtCore.QCoreApplication.setApplicationName("PoioAnalyzer");
        settings = QtCore.QSettings()
        self.strMorphemeSeperator = unicode(settings.value("Ann/MorphSep", "-"))
        self.strGlossSepereator = unicode(settings.value("Ann/GlossSep",  ":"))
        self.strEmptyCharacter = unicode(settings.value("Ann/EmptyChar",  "#"))
        self.arrUtteranceTierTypes = unicode(settings.value("Ann/UttTierTypeRefs", u"utterance|utterances|Äußerung|Äußerungen")).split("|")
        self.arrWordTierTypes = unicode(settings.value("Ann/WordTierTypeRefs", u"words|word|Wort|Worte|Wörter")).split("|")
        self.arrMorphemeTierTypes = unicode(settings.value("Ann/MorphTierTypeRefs", u"morpheme|morphemes|Morphem|Morpheme")).split("|")
        self.arrGlossTierTypes = unicode(settings.value("Ann/GlossTierTypeRefs",  u"glosses|gloss|Glossen|Gloss|Glosse")).split("|")
        self.arrTranslationTierTypes = unicode(settings.value("Ann/TransTierTypeRefs", u"translation|translations|Übersetzung|Übersetzungen")).split("|")

    def removeFiles(self):
        pass

    def addFiles(self):
        # PySide version
        #filepaths, types = QtGui.QFileDialog.getOpenFileNames(self, self.tr("Add Files"), "", self.tr("Elan files (*.eaf);;Toolbox files (*.txt);;All files (*.*)"))
        # PyQt version
        filepaths = QtGui.QFileDialog.getOpenFileNames(self, self.tr("Add Files"), "", self.tr("Elan files (*.eaf);;Toolbox files (*.txt);;All files (*.*)"))
        self.project.addFilePaths(filepaths)
        start = time.time()
        self.updateCorpusReader()
        end = time.time()
        print "Time elapsed = ", end - start, "seconds"
        start = time.time()
        self.updateIlTextEdit()
        end = time.time()
        print "Time elapsed = ", end - start, "seconds"

    def updateIlTextEdit(self):
        itemsCount = self.project.rowCount()
        files = []
        for [filepath, annotationtree] in self.corpusreader.annotationtrees:
            utterancesIds = annotationtree.getFilteredUtteranceIds()
            filter = annotationtree.lastFilter()
            utterances = []
            for id in utterancesIds:
                utterance = annotationtree.getUtteranceById(id)
                if id in filter.matchobject["utterance"]:
                    offset = 0
                    for g in filter.matchobject["utterance"][id]:
                        utterance = utterance[:g[0]+offset] + "<span style=\"color:green;\">" + utterance[g[0]+offset:]
                        offset = offset + len("<span style=\"color:green;\">")
                        utterance = utterance[:g[1]+offset] + "</span>" + utterance[g[1]+offset:]
                        offset = offset + len("</span>")
                translations = annotationtree.getTranslationsForUtterance(id)
                if len(translations) == 0:
                    translationId = annotationtree.newTranslationForUtteranceId(id, "")
                    translations = [ [translationId, self.strEmptyCharacter] ]
                else:
                    new_translations = []
                    for t in translations:
                        if t[1] == "":
                            new_t = self.strEmptyCharacter
                            new_translations.append = [t[0], new_t]
                        if t[0] in filter.matchobject["translation"]:
                            offset = 0
                            new_t = t[1]
                            for g in filter.matchobject["translation"][t[0]]:
                                new_t = new_t[:g[0]+offset] + "<span style=\"color:green;\">" + new_t[g[0]+offset:]
                                offset = offset + len("<span style=\"color:green;\">")
                                new_t = new_t[:g[1]+offset] + "</span>" + new_t[g[1]+offset:]
                                offset = offset + len("</span>")
                            new_translations.append([t[0], new_t])
                        else:
                            new_translations.append([t[0], t[1]])
                        translations = new_translations
                wordIds = annotationtree.getWordIdsForUtterance(id)
                ilElements = []
                for wid in wordIds:
                    strWord = annotationtree.getWordById(wid)
                    if strWord == "":
                        strWord = self.strEmptyCharacter
                    strMorphemes = annotationtree.getMorphemeStringForWord(wid)
                    if strMorphemes == "":
                        strMorphemes = strWord
                    strGlosses = annotationtree.getGlossStringForWord(wid)
                    if strGlosses == "":
                        strGlosses = self.strEmptyCharacter

                    markWord = False
                    if wid in filter.matchobject["word"]:
                        markWord = True
                    ilElements.append([wid, strWord, strMorphemes, strGlosses, markWord])
                    
                utterances.append({ "id" : id,  "utterance" : utterance, "ilElements" : ilElements, "translations" : translations })
            if utterances == []:
                utterances = None
            files.append({ "filename" : os.path.basename(filepath), "utterances" : utterances})
        context = self.ui.declarativeviewResult.rootContext()
        context.setContextProperty("resultModel", files)
        #print utterances
        #self.ui.texteditInterlinear.scrollToAnchor("#")

    #def findFromStart(self, exp):
    #    self.ui.texteditInterlinear.setTextCursor(QtGui.QTextCursor(self.ui.texteditInterlinear.document()))
    #    if not self.ui.texteditInterlinear.find(exp) and exp != "":
    #        self.statusBar().showMessage(self.tr("No match found."), 2000)
        
    #def findNext(self):
    #    found = self.ui.texteditInterlinear.find(self.ui.lineeditQuickSearch.text())
    #    if not found:
    #        self.statusBar().showMessage(self.tr("Restarting search from beginning of document."), 2000)
    #        found = self.findFromStart(self.ui.lineeditQuickSearch.text())
    #    return found
    
    def applyFilter(self):
        filterChain = []
        for i in range(0, self.ui.tabWidget.currentIndex()+1):
            currentFilter = AnnotationTreeFilter()
            inputfield = self.ui.tabWidget.findChild(QtGui.QLineEdit, "lineeditSearchUtterances_%i"%(i+1))
            currentFilter.setUtteranceFilter(unicode(inputfield.text()))
            inputfield = self.ui.tabWidget.findChild(QtGui.QLineEdit, "lineeditSearchTranslations_%i"%(i+1))
            currentFilter.setTranslationFilter(unicode(inputfield.text()))
            inputfield = self.ui.tabWidget.findChild(QtGui.QLineEdit, "lineeditSearchWords_%i"%(i+1))
            currentFilter.setWordFilter(unicode(inputfield.text()))
            inputfield = self.ui.tabWidget.findChild(QtGui.QLineEdit, "lineeditSearchMorphemes_%i"%(i+1))
            currentFilter.setMorphemeFilter(unicode(inputfield.text()))
            inputfield = self.ui.tabWidget.findChild(QtGui.QLineEdit, "lineeditSearchGlosses_%i"%(i+1))
            currentFilter.setGlossFilter(unicode(inputfield.text()))
            
            checkbox = self.ui.tabWidget.findChild(QtGui.QCheckBox, "checkboxInvert_%i"%(i+1))
            currentFilter.setInvertedFilter(checkbox.isChecked())
            checkbox = self.ui.tabWidget.findChild(QtGui.QCheckBox, "checkboxContained_%i"%(i+1))
            currentFilter.setContainedMatches(checkbox.isChecked())
            
            radiobuttonAnd = self.ui.tabWidget.findChild(QtGui.QRadioButton, "radiobuttonAnd_%i"%(i+1))
            radiobuttonOr = self.ui.tabWidget.findChild(QtGui.QRadioButton, "radiobuttonOr_%i"%(i+1))
            if radiobuttonAnd.isChecked():
                currentFilter.setBooleanOperation(AnnotationTreeFilter.AND)
            elif radiobuttonOr.isChecked():
                currentFilter.setBooleanOperation(AnnotationTreeFilter.OR)
            filterChain.append(currentFilter)
    
        for [filepath, annotationtree] in self.corpusreader.annotationtrees:
            annotationtree.clearFilters()
            for filter in filterChain:
                annotationtree.appendFilter(copy.deepcopy(filter))

        #self.updateCorpusReaderFilter()
        self.updateIlTextEdit()
        
    def searchTabChanged(self, index):
        if index == self.ui.tabWidget.count() - 1:
            self.addSearchTab()
        else:
            self.applyFilter()
        
    def addSearchTab(self):
        nrOfNewTab = self.ui.tabWidget.count()
        widgetSearch = QtGui.QWidget()
        ui = Ui_TabWidgetSearch()
        ui.setupUi(widgetSearch)
        widgetSearch.setObjectName("%s_%i" % (widgetSearch.objectName(), nrOfNewTab))
        for childWidget in widgetSearch.findChildren(QtGui.QWidget):
            if re.match(u"lineeditSearch", childWidget.objectName()):
                QtCore.QObject.connect(childWidget, QtCore.SIGNAL("returnPressed()"), self.applyFilter)
            childWidget.setObjectName("%s_%i" % (childWidget.objectName(), nrOfNewTab))
        self.ui.tabWidget.insertTab(nrOfNewTab - 1, widgetSearch, "Search %i" % nrOfNewTab)
        self.ui.tabWidget.setCurrentIndex(nrOfNewTab - 1)    
        
    def searchTabClosed(self):
        # always leave at least one Search tab open
        if self.ui.tabWidget.indexOf(self.ui.tabNewSearch) < 2:
            return
        currentIndex = self.ui.tabWidget.currentIndex()
        print currentIndex
        widgetSearch = self.ui.tabWidget.currentWidget()
        self.ui.tabWidget.removeTab(currentIndex)
        widgetSearch.close()
        widgetSearch.deleteLater()
        del widgetSearch
        self.ui.tabWidget.update()
        print "removed"
