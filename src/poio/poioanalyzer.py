# -*- coding: utf-8 -*-
# (C) 2009 copyright by Peter Bouda

import sys, os.path, re
import time
from PyQt4 import QtCore, QtGui

from pyannotation.toolbox.data import ToolboxAnnotationFileObject
from pyannotation.elan.data import EafAnnotationFileObject
from pyannotation.data import AnnotationTree, AnnotationTreeFilter
import pyannotation.data

from pyannotation.corpusreader import GlossCorpusReader

from poio.ui.Ui_MainAnalyzer import Ui_MainWindow
from poio.ui.PoioIlTextEdit import PoioIlTextEdit

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
        self.currentFilter = AnnotationTreeFilter()
        
    def initCorpusReader(self):
        self.corpusreader = GlossCorpusReader(utterancetierTypes = self.arrUtteranceTierTypes,
                                              wordtierTypes = self.arrWordTierTypes,
                                              translationtierTypes = self.arrTranslationTierTypes,
                                              morphemetierTypes = self.arrMorphemeTierTypes,
                                              glosstierTypes = self.arrGlossTierTypes)

    def updateCorpusReaderFilter(self):
        self.currentFilter.resetMatchObject()
        for [filepath, annotationtree] in self.corpusreader.annotationtrees:
            annotationtree.updateLastFilter(self.currentFilter)
        
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
        self.updateCorpusReaderFilter()
        
    def initConnects(self):
        QtCore.QObject.connect(self.ui.buttonAddFiles, QtCore.SIGNAL("pressed()"), self.addFiles)
        QtCore.QObject.connect(self.ui.buttonRemoveFiles, QtCore.SIGNAL("pressed()"), self.removeFiles)
        
        # Filter and Search
        QtCore.QObject.connect(self.ui.buttonSearch, QtCore.SIGNAL("pressed()"), self.applyFilter)
        QtCore.QObject.connect(self.ui.lineeditSearchUtterances, QtCore.SIGNAL("returnPressed()"), self.applyFilter)
        QtCore.QObject.connect(self.ui.lineeditSearchWords, QtCore.SIGNAL("returnPressed()"), self.applyFilter)
        QtCore.QObject.connect(self.ui.lineeditSearchMorphemes, QtCore.SIGNAL("returnPressed()"), self.applyFilter)
        QtCore.QObject.connect(self.ui.lineeditSearchGlosses, QtCore.SIGNAL("returnPressed()"), self.applyFilter)
        QtCore.QObject.connect(self.ui.lineeditSearchTranslations, QtCore.SIGNAL("returnPressed()"), self.applyFilter)
        
        # Quick Search
        QtCore.QObject.connect(self.ui.actionQuickSearch, QtCore.SIGNAL("triggered()"), self.ui.lineeditQuickSearch.setFocus)
        QtCore.QObject.connect(self.ui.lineeditQuickSearch, QtCore.SIGNAL("textChanged(const QString &)"), self.findFromStart)
        QtCore.QObject.connect(self.ui.lineeditQuickSearch, QtCore.SIGNAL("returnPressed()"), self.findNext)

    def initSettings(self):
        QtCore.QCoreApplication.setOrganizationName("Interdisciplinary Centre for Social and Language Documentation");
        QtCore.QCoreApplication.setOrganizationDomain("cidles.eu");
        QtCore.QCoreApplication.setApplicationName("PoioAnalyzer");
        settings = QtCore.QSettings()
        self.strMorphemeSeperator = unicode(settings.value("Ann/MorphSep", QtCore.QVariant("-")).toString())
        self.strGlossSepereator = unicode(settings.value("Ann/GlossSep",  QtCore.QVariant(":")).toString())
        self.strEmptyCharacter = unicode(settings.value("Ann/EmptyChar",  QtCore.QVariant("#")).toString())
        self.arrUtteranceTierTypes = unicode(settings.value("Ann/UttTierTypeRefs",  QtCore.QVariant(u"utterance|utterances|Äußerung|Äußerungen")).toString()).split("|")
        self.arrWordTierTypes = unicode(settings.value("Ann/WordTierTypeRefs",  QtCore.QVariant(u"words|word|Wort|Worte|Wörter")).toString()).split("|")
        self.arrMorphemeTierTypes = unicode(settings.value("Ann/MorphTierTypeRefs",  QtCore.QVariant(u"morpheme|morphemes|Morphem|Morpheme")).toString()).split("|")
        self.arrGlossTierTypes = unicode(settings.value("Ann/GlossTierTypeRefs",  QtCore.QVariant(u"glosses|gloss|Glossen|Gloss|Glosse")).toString()).split("|")
        self.arrTranslationTierTypes = unicode(settings.value("Ann/TransTierTypeRefs",  QtCore.QVariant(u"translation|translations|Übersetzung|Übersetzungen")).toString()).split("|")

    def removeFiles(self):
        pass

    def addFiles(self):
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
        self.ui.texteditInterlinear.clear()
        itemsCount = self.project.rowCount()
        for [filepath, annotationtree] in self.corpusreader.annotationtrees:
            self.ui.texteditInterlinear.appendTitle(os.path.basename(filepath))
            utterancesIds = annotationtree.getFilteredUtteranceIds()
            for id in utterancesIds:
                utterance = annotationtree.getUtteranceById(id)
                if id in self.currentFilter.matchobject["utterance"]:
                    offset = 0
                    for g in self.currentFilter.matchobject["utterance"][id]:
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
                        if t[0] in self.currentFilter.matchobject["translation"]:
                            offset = 0
                            new_t = t[1]
                            for g in self.currentFilter.matchobject["translation"][t[0]]:
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
                    if wid in self.currentFilter.matchobject["word"]:
                        markWord = True
                    ilElements.append([wid, strWord, strMorphemes, strGlosses, markWord])

                self.ui.texteditInterlinear.appendUtterance(id,  utterance, ilElements, translations)
            

        self.ui.texteditInterlinear.setReadOnly(True)
        self.ui.texteditInterlinear.scrollToAnchor("#")

    def findFromStart(self, exp):
        self.ui.texteditInterlinear.setTextCursor(QtGui.QTextCursor(self.ui.texteditInterlinear.document()))
        if not self.ui.texteditInterlinear.find(exp) and exp != "":
            self.statusBar().showMessage(self.tr("No match found."), 2000)
        
    def findNext(self):
        found = self.ui.texteditInterlinear.find(self.ui.lineeditQuickSearch.text())
        if not found:
            self.statusBar().showMessage(self.tr("Restarting search from beginning of document."), 2000)
            found = self.findFromStart(self.ui.lineeditQuickSearch.text())
        return found
    
    def applyFilter(self):
        self.currentFilter.setUtteranceFilter(unicode(self.ui.lineeditSearchUtterances.text()))
        self.currentFilter.setTranslationFilter(unicode(self.ui.lineeditSearchTranslations.text()))
        self.currentFilter.setWordFilter(unicode(self.ui.lineeditSearchWords.text()))
        self.currentFilter.setMorphemeFilter(unicode(self.ui.lineeditSearchMorphemes.text()))
        self.currentFilter.setGlossFilter(unicode(self.ui.lineeditSearchGlosses.text()))
        
        self.currentFilter.setInvertedFilter(self.ui.checkboxInvert.isChecked())
        self.currentFilter.setContainedMatches(self.ui.checkboxContained.isChecked())
        
        if self.ui.radiobuttonAnd.isChecked():
            self.currentFilter.setBooleanOperation(AnnotationTreeFilter.AND)
        elif self.ui.radiobuttonOr.isChecked():
            self.currentFilter.setBooleanOperation(AnnotationTreeFilter.OR)

        self.updateCorpusReaderFilter()
        self.updateIlTextEdit()