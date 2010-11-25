# -*- coding: utf-8 -*-
# (C) 2009 copyright by Peter Bouda

import sys, os.path, re
from PyQt4 import QtCore, QtGui

from pyannotation.toolbox.data import ToolboxAnnotationFileObject
from pyannotation.elan.data import EafAnnotationFileObject
from pyannotation.data import AnnotationTree
import pyannotation.data

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
        
    def initConnects(self):
        QtCore.QObject.connect(self.ui.buttonAddFiles, QtCore.SIGNAL("pressed()"), self.addFiles)
        QtCore.QObject.connect(self.ui.buttonRemoveFiles, QtCore.SIGNAL("pressed()"), self.removeFiles)
        QtCore.QObject.connect(self.ui.actionQuickSearch, QtCore.SIGNAL("triggered()"), self.ui.lineeditQuickSearch.setFocus)
        QtCore.QObject.connect(self.ui.lineeditQuickSearch, QtCore.SIGNAL("textChanged(const QString &)"), self.find_from_start)
        QtCore.QObject.connect(self.ui.lineeditQuickSearch, QtCore.SIGNAL("returnPressed()"), self.find_next)

    def initSettings(self):
        QtCore.QCoreApplication.setOrganizationName("Interdisciplinary Centre for Social and Language Documentation");
        QtCore.QCoreApplication.setOrganizationDomain("cidles.eu");
        QtCore.QCoreApplication.setApplicationName("PoioAnalyzer");
        settings = QtCore.QSettings()
        self.strMorphemeSeperator = unicode(settings.value("Ann/MorphSep", QtCore.QVariant("-")).toString())
        self.strGlossSepereator = unicode(settings.value("Ann/GlossSep",  QtCore.QVariant(":")).toString())
        self.strEmptyCharacter = unicode(settings.value("Ann/EmptyChar",  QtCore.QVariant("#")).toString())

    def removeFiles(self):
        pass

    def addFiles(self):
        filepaths = QtGui.QFileDialog.getOpenFileNames(self, self.tr("Add Files"), "", self.tr("Elan files (*.eaf);;Toolbox files (*.txt);;All files (*.*)"))
        self.project.addFilePaths(filepaths)
        self.updateIlTextEdit()
            
    def openFile(self):
        filepath = QtGui.QFileDialog.getOpenFileName(self, self.tr("Open File"), "", self.tr("Elan files (*.eaf);;Toolbox files (*.txt);;All files (*.*)"))
        filepath = unicode(filepath)
        if filepath != '':
            self.init = 1
            self.annotationFileObject = ToolboxAnnotationFileObject(filepath)
            self.annotationFileTiers = self.annotationFileObject.createTierHandler()
            self.annotationFileParser = self.annotationFileObject.createParser()
            self.annotationTree = AnnotationTree(self.annotationFileParser)
            self.annotationTree.parse()
            #print self.annotationTree.tree
            self.utterancesIds = self.annotationTree.getUtteranceIdsInTier()
            self.updateIlTextEdit()

    def updateIlTextEdit(self):
        self.ui.texteditInterlinear.clear()
        #self.ui.texteditInterlinear.appendTitle(self.filename)
        idInScene = 1
        itemsCount = self.project.rowCount()
        progress = QtGui.QProgressDialog(self.tr("Loading Files..."), self.tr("Abort"), 0, itemsCount, self.parent())
        progress.setWindowModality(QtCore.Qt.WindowModal)
        for i in range(itemsCount):
            poiofile = self.project.poioFileAt(i)
            filepath = poiofile.filepath
            self.ui.texteditInterlinear.appendTitle(os.path.basename(filepath))
            if poiofile.type == pyannotation.data.EAF:
                self.annotationFileObject = EafAnnotationFileObject(filepath)
            elif poiofile.type == pyannotation.data.TOOLBOX:
                self.annotationFileObject = ToolboxAnnotationFileObject(filepath)
            self.annotationTierHandler = self.annotationFileObject.createTierHandler()
            self.annotationParser = self.annotationFileObject.createParser()
            self.annotationTree = AnnotationTree(self.annotationParser)
            self.initTierTypesFromSettings()
            self.annotationTree.parse()
            utterancesIds = self.annotationTree.getUtteranceIds()
            for id in utterancesIds:
                progress.setValue(idInScene - 1)
                utterance = self.annotationTree.getUtteranceById(id)
                translations = self.annotationTree.getTranslationsForUtterance(id)
                if len(translations) == 0:
                    translationId = self.annotationTree.newTranslationForUtteranceId(id, "")
                    translations = [ [translationId, self.strEmptyCharacter] ]
                else:
                    for t in translations:
                        if t[1] == "":
                            t[1] = self.strEmptyCharacter
                wordIds = self.annotationTree.getWordIdsForUtterance(id)
                ilElements = []
                for wid in wordIds:
                    strWord = self.annotationTree.getWordById(wid)
                    if strWord == "":
                        strWord = self.strEmptyCharacter
                    strMorphemes = self.annotationTree.getMorphemeStringForWord(wid)
                    if strMorphemes == "":
                        strMorphemes = strWord
                    strGlosses = self.annotationTree.getGlossStringForWord(wid)
                    if strGlosses == "":
                        strGlosses = self.strEmptyCharacter
                    ilElements.append([wid, strWord, strMorphemes, strGlosses])
                self.ui.texteditInterlinear.appendUtterance(id,  utterance, ilElements, translations)
            idInScene = idInScene + 1
            if (progress.wasCanceled()):
                self.graphicssceneIlText.clear()
                break
        progress.setValue(itemsCount)
        self.ui.texteditInterlinear.setReadOnly(True)

    def initTierTypesFromSettings(self):
            settings = QtCore.QSettings()
            arrUtteranceTierTypes = unicode(settings.value("Ann/UttTierTypeRefs",  QtCore.QVariant(u"utterance|utterances|Äußerung|Äußerungen")).toString()).split("|")
            arrWordTierTypes = unicode(settings.value("Ann/WordTierTypeRefs",  QtCore.QVariant(u"words|word|Wort|Worte|Wörter")).toString()).split("|")
            arrMorphemeTierTypes = unicode(settings.value("Ann/MorphTierTypeRefs",  QtCore.QVariant(u"morpheme|morphemes|Morphem|Morpheme")).toString()).split("|")
            arrGlossTierTypes = unicode(settings.value("Ann/GlossTierTypeRefs",  QtCore.QVariant(u"glosses|gloss|Glossen|Gloss|Glosse")).toString()).split("|")
            arrTranslationTierTypes = unicode(settings.value("Ann/TransTierTypeRefs",  QtCore.QVariant(u"translation|translations|Übersetzung|Übersetzungen")).toString()).split("|")
            self.annotationTierHandler.setUtterancetierType(arrUtteranceTierTypes)
            self.annotationTierHandler.setWordtierType(arrWordTierTypes)
            self.annotationTierHandler.setMorphemetierType(arrMorphemeTierTypes)
            self.annotationTierHandler.setGlosstierType(arrGlossTierTypes)
            self.annotationTierHandler.setTranslationtierType(arrTranslationTierTypes)

    def find_from_start(self, exp):
        self.ui.texteditInterlinear.setTextCursor(QtGui.QTextCursor(self.ui.texteditInterlinear.document()))
        if not self.ui.texteditInterlinear.find(exp) and exp != "":
            self.statusBar().showMessage(self.tr("No match found."), 2000)
        
    def find_next(self):
        found = self.ui.texteditInterlinear.find(self.ui.lineeditQuickSearch.text())
        if not found:
            self.statusBar().showMessage(self.tr("Restarting search from beginning of document."), 2000)
            found = self.find_from_start(self.ui.lineeditQuickSearch.text())
        return found
