# -*- coding: utf-8 -*-
# (C) 2009 copyright by Peter Bouda

import sys, os.path, re
from PyQt4 import QtCore, QtGui

from pyannotation.elan.data import EafAnnotationFileObject
from pyannotation.data import AnnotationTree

import poio
from poio.ui.PoioIlTextEdit import PoioIlTextEdit
from poio.ui.Ui_MainWindowGRAID import Ui_MainWindow
from poio.ui.DialogNewTier import DialogNewTier
from poio.poioproject import PoioProject

class PoioGRAID(QtGui.QMainWindow):
    """The main window of the PoioILE application."""

    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #self.ui.verticalLayoutMain.setStretch(2,1)
        self.initVars()
        self.initSettings()
        self.initConnects()
        #self.initSignals()
        #self.hideTiersWidgets()
        self.init = 0
        
    def initVars(self):
        self.eaf = None
        self.utterancesDict = []
        self.clearAllTierVars()
        self.filename = ''
        self.project = None

    def initSettings(self):
        QtCore.QCoreApplication.setOrganizationName("Interdisciplinary Centre for Social and Language Documentation");
        QtCore.QCoreApplication.setOrganizationDomain("cidles.eu");
        QtCore.QCoreApplication.setApplicationName("PoioGRAID");
        settings = QtCore.QSettings()
        self.strEmptyCharacter = unicode(settings.value("Ann/EmptyChar",  QtCore.QVariant("#")).toString())
        
    def initConnects(self):
        # Projects
        QtCore.QObject.connect(self.ui.actionNew, QtCore.SIGNAL("triggered()"), self.newProject)
        QtCore.QObject.connect(self.ui.actionOpen, QtCore.SIGNAL("triggered()"), self.openProject)
        #QtCore.QObject.connect(self.ui.actionSaveAs, QtCore.SIGNAL("triggered()"), self.saveProjectAs)
        QtCore.QObject.connect(self.ui.actionSave, QtCore.SIGNAL("triggered()"), self.saveProject)

        # Files
        QtCore.QObject.connect(self.ui.actionAddFile, QtCore.SIGNAL("triggered()"), self.addFile)
        self.ui.toolbuttonAddFile.setDefaultAction(self.ui.actionAddFile)
        QtCore.QObject.connect(self.ui.actionExportFile, QtCore.SIGNAL("triggered()"), self.exportFile)
        self.ui.toolbuttonExportFile.setDefaultAction(self.ui.actionExportFile)
        QtCore.QObject.connect(self.ui.actionNewFile, QtCore.SIGNAL("triggered()"), self.newFile)
        self.ui.toolbuttonNewFile.setDefaultAction(self.ui.actionNewFile)
        QtCore.QObject.connect(self.ui.actionRemoveFile, QtCore.SIGNAL("triggered()"), self.removeFile)
        self.ui.toolbuttonRemoveFile.setDefaultAction(self.ui.actionRemoveFile)

        QtCore.QObject.connect(self.ui.actionQuit, QtCore.SIGNAL("triggered()"), self.close)
        QtCore.QObject.connect(self.ui.actionAboutPoioILE, QtCore.SIGNAL("triggered()"), self.aboutDialog)
        QtCore.QObject.connect(self.ui.actionInsertUtterance, QtCore.SIGNAL("triggered()"), self.insertUtteranceAfterCurrent)
        QtCore.QObject.connect(self.ui.actionDeleteUtterance, QtCore.SIGNAL("triggered()"), self.deleteCurrentUtterance)
        QtCore.QObject.connect(self.ui.actionInsertWord, QtCore.SIGNAL("triggered()"), self.insertWordAfterCurrent)
        QtCore.QObject.connect(self.ui.actionDeleteWord, QtCore.SIGNAL("triggered()"), self.deleteCurrentWord)
        QtCore.QObject.connect(self.ui.listwidgetUtterances, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.setTierUtterances)
        QtCore.QObject.connect(self.ui.listwidgetWords, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.setTierWords)
        QtCore.QObject.connect(self.ui.listwidgetGRAID1, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.setTierGRAID1)
        QtCore.QObject.connect(self.ui.listwidgetGRAID2, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.setTierGRAID2)
        QtCore.QObject.connect(self.ui.listwidgetTranslations, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.setTierTranslations)
        QtCore.QObject.connect(self.ui.pushbuttonNewTierWfW, QtCore.SIGNAL("clicked()"), self.newTierWfW)
        QtCore.QObject.connect(self.ui.pushbuttonNewTierGRAID1, QtCore.SIGNAL("clicked()"), self.newTierGRAID1)
        QtCore.QObject.connect(self.ui.pushbuttonNewTierGRAID2, QtCore.SIGNAL("clicked()"), self.newTierGRAID2)
        QtCore.QObject.connect(self.ui.pushbuttonNewTierTranslations, QtCore.SIGNAL("clicked()"), self.newTierTranslations)

    def aboutDialog(self):
        about = QtGui.QMessageBox(self)
        about.setTextFormat(QtCore.Qt.RichText)
        about.setWindowTitle(self.tr("About PoioGRAID"))
        about.setText(self.tr("<b>PoioGRAID 0.1.0</b><br/>Poio GRAID Editor by the <a href=\"http://www.cidles.eu\">Interdisciplinary Centre for Social and Language Documentation</a>.<br/><br/>All rights reserved. See LICENSE file for details.<br/><br/>For more information visit the website:<br/><a href=\"http://www.cidles.eu/ltll/poio\">http://www.cidles.eu/poio/ltll</a>"))
        about.exec_()

    def lineeditValidate(self, input):
        a = input.split(" ")
        lg = 0
        lm = 0
        if len(a) > 1:
            lm = len(a[1].split("-"))
        if len(a) > 2:
            lg = len(a[2].split("-"))
        if lg == lm:
            return True
        else:
            return False

    def updateIlTextEdit(self):
        self.ui.texteditInterlinear.clear()
        self.ui.texteditInterlinear.appendTitle(self.filename)
        idInScene = 1
        progress = QtGui.QProgressDialog(self.tr("Loading Tiers..."), self.tr("Abort"), 0, len(self.utterancesIds), self.parent())
        progress.setWindowModality(QtCore.Qt.WindowModal)
        for id in self.utterancesIds:
            progress.setValue(idInScene - 1)
            utterance = self.eafTree.getUtteranceById(id)
            translations = self.eafTree.getTranslationsForUtterance(id)
            if len(translations) == 0:
                translationId = self.eafTree.newTranslationForUtteranceId(id, "")
                translations = [ [translationId, self.strEmptyCharacter] ]
            else:
                for t in translations:
                    if t[1] == "":
                        t[1] = self.strEmptyCharacter
            wordIds = self.eafTree.getWordIdsForUtterance(id)
            ilElements = []
            for wid in wordIds:
                strWord = self.eafTree.getWordById(wid)
                if strWord == "":
                    strWord = self.strEmptyCharacter
                strMorphemes = self.eafTree.getMorphemeStringForWord(wid)
                if strMorphemes == "":
                    strMorphemes = strWord
                strGlosses = self.eafTree.getGlossStringForWord(wid)
                if strGlosses == "":
                    strGlosses = self.strEmptyCharacter
                markWord = False
                ilElements.append([wid, strWord, strMorphemes, strGlosses, markWord])
            self.ui.texteditInterlinear.appendUtterance(id,  utterance, ilElements, translations)
            idInScene = idInScene + 1
            if (progress.wasCanceled()):
                self.graphicssceneIlText.clear()
                break
        progress.setValue(len(self.utterancesIds))
        self.ui.texteditInterlinear.scrollToAnchor("title")

    def deleteCurrentUtterance(self):
        self.updateEafTreeFromTexteditInterlinear()
        #utteranceId = self.ui.texteditInterlinear.deleteCurrentUtterance()
        utteranceId = self.ui.texteditInterlinear.getCurrentUtteranceId()
        if utteranceId == "":
            QtGui.QMessageBox.info(self, self.tr("No utterance selected"), self.tr("Please move the cursor to the utterace you want to delete."), QtGui.QMessageBox.Ok)
        else:
            self.eafTree.removeUtteranceWithId(utteranceId)
            self.utterancesIds.remove(utteranceId)
            self.updateIlTextEdit()
        
    def insertUtteranceAfterCurrent(self):
        pass

    def deleteCurrentWord(self):
        self.updateEafTreeFromTexteditInterlinear()
        wordId = self.ui.texteditInterlinear.getCurrentWordId()
        if wordId == "":
            QtGui.QMessageBox.information(self, self.tr("No word selected"), self.tr("Please move the cursor to the word you want to delete."), QtGui.QMessageBox.Ok)
        else:
            print wordId
            self.eafTree.removeWordWithId(wordId)
            self.updateIlTextEdit()
        
    def insertWordAfterCurrent(self):
        pass

    def clearAllTierLists(self):
        self.ui.listwidgetUtterances.clear()
        self.ui.listwidgetWords.clear()
        self.ui.listwidgetf.clear()
        self.ui.listwidgetGRAID1.clear()
        self.ui.listwidgetGRAID2.clear()
        self.ui.listwidgetTranslations.clear()

    def clearAllTierVars(self):
        self.tierWords = None
        self.tierUtterances = None
        self.tierWfW = None
        self.tierGRAID1 = None
        self.tierGRAID2 = None
        self.tierTranslations = None

    def newProject(self):
        pass

    def openProject(self):
        pass

    def saveProject(self):
        pass

    def newFile(self):
        pass

    def removeFile(self):
        pass

    def exportFile(self):
        filepath = QtGui.QFileDialog.getSaveFileName(self, self.tr("Export File"), "", self.tr("Elan files (*.eaf);;All files (*.*)"))
        filepath = unicode(filepath)
        if filepath != '':
            self.filepath = filepath
            self.filename = os.path.basename(filepath)
            if self.tierUtterances == None or self.tierTranslations == None or self.tierWords == None or self.tierWfW == None or self.tierGRAID1 == None or self.tierGRAID2 == None:
                QtGui.QMessageBox.critical(self, self.tr("Please define tiers"), self.tr("Please create and choose all tiers before saving the data to a file."), QtGui.QMessageBox.Ok)
                return
            self.updateEafTreeFromTexteditInterlinear()
            xml = self.eafTree.getAsEafXml(self.tierUtterances, self.tierWords, self.tierMorphemes, self.tierFunctions, self.tierTranslations)
            file = open(self.filepath, "w")
            file.write(xml)
            file.close()
            self.ui.statusBar.showMessage(self.tr("File exported."))

    def addFile(self):
        filepath = QtGui.QFileDialog.getOpenFileName(self, self.tr("Add File"), "", self.tr("Elan files (*.eaf);;All files (*.*)"))
        filepath = unicode(filepath)
        if filepath != '':
            self.init = 1
            self.annotationFileObject = EafAnnotationFileObject(filepath)
            self.annotationTierHandler = self.annotationFileObject.createTierHandler()
            self.annotationParser = self.annotationFileObject.createParser()
            self.eafTree = AnnotationTree(self.annotationParser)
            self.initTierTypesFromSettings()
            self.eafTree.parse()
            self.clearAllTierLists()
            self.clearAllTierVars()
            self.initTierUtterances()
            self.filename = os.path.basename(filepath)
            self.filepath = filepath
