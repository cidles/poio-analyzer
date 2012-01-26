# -*- coding: utf-8 -*-
# (C) 2009 copyright by Peter Bouda

import sys, os.path, re
from PyQt4 import QtCore, QtGui

#from pyannotation.elan.data import EafAnnotationFileObject
import pyannotation.annotationtree

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

        self.init_vars()
        self.init_connects()
        self.init_settings()

        self.init = 0

    def init_vars(self):
        self.eaf = None
        self.utterances_dict = []
        self.clear_all_tier_vars()
        self.filename = ''
        self.project = None

    def init_settings(self):
        QtCore.QCoreApplication.setOrganizationName("Interdisciplinary Centre for Social and Language Documentation");
        QtCore.QCoreApplication.setOrganizationDomain("cidles.eu");
        QtCore.QCoreApplication.setApplicationName("PoioILE");
        settings = QtCore.QSettings()
        self.str_morpheme_seperator = unicode(settings.value("Ann/MorphSep", QtCore.QVariant("-")).toString())
        self.str_gloss_sepereator = unicode(settings.value("Ann/GlossSep",  QtCore.QVariant(":")).toString())
        self.str_empty_character = unicode(settings.value("Ann/EmptyChar",  QtCore.QVariant("#")).toString())

    def init_connects(self):
        # Projects
        QtCore.QObject.connect(self.ui.actionNew, QtCore.SIGNAL("triggered()"), self.new_project)
        QtCore.QObject.connect(self.ui.actionOpen, QtCore.SIGNAL("triggered()"), self.open_project)
        #QtCore.QObject.connect(self.ui.actionSaveAs, QtCore.SIGNAL("triggered()"), self.saveProjectAs)
        QtCore.QObject.connect(self.ui.actionSave, QtCore.SIGNAL("triggered()"), self.save_project)

        # Files
        QtCore.QObject.connect(self.ui.actionAddFile, QtCore.SIGNAL("triggered()"), self.add_file)
        self.ui.toolbuttonAddFile.setDefaultAction(self.ui.actionAddFile)
        QtCore.QObject.connect(self.ui.actionExportFile, QtCore.SIGNAL("triggered()"), self.export_file)
        self.ui.toolbuttonExportFile.setDefaultAction(self.ui.actionExportFile)
        QtCore.QObject.connect(self.ui.actionNewFile, QtCore.SIGNAL("triggered()"), self.new_file)
        self.ui.toolbuttonNewFile.setDefaultAction(self.ui.actionNewFile)
        QtCore.QObject.connect(self.ui.actionRemoveFile, QtCore.SIGNAL("triggered()"), self.remove_file)
        self.ui.toolbuttonRemoveFile.setDefaultAction(self.ui.actionRemoveFile)

        QtCore.QObject.connect(self.ui.actionQuit, QtCore.SIGNAL("triggered()"), self.close)
        QtCore.QObject.connect(self.ui.actionAboutPoioILE, QtCore.SIGNAL("triggered()"), self.about_dialog)
        QtCore.QObject.connect(self.ui.actionInsertUtterance, QtCore.SIGNAL("triggered()"), self.insert_utterance_after_current)
        QtCore.QObject.connect(self.ui.actionDeleteUtterance, QtCore.SIGNAL("triggered()"), self.delete_current_utterance)
        QtCore.QObject.connect(self.ui.actionInsertWord, QtCore.SIGNAL("triggered()"), self.insert_word_after_current)
        QtCore.QObject.connect(self.ui.actionDeleteWord, QtCore.SIGNAL("triggered()"), self.delete_current_word)

        QtCore.QObject.connect(self.ui.listwidgetUtterances, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.set_tier_utterances)
        QtCore.QObject.connect(self.ui.listwidgetWords, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.set_tier_words)
        QtCore.QObject.connect(self.ui.listwidgetWfw, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.set_tier_wfw)
        QtCore.QObject.connect(self.ui.listwidgetGraid1, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.set_tier_graid1)
        QtCore.QObject.connect(self.ui.listwidgetGraid2, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.set_tier_graid2)
        QtCore.QObject.connect(self.ui.listwidgetTranslations, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.set_tier_translations)

        QtCore.QObject.connect(self.ui.pushbuttonNewTierWfw, QtCore.SIGNAL("clicked()"), self.new_tier_wfw)
        QtCore.QObject.connect(self.ui.pushbuttonNewTierGraid1, QtCore.SIGNAL("clicked()"), self.new_tier_graid1)
        QtCore.QObject.connect(self.ui.pushbuttonNewTierGraid2, QtCore.SIGNAL("clicked()"), self.new_tier_graid2)
        QtCore.QObject.connect(self.ui.pushbuttonNewTierTranslations, QtCore.SIGNAL("clicked()"), self.new_tier_translations)

    def about_dialog(self):
        about = QtGui.QMessageBox(self)
        about.setTextFormat(QtCore.Qt.RichText)
        about.setWindowTitle(self.tr("About PoioILE"))
        about.setText(self.tr("<b>PoioILE 0.2.1</b><br/>Poio Interlinear Editor by the <a href=\"http://cidles.eu\">Interdisciplinary Centre for Social and Language Documentation</a>.<br/><br/>All rights reserved. See LICENSE file for details.<br/><br/>For more information visit the website:<br/><a href=\"http://ltml.cidles.eu/poio\">http://ltml.cidles.eu/poio</a>"))
        about.exec_()

    def lineedit_validate(self, input):
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

    def update_il_text_edit(self):
        self.ui.texteditInterlinear.clear()
        self.ui.texteditInterlinear.appendTitle(self.filename)
        id_in_scene = 1

        for id in self.utterances_ids:
            utterance = self.eaf_tree.get_utterance_by_id(id)
            translations = self.eaf_tree.get_translations_for_utterance(id)
            if len(translations) == 0:
                id_translation = self.eaf_tree.new_translation_for_utterance_id(id, "")
                translations = [ [id_translation, self.str_empty_character] ]
            else:
                for t in translations:
                    if t[1] == "":
                        t[1] = self.str_empty_character
            ids_words = self.eaf_tree.get_word_ids_for_utterance(id)
            il_elements = []
            for id_w in ids_words:
                if id_w == "":
                    str_word = self.str_empty_character
                    str_morphemes = self.str_empty_character
                    str_glosses = self.str_empty_character
                else:
                    str_word = self.eaf_tree.get_word_by_id(id_w)
                    if str_word == "":
                        str_word = self.str_empty_character
                    str_morphemes = self.eaf_tree.get_morpheme_string_for_word(id_w)
                    if str_morphemes == "":
                        str_morphemes = str_word
                    str_glosses = self.eaf_tree.get_gloss_string_for_word(id_w)
                    if str_glosses == "":
                        str_glosses = self.str_empty_character
                il_elements.append([id_w, str_word, str_morphemes, str_glosses, False])
            self.ui.texteditInterlinear.appendUtterance(id,  utterance, il_elements, translations)
            id_in_scene = id_in_scene + 1

        self.ui.texteditInterlinear.scrollToAnchor("title")

    def delete_current_utterance(self):
        self.update_eaf_tree_from_textedit_interlinear()
        #utteranceId = self.ui.texteditInterlinear.deleteCurrentUtterance()
        id_utterance = self.ui.texteditInterlinear.getCurrentUtteranceId()
        if id_utterance == "":
            QtGui.QMessageBox.info(self, self.tr("No utterance selected"), self.tr("Please move the cursor to the utterace you want to delete."), QtGui.QMessageBox.Ok)
        else:
            self.eaf_tree.remove_utterance_with_id(id_utterance)
            self.utterances_ids.remove(id_utterance)
            self.update_il_text_edit()

    def insert_utterance_after_current(self):
        pass

    def delete_current_word(self):
        self.update_eaf_tree_from_textedit_interlinear()
        id_word = self.ui.texteditInterlinear.getCurrentWordId()
        if id_word == "":
            QtGui.QMessageBox.information(self, self.tr("No word selected"), self.tr("Please move the cursor to the word you want to delete."), QtGui.QMessageBox.Ok)
        else:
            self.eaf_tree.remove_word_with_id(id_word)
            self.update_il_text_edit()

    def insert_word_after_current(self):
        pass

    def clear_all_tier_lists(self):
        self.ui.listwidgetUtterances.clear()
        self.ui.listwidgetWords.clear()
        self.ui.listwidgetMorphemes.clear()
        self.ui.listwidgetFunctions.clear()
        self.ui.listwidgetTranslations.clear()

    def clear_all_tier_vars(self):
        self.tier_words = None
        self.tier_utterances = None
        self.tier_morphemes = None
        self.tier_functions = None
        self.tier_translations = None

    def new_project(self):
        pass

    def open_project(self):
        pass

    def save_project(self):
        pass

    def new_file(self):
        pass

    def remove_file(self):
        pass

    def export_file(self):
        filepath = QtGui.QFileDialog.getSaveFileName(self, self.tr("Export File"), "", self.tr("Elan files (*.eaf);;All files (*.*)"))
        filepath = unicode(filepath)
        if filepath != '':
            self.filepath = filepath
            self.filename = os.path.basename(filepath)
            if self.tier_utterances == None or self.tier_translations == None or self.tier_words == None or self.tier_morphemes == None or self.tier_functions == None:
                QtGui.QMessageBox.critical(self, self.tr("Please define tiers"), self.tr("Please create and choose all tiers before saving the data to a file."), QtGui.QMessageBox.Ok)
                return
            self.update_eaf_tree_from_textedit_interlinear()
            xml = self.eaf_tree.get_file(self.tier_utterances, self.tier_words, self.tier_morphemes, self.tier_functions, self.tier_translations)
            file = open(self.filepath, "w")
            file.write(xml)
            file.close()
            self.ui.statusBar.showMessage(self.tr("File exported."))

    def add_file(self):
        filepath = QtGui.QFileDialog.getOpenFileName(self, self.tr("Add File"), "", self.tr("Elan files (*.eaf);;All files (*.*)"))
        filepath = unicode(filepath)
        if filepath != '':
            self.init = 1
            #self.annotation_file_object = EafAnnotationFileObject(filepath)
            #self.annotationTierHandler = self.annotationFileObject.createTierHandler()
            #self.annotationParser = self.annotationFileObject.createParserMorphsynt()
            self.eaf_tree = pyannotation.annotationtree.AnnotationTree(
                pyannotation.data.EAF,
                pyannotation.data.MORPHSYNT,
                filepath
            )
            self.init_tier_types_from_settings()
            self.eaf_tree.parse()
            self.clear_all_tier_lists()
            self.clear_all_tier_vars()
            self.init_tier_utterances()
            self.filename = os.path.basename(filepath)
            self.filepath = filepath
            #            self.graphicssceneIlText.setTextTitle(self.filename)
            self.init = 0
            self.update_il_text_edit()

    def update_eaf_tree_from_textedit_interlinear(self):
        dict_annotations = self.ui.texteditInterlinear.getAnnotationDict()
        for id in self.utterances_ids:
            utterance = self.eaf_tree.get_utterance_by_id(id)
            new_utterance = dict_annotations["utterance-%s" % id]
            if utterance != new_utterance:
                self.eaf_tree.set_utterance(id, new_utterance)
            translations = self.eaf_tree.get_translations_for_utterance(id)
            for t in translations:
                new_translation = dict_annotations["translation-%s" % t[0]]
                if t[1] != new_translation:
                    self.eaf_tree.set_translation(t[0], new_translation)
            ids_words = self.eaf_tree.get_word_ids_for_utterance(id)
            for id_w in ids_words:
                new_word = dict_annotations["word-%s" % id_w]
                new_morphemes = dict_annotations["morph-%s" % id_w]
                new_glosses = dict_annotations["gloss-%s" % id_w]
                str_word = self.eaf_tree.get_word_by_id(id_w)
                str_morphemes = self.eaf_tree.get_morpheme_string_for_word(id_w)
                str_glosses = self.eaf_tree.get_gloss_string_for_word(id_w)
                if new_word != str_word or new_morphemes != str_morphemes or new_glosses != str_glosses:
                    text = "%s %s %s" % (new_word, new_morphemes, new_glosses)
                    if not self.lineedit_validate(text):
                        QtGui.QMessageBox.critical(self, self.tr("Wrong input"), self.tr("The number of morphemes and the number of glosses do not match. Please check your input in utterance ") + "%s." % id, QtGui.QMessageBox.Ok)
                    else:
                        il_element = self.eaf_tree.il_element_for_string(text)
                        self.eaf_tree.set_il_element_for_word_id(id_w, il_element)
        return True

    def init_tier_types_from_settings(self):
        settings = QtCore.QSettings()
        arr_utterance_tier_types = unicode(settings.value("Ann/UttTierTypeRefs",  QtCore.QVariant(u"utterance|utterances|Äußerung|Äußerungen")).toString()).split("|")
        arr_word_tier_types = unicode(settings.value("Ann/WordTierTypeRefs",  QtCore.QVariant(u"words|word|Wort|Worte|Wörter")).toString()).split("|")
        arr_morpheme_tier_types = unicode(settings.value("Ann/MorphTierTypeRefs",  QtCore.QVariant(u"morpheme|morphemes|Morphem|Morpheme")).toString()).split("|")
        arr_gloss_tier_types = unicode(settings.value("Ann/GlossTierTypeRefs",  QtCore.QVariant(u"glosses|gloss|Glossen|Gloss|Glosse")).toString()).split("|")
        arr_translation_tier_types = unicode(settings.value("Ann/TransTierTypeRefs",  QtCore.QVariant(u"translation|translations|Übersetzung|Übersetzungen")).toString()).split("|")
        self.eaf_tree.tier_handler.set_utterancetier_type(arr_utterance_tier_types)
        #print arrUtteranceTierTypes
        self.eaf_tree.tier_handler.set_wordtier_type(arr_word_tier_types)
        self.eaf_tree.tier_handler.set_morphemetier_type(arr_morpheme_tier_types)
        self.eaf_tree.tier_handler.set_glosstier_type(arr_gloss_tier_types)
        self.eaf_tree.tier_handler.set_translationtier_type(arr_translation_tier_types)

    def init_tier_utterances(self):
        self.ui.listwidgetUtterances.clear()
        #alltiers = self.eaf.tiers()
        alltiers = self.eaf_tree.tier_handler.get_utterancetier_ids()
        for id in alltiers:
            item_text = "%s" % id
            item = QtGui.QListWidgetItem(item_text)
            item.setData(32,  QtCore.QVariant(id))
            #item.setData(33, QtCore.QVariant(type))
            self.ui.listwidgetUtterances.addItem(item)
            # choose first item as default
        if len(alltiers)>0:
            self.ui.listwidgetUtterances.setCurrentItem(self.ui.listwidgetUtterances.item(0))

    def init_tier_words(self):
        self.ui.listwidgetWords.clear()
        alltiers = self.eaf_tree.tier_handler.get_wordtier_ids(self.tier_utterances)
        for id in alltiers:
            item_text = "%s" % id
            item = QtGui.QListWidgetItem(item_text)
            item.setData(32,  QtCore.QVariant(id))
            #item.setData(33, QtCore.QVariant(type))
            self.ui.listwidgetWords.addItem(item)
            # choose first item as default
        if len(alltiers)>0:
            self.ui.listwidgetWords.setCurrentItem(self.ui.listwidgetWords.item(0))

    def init_tier_wfw(self):
        self.ui.listwidgetWfW.clear()
        alltiers = self.eaf_tree.tier_handler.get_wfwtier_ids(self.tier_words)
        for id in alltiers:
            item_text = "%s" % id
            item = QtGui.QListWidgetItem(item_text)
            item.setData(32, QtCore.QVariant(id))
            #item.setData(33, QtCore.QVariant(type))
            self.ui.listwidgetWfW.addItem(item)
            # choose first item as default
        if len(alltiers)>0:
            self.ui.listwidgetWfW.setCurrentItem(self.ui.listwidgetWfW.item(0))

    def init_tier_graid1(self):
        self.ui.listwidgetGRAID1.clear()
        alltiers = self.eaf_tree.tier_handler.get_graid1tier_ids(self.tier_words)
        for id in alltiers:
            item_text = "%s" % id
            item = QtGui.QListWidgetItem(item_text)
            item.setData(32,  QtCore.QVariant(id))
            #item.setData(33, QtCore.QVariant(type))
            self.ui.listwidgetGRAID1.addItem(item)
            # choose first item as default
        if len(alltiers)>0:
            self.ui.listwidgetGRAID1.setCurrentItem(self.ui.listwidgetGRAID1.item(0))

    def init_tier_graid2(self):
        self.ui.listwidgetGRAID2.clear()
        alltiers = self.eaf_tree.tier_handler.get_graid2tier_ids(self.tier_words)
        for id in alltiers:
            item_text = "%s" % id
            item = QtGui.QListWidgetItem(item_text)
            item.setData(32,  QtCore.QVariant(id))
            #item.setData(33, QtCore.QVariant(type))
            self.ui.listwidgetGRAID2.addItem(item)
            # choose first item as default
        if len(alltiers)>0:
            self.ui.listwidgetGRAID2.setCurrentItem(self.ui.listwidgetGRAID2.item(0))

    def init_tier_translations(self):
        self.ui.listwidgetTranslations.clear()
        alltiers = self.eaf_tree.tier_handler.get_translationtier_ids(self.tier_utterances)
        for id in alltiers:
            item_text = "%s" % id
            item = QtGui.QListWidgetItem(item_text)
            item.setData(32,  QtCore.QVariant(id))
            #item.setData(33, QtCore.QVariant(type))
            self.ui.listwidgetTranslations.addItem(item)
            # choose first item as default
        if len(alltiers)>0:
            self.ui.listwidgetTranslations.setCurrentItem(self.ui.listwidgetTranslations.item(0))

    def set_tier_utterances(self,  current,  prev):
        if current == None:
            self.tier_utterances = None
        else:
            self.tier_utterances = unicode(current.data(32).toString())
            self.init_tier_words()
            self.init_tier_translations()
            #self.utterancesIds = self.eaf.getAlignableAnnotationIdsForTier(self.tierUtterances)
            self.utterances_ids = self.eaf_tree.get_utterance_ids_in_tier(self.tier_utterances)
            if self.init == 0:
                self.update_il_text_edit()

    def set_tier_words(self,  current,  prev):
        if current == None:
            self.tier_words = None
        else:
            self.tier_words = unicode(current.data(32).toString())
            self.init_tier_morphemes()
            if self.init == 0:
                self.update_il_text_edit()

    def set_tier_wfw(self,  current,  prev):
        if current == None:
            self.tier_wfw = None
        else:
            self.tier_wfw = unicode(current.data(32).toString())
            if self.init == 0:
                self.updateIlTextEdit()

    def set_tier_graid1(self,  current,  prev):
        if current == None:
            self.tier_graid1 = None
        else:
            self.tier_graid1 = unicode(current.data(32).toString())
            if self.init == 0:
                self.update_il_text_edit()()

    def set_tier_graid2(self,  current,  prev):
        if current == None:
            self.tier_graid2 = None
        else:
            self.tier_graid2 = unicode(current.data(32).toString())
            if self.init == 0:
                self.update_il_text_edit()

    def set_tier_translations(self,  current,  prev):
        if current == None:
            self.tier_translations = None
        else:
            self.tier_translations = unicode(current.data(32).toString())
            if self.init == 0:
                self.update_il_text_edit()

    def new_tier_wfw(self):
        if self.tier_words == '':
            QtGui.QMessageBox.critical(self, self.tr("No word tier"), self.tr("Please choose or create a word tier before creating the word-for-word-translation tier."), QtGui.QMessageBox.Ok)
        else:
            locale = self.eaf_tree.tier_handler.getLocaleForTier(self.tier_words)
            participant = self.eaf_tree.tier_handler.getParticipantForTier(self.tier_words)
            dialog = DialogNewTier(self.tier_words,  'wfwtranslation',  locale, participant, self)
            ret = dialog.exec_()
            if ret == 1:
                self.eaf_tree.tier_handler.addTier(dialog.tierId, dialog.tierType, "Symbolic_Subdivision", self.tier_words, dialog.tierDefaultLocale, dialog.tierParticipant)
                self.init_tier_wfw()

    def new_tier_graid1(self):
        if self.tier_words == '':
            QtGui.QMessageBox.critical(self, self.tr("No word tier"), self.tr("Please choose or create a word tier before creating the GRAID1 tier."), QtGui.QMessageBox.Ok)
        else:
            locale = self.eaf_tree.tier_handler.getLocaleForTier(self.tierMorphemes)
            participant = self.eaf_tree.tier_handler.getParticipantForTier(self.tierMorphemes)
            dialog = DialogNewTier(self.tier_words,'graid1', locale, participant, self)
            ret = dialog.exec_()
            if ret == 1:
                self.eaf_tree.tier_handler.addTier(dialog.tierId, dialog.tierType, "Symbolic_Subdivision", self.tier_words, dialog.tierDefaultLocale, dialog.tierParticipant)
                self.init_tier_graid1()

    def new_tier_graid2(self):
        if self.tier_utterances == '':
            QtGui.QMessageBox.critical(self, self.tr("No utterances tier"), self.tr("Please choose or create an utterances tier before creating the GRAID2 tier."), QtGui.QMessageBox.Ok)
        else:
            locale = self.eaf_tree.tier_handler.get_locale_for_tier(self.tier_utterances)
            participant = self.eaf_tree.tier_handler.get_participant_for_tier(self.tier_utterances)
            dialog = DialogNewTier(self.tier_utterances, 'graid2', locale, participant, self)
            ret = dialog.exec_()
            if ret == 1:
                self.eaf_tree.tier_handler.add_tier(dialog.tierId, dialog.tierType, "Symbolic_Association", self.tier_utterances, dialog.tierDefaultLocale, dialog.tierParticipant)
                self.init_tier_graid2()

    def new_tier_translations(self):
        if self.tier_utterances == '':
            QtGui.QMessageBox.critical(self, self.tr("No utterances tier"), self.tr("Please choose or create an utterances tier before creating the translation tier."), QtGui.QMessageBox.Ok)
        else:
            locale = self.eaf_tree.tier_handler.get_locale_for_tier(self.tier_utterances)
            participant = self.eaf_tree.tier_handler.get_participant_for_tier(self.tier_utterances)
            dialog = DialogNewTier(self.tier_utterances,  'translations',  locale, participant, self)
            ret = dialog.exec_()
            if ret == 1:
                self.eaf_tree.tier_handler.add_tier(dialog.tierId, dialog.tierType, "Symbolic_Association", self.tier_utterances, dialog.tierDefaultLocale, dialog.tierParticipant)
                self.init_tier_translations()











class PoioGRAID_old(QtGui.QMainWindow):
    """The main window of the PoioILE application."""

    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)

        # initialize UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # initialize properties
        self.init_vars()

        self.init_settings()
        self.init_connects()
        #self.initSignals()
        #self.hideTiersWidgets()
        self.init = 0
        
    def init_vars(self):
        self.eaf = None
        self.utterances_dict = []
        self.clear_all_tier_vars()
        self.filename = ''
        self.project = None

    def init_settings(self):
        QtCore.QCoreApplication.setOrganizationName("Interdisciplinary Centre for Social and Language Documentation");
        QtCore.QCoreApplication.setOrganizationDomain("cidles.eu");
        QtCore.QCoreApplication.setApplicationName("PoioGRAID");
        settings = QtCore.QSettings()
        self.str_empty_character = unicode(settings.value("Ann/EmptyChar",  QtCore.QVariant("#")).toString())
        
    def initConnects(self):
        # Projects
        QtCore.QObject.connect(self.ui.actionNew, QtCore.SIGNAL("triggered()"), self.new_project)
        QtCore.QObject.connect(self.ui.actionOpen, QtCore.SIGNAL("triggered()"), self.open_project)
        #QtCore.QObject.connect(self.ui.actionSaveAs, QtCore.SIGNAL("triggered()"), self.saveProjectAs)
        QtCore.QObject.connect(self.ui.actionSave, QtCore.SIGNAL("triggered()"), self.save_project)

        # Files
        QtCore.QObject.connect(self.ui.actionAddFile, QtCore.SIGNAL("triggered()"), self.add_file)
        self.ui.toolbuttonAddFile.setDefaultAction(self.ui.actionAddFile)
        QtCore.QObject.connect(self.ui.actionExportFile, QtCore.SIGNAL("triggered()"), self.export_file)
        self.ui.toolbuttonExportFile.setDefaultAction(self.ui.actionExportFile)
        QtCore.QObject.connect(self.ui.actionNewFile, QtCore.SIGNAL("triggered()"), self.new_file)
        self.ui.toolbuttonNewFile.setDefaultAction(self.ui.actionNewFile)
        QtCore.QObject.connect(self.ui.actionRemoveFile, QtCore.SIGNAL("triggered()"), self.remove_file)
        self.ui.toolbuttonRemoveFile.setDefaultAction(self.ui.actionRemoveFile)

        QtCore.QObject.connect(self.ui.actionQuit, QtCore.SIGNAL("triggered()"), self.close)
        QtCore.QObject.connect(self.ui.actionAboutPoioILE, QtCore.SIGNAL("triggered()"), self.about_dialog)
        QtCore.QObject.connect(self.ui.actionInsertUtterance, QtCore.SIGNAL("triggered()"), self.insert_utterance_after_current)
        QtCore.QObject.connect(self.ui.actionDeleteUtterance, QtCore.SIGNAL("triggered()"), self.delete_current_utterance)
        QtCore.QObject.connect(self.ui.actionInsertWord, QtCore.SIGNAL("triggered()"), self.insert_word_after_current)
        QtCore.QObject.connect(self.ui.actionDeleteWord, QtCore.SIGNAL("triggered()"), self.delete_current_word)
        QtCore.QObject.connect(self.ui.listwidgetUtterances, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.set_tier_utterances)
        QtCore.QObject.connect(self.ui.listwidgetWords, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.set_tier_words)
        QtCore.QObject.connect(self.ui.listwidgetGRAID1, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.set_tier_graid1)
        QtCore.QObject.connect(self.ui.listwidgetGRAID2, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.set_tier_graid2)
        QtCore.QObject.connect(self.ui.listwidgetTranslations, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.set_tier_translations)
        QtCore.QObject.connect(self.ui.pushbuttonNewTierWfW, QtCore.SIGNAL("clicked()"), self.new_tier_wfw)
        QtCore.QObject.connect(self.ui.pushbuttonNewTierGRAID1, QtCore.SIGNAL("clicked()"), self.new_tier_graid1)
        QtCore.QObject.connect(self.ui.pushbuttonNewTierGRAID2, QtCore.SIGNAL("clicked()"), self.new_tier_graid2)
        QtCore.QObject.connect(self.ui.pushbuttonNewTierTranslations, QtCore.SIGNAL("clicked()"), self.new_tier_translations)

    def about_dialog(self):
        about = QtGui.QMessageBox(self)
        about.setTextFormat(QtCore.Qt.RichText)
        about.setWindowTitle(self.tr("About PoioGRAID"))
        about.setText(self.tr("<b>PoioGRAID 0.1.0</b><br/>Poio GRAID Editor by the <a href=\"http://www.cidles.eu\">Interdisciplinary Centre for Social and Language Documentation</a>.<br/><br/>All rights reserved. See LICENSE file for details.<br/><br/>For more information visit the website:<br/><a href=\"http://www.cidles.eu/ltll/poio\">http://www.cidles.eu/poio/ltll</a>"))
        about.exec_()

    def lineedit_validate(self, input):
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

        for id in self.utterancesIds:
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