#            self.graphicssceneIlText.setTextTitle(self.filename)
            self.init = 0
            self.updateIlTextEdit()

    def updateEafTreeFromTexteditInterlinear(self):
        dictAnnotations = self.ui.texteditInterlinear.getAnnotationDict()
        for id in self.utterancesIds:
            utterance = self.eafTree.getUtteranceById(id)
            newUtterance = dictAnnotations["utterance-%s" % id]
            if utterance != newUtterance:
                self.eafTree.setUtterance(id, newUtterance)
            translations = self.eafTree.getTranslationsForUtterance(id)
            for t in translations:
                newTranslation = dictAnnotations["translation-%s" % t[0]]
                if t[1] != newTranslation:
                    self.eafTree.setTranslation(t[0], newTranslation)
            wordIds = self.eafTree.getWordIdsForUtterance(id)
            for wid in wordIds:
                newWord = dictAnnotations["word-%s" % wid]
                newMorphemes = dictAnnotations["morph-%s" % wid]
                newGlosses = dictAnnotations["gloss-%s" % wid]
                strWord = self.eafTree.getWordById(wid)
                strMorphemes = self.eafTree.getMorphemeStringForWord(wid)
                strGlosses = self.eafTree.getGlossStringForWord(wid)
                if newWord != strWord or newMorphemes != strMorphemes or newGlosses != strGlosses:
                    text = "%s %s %s" % (newWord, newMorphemes, newGlosses)
                    if not self.lineeditValidate(text):
                        QtGui.QMessageBox.critical(self, self.tr("Wrong input"), self.tr("The number of morphemes and the number of glosses do not match. Please check your input in utterance ") + "%s." % id, QtGui.QMessageBox.Ok)
                    else:
                        ilElement = self.eafTree.ilElementForString(text)
                        self.eafTree.setIlElementForWordId(wid, ilElement)
        return True

    def initTierTypesFromSettings(self):
            settings = QtCore.QSettings()
            arrUtteranceTierTypes = unicode(settings.value("Ann/UttTierTypeRefs",  QtCore.QVariant(u"utterance|utterances|Äußerung|Äußerungen")).toString()).split("|")
            arrWordTierTypes = unicode(settings.value("Ann/WordTierTypeRefs",  QtCore.QVariant(u"words|word|Wort|Worte|Wörter")).toString()).split("|")
            arrWfWTierTypes = unicode(settings.value("Ann/WfWTierTypeRefs",  QtCore.QVariant(u"wfwtranslation")).toString()).split("|")
            arrGRAID1TierTypes = unicode(settings.value("Ann/GRAID1TierTypeRefs",  QtCore.QVariant(u"graid1")).toString()).split("|")
            arrGRAID2TierTypes = unicode(settings.value("Ann/GRAID2TierTypeRefs",  QtCore.QVariant(u"graid2")).toString()).split("|")
            arrTranslationTierTypes = unicode(settings.value("Ann/TransTierTypeRefs",  QtCore.QVariant(u"translation|translations|Übersetzung|Übersetzungen")).toString()).split("|")
            self.annotationTierHandler.setUtterancetierType(arrUtteranceTierTypes)
            #print arrUtteranceTierTypes
            self.annotationTierHandler.setWordtierType(arrWordTierTypes)
            self.annotationTierHandler.setWfwtierType(arrMorphemeTierTypes)
            self.annotationTierHandler.setGraid1tierType(arrGlossTierTypes)
            self.annotationTierHandler.setGraid2tierType(arrGlossTierTypes)
            self.annotationTierHandler.setTranslationtierType(arrTranslationTierTypes)
            
    def initTierUtterances(self):
        self.ui.listwidgetUtterances.clear()
        #alltiers = self.eaf.tiers()
        alltiers = self.annotationTierHandler.getUtterancetierIds()
        for id in alltiers:
            item_text = "%s" % id
            item = QtGui.QListWidgetItem(item_text)
            item.setData(32,  QtCore.QVariant(id))
            #item.setData(33, QtCore.QVariant(type))
            self.ui.listwidgetUtterances.addItem(item)
        # choose first item as default
        if len(alltiers)>0:
            self.ui.listwidgetUtterances.setCurrentItem(self.ui.listwidgetUtterances.item(0))
        
    def initTierWords(self):
        self.ui.listwidgetWords.clear()
        alltiers = self.annotationTierHandler.getWordtierIds(self.tierUtterances)
        for id in alltiers:
            item_text = "%s" % id
            item = QtGui.QListWidgetItem(item_text)
            item.setData(32,  QtCore.QVariant(id))
            #item.setData(33, QtCore.QVariant(type))
            self.ui.listwidgetWords.addItem(item)
        # choose first item as default
        if len(alltiers)>0:
            self.ui.listwidgetWords.setCurrentItem(self.ui.listwidgetWords.item(0))

    def initTierWfW(self):
        self.ui.listwidgetWfW.clear()
        alltiers = self.annotationTierHandler.getWfwtierIds(self.tierWords)
        for id in alltiers:
            item_text = "%s" % id
            item = QtGui.QListWidgetItem(item_text)
            item.setData(32, QtCore.QVariant(id))
            #item.setData(33, QtCore.QVariant(type))
            self.ui.listwidgetWfW.addItem(item)
        # choose first item as default
        if len(alltiers)>0:
            self.ui.listwidgetWfW.setCurrentItem(self.ui.listwidgetWfW.item(0))
        
    def initTierGRAID1(self):
        self.ui.listwidgetGRAID1.clear()
        alltiers = self.annotationTierHandler.getGraid1tierIds(self.tierWords)
        for id in alltiers:
            item_text = "%s" % id
            item = QtGui.QListWidgetItem(item_text)
            item.setData(32,  QtCore.QVariant(id))
            #item.setData(33, QtCore.QVariant(type))
            self.ui.listwidgetGRAID1.addItem(item)
        # choose first item as default
        if len(alltiers)>0:
            self.ui.listwidgetGRAID1.setCurrentItem(self.ui.listwidgetGRAID1.item(0))

    def initTierGRAID2(self):
        self.ui.listwidgetGRAID2.clear()
        alltiers = self.annotationTierHandler.getGraid2tierIds(self.tierWords)
        for id in alltiers:
            item_text = "%s" % id
            item = QtGui.QListWidgetItem(item_text)
            item.setData(32,  QtCore.QVariant(id))
            #item.setData(33, QtCore.QVariant(type))
            self.ui.listwidgetGRAID2.addItem(item)
            # choose first item as default
        if len(alltiers)>0:
            self.ui.listwidgetGRAID2.setCurrentItem(self.ui.listwidgetGRAID2.item(0))

    def initTierTranslations(self):
        self.ui.listwidgetTranslations.clear()
        alltiers = self.annotationTierHandler.getTranslationtierIds(self.tierUtterances)
        for id in alltiers:
            item_text = "%s" % id
            item = QtGui.QListWidgetItem(item_text)
            item.setData(32,  QtCore.QVariant(id))
            #item.setData(33, QtCore.QVariant(type))
            self.ui.listwidgetTranslations.addItem(item)
        # choose first item as default
        if len(alltiers)>0:
            self.ui.listwidgetTranslations.setCurrentItem(self.ui.listwidgetTranslations.item(0))
        
    def setTierUtterances(self,  current,  prev):
        if current == None:
            self.tierUtterances = None
        else:
            self.tierUtterances = unicode(current.data(32).toString())
            self.initTierWords()
            self.initTierTranslations()
            #self.utterancesIds = self.eaf.getAlignableAnnotationIdsForTier(self.tierUtterances)
            self.utterancesIds = self.eafTree.getUtteranceIdsInTier(self.tierUtterances)
            if self.init == 0:
                self.updateIlTextEdit()

    def setTierWords(self,  current,  prev):
        if current == None:
            self.tierWords = None
        else:
            self.tierWords = unicode(current.data(32).toString())
            self.initTierMorphemes()
            if self.init == 0:
                self.updateIlTextEdit()

    def setTierWfW(self,  current,  prev):
        if current == None:
            self.tierWfW = None
        else:
            self.tierWfW = unicode(current.data(32).toString())
            self.initTierWfW()
            if self.init == 0:
                self.updateIlTextEdit()

    def setTierGRAID1(self,  current,  prev):
        if current == None:
            self.tierGRAID1 = None
        else:
            self.tierGRAID1 = unicode(current.data(32).toString())
            if self.init == 0:
                self.updateIlTextEdit()

    def setTierGRAID2(self,  current,  prev):
        if current == None:
            self.tierGRAID2 = None
        else:
            self.tierGRAID2 = unicode(current.data(32).toString())
            if self.init == 0:
                self.updateIlTextEdit()

    def setTierTranslations(self,  current,  prev):
        if current == None:
            self.tierTranslations = None
        else:
            self.tierTranslations = unicode(current.data(32).toString())
            if self.init == 0:
                self.updateIlTextEdit()

    def newTierWfW(self):
        if self.tierWords == '':
            QtGui.QMessageBox.critical(self, self.tr("No word translation tier"), self.tr("Please choose or create a word tier before creating the word-for-word-translation tier."), QtGui.QMessageBox.Ok)
        else:
            locale = self.annotationTierHandler.getLocaleForTier(self.tierWords)
            participant = self.annotationTierHandler.getParticipantForTier(self.tierWords)
            dialog = DialogNewTier(self.tierWords,  'wfwtranslation',  locale, participant, self)
            ret = dialog.exec_()
            if ret == 1:
                self.annotationTierHandler.addTier(dialog.tierId, dialog.tierType, "Symbolic_Subdivision", self.tierWords, dialog.tierDefaultLocale, dialog.tierParticipant)
                self.initTierMorphemes()


    def newTierGRAID1(self):
        if self.tierMorphemes == '':
            QtGui.QMessageBox.critical(self, self.tr("No word tier"), self.tr("Please choose or create a word tier before creating the GRAID1 tier."), QtGui.QMessageBox.Ok)
        else:
            locale = self.annotationTierHandler.getLocaleForTier(self.tierMorphemes)
            participant = self.annotationTierHandler.getParticipantForTier(self.tierMorphemes)
            dialog = DialogNewTier(self.tierMorphemes,  'graid1',  locale, participant, self)
            ret = dialog.exec_()
            if ret == 1:
                self.annotationTierHandler.addTier(dialog.tierId, dialog.tierType, "Symbolic_Subdivision", self.tierWords, dialog.tierDefaultLocale, dialog.tierParticipant)
                self.initTierGlosses()


    def newTierGRAID2(self):
        if self.tierUtterances == '':
            QtGui.QMessageBox.critical(self, self.tr("No utterances tier"), self.tr("Please choose or create an utterances tier before creating the GRAID2 tier."), QtGui.QMessageBox.Ok)
        else:
            locale = self.annotationTierHandler.getLocaleForTier(self.tierUtterances)
            participant = self.annotationTierHandler.getParticipantForTier(self.tierUtterances)
            dialog = DialogNewTier(self.tierUtterances,  'graid2',  locale, participant, self)
            ret = dialog.exec_()
            if ret == 1:
                self.annotationTierHandler.addTier(dialog.tierId, dialog.tierType, "Symbolic_Association", self.tierUtterances, dialog.tierDefaultLocale, dialog.tierParticipant)
                self.initTierTranslations()

    def newTierTranslations(self):
        if self.tierUtterances == '':
            QtGui.QMessageBox.critical(self, self.tr("No utterances tier"), self.tr("Please choose or create an utterances tier before creating the translation tier."), QtGui.QMessageBox.Ok)
        else:
            locale = self.annotationTierHandler.getLocaleForTier(self.tierUtterances)
            participant = self.annotationTierHandler.getParticipantForTier(self.tierUtterances)
            dialog = DialogNewTier(self.tierUtterances,  'translations',  locale, participant, self)
            ret = dialog.exec_()
            if ret == 1:
                self.annotationTierHandler.addTier(dialog.tierId, dialog.tierType, "Symbolic_Association", self.tierUtterances, dialog.tierDefaultLocale, dialog.tierParticipant)
                self.initTierTranslations()

