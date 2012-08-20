# -*- coding: utf-8 -*-
# (C) 2009 copyright by Peter Bouda

from __future__ import unicode_literals
import sys, os.path, re
from PyQt4 import QtCore, QtGui

#from pyannotation.elan.data import EafAnnotationFileObject
import pyannotation.annotationtree

import poio
from poio.ui.PoioIlTextEdit import PoioIlTextEdit
from poio.ui.Ui_MainWindow import Ui_MainWindow
from poio.ui.DialogNewTier import DialogNewTier
from poio.poioproject import PoioProject

class PoioILE(QtGui.QMainWindow):
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
        QtCore.QObject.connect(self.ui.listwidgetMorphemes, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.set_tier_morphemes)
        QtCore.QObject.connect(self.ui.listwidgetFunctions, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.set_tier_functions)
        QtCore.QObject.connect(self.ui.listwidgetTranslations, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.set_tier_translations)
        QtCore.QObject.connect(self.ui.pushbuttonNewTierMorphemes, QtCore.SIGNAL("clicked()"), self.new_tier_morphemes)
        QtCore.QObject.connect(self.ui.pushbuttonNewTierFunctions, QtCore.SIGNAL("clicked()"), self.new_tier_functions)
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
            arr_utterance_tier_types = unicode(settings.value("Ann/UttTierTypeRefs",  QtCore.QVariant("utterance|utterances|Äußerung|Äußerungen")).toString()).split("|")
            arr_word_tier_types = unicode(settings.value("Ann/WordTierTypeRefs",  QtCore.QVariant("words|word|Wort|Worte|Wörter")).toString()).split("|")
            arr_morpheme_tier_types = unicode(settings.value("Ann/MorphTierTypeRefs",  QtCore.QVariant("morpheme|morphemes|Morphem|Morpheme")).toString()).split("|")
            arr_gloss_tier_types = unicode(settings.value("Ann/GlossTierTypeRefs",  QtCore.QVariant("glosses|gloss|Glossen|Gloss|Glosse")).toString()).split("|")
            arr_translation_tier_types = unicode(settings.value("Ann/TransTierTypeRefs",  QtCore.QVariant("translation|translations|Übersetzung|Übersetzungen")).toString()).split("|")
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

    def init_tier_morphemes(self):
        self.ui.listwidgetMorphemes.clear()
        alltiers = self.eaf_tree.tier_handler.get_morphemetier_ids(self.tier_words)
        for id in alltiers:
            item_text = "%s" % id
            item = QtGui.QListWidgetItem(item_text)
            item.setData(32,  QtCore.QVariant(id))
            #item.setData(33, QtCore.QVariant(type))
            self.ui.listwidgetMorphemes.addItem(item)
        # choose first item as default
        if len(alltiers)>0:
            self.ui.listwidgetMorphemes.setCurrentItem(self.ui.listwidgetMorphemes.item(0))
        
    def init_tier_glosses(self):
        self.ui.listwidgetFunctions.clear()
        alltiers = self.eaf_tree.tier_handler.get_glosstier_ids(self.tier_morphemes)
        for id in alltiers:
            item_text = "%s" % id
            item = QtGui.QListWidgetItem(item_text)
            item.setData(32,  QtCore.QVariant(id))
            #item.setData(33, QtCore.QVariant(type))
            self.ui.listwidgetFunctions.addItem(item)
        # choose first item as default
        if len(alltiers)>0:
            self.ui.listwidgetFunctions.setCurrentItem(self.ui.listwidgetFunctions.item(0))

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

    def set_tier_morphemes(self,  current,  prev):
        if current == None:
            self.tier_morphemes = None
        else:
            self.tier_morphemes = unicode(current.data(32).toString())
            self.init_tier_glosses()
            if self.init == 0:
                self.update_il_text_edit()

    def set_tier_functions(self,  current,  prev):
        if current == None:
            self.tier_functions = None
        else:
            self.tier_functions = unicode(current.data(32).toString())
            if self.init == 0:
                self.update_il_text_edit()

    def set_tier_translations(self,  current,  prev):
        if current == None:
            self.tier_translations = None
        else:
            self.tier_translations = unicode(current.data(32).toString())
            if self.init == 0:
                self.update_il_text_edit()

    def new_tier_morphemes(self):
        if self.tier_words == '':
            QtGui.QMessageBox.critical(self, self.tr("No word tier"), self.tr("Please choose or create a word tier before creating the morpheme tier."), QtGui.QMessageBox.Ok)
        else:
            locale = self.eaf_tree.tier_handler.get_locale_for_tier(self.tier_words)
            participant = self.eaf_tree.tier_handler.get_participant_for_tier(self.tier_words)
            dialog = DialogNewTier(self.tier_words,  'morphemes',  locale, participant, self)
            ret = dialog.exec_()
            if ret == 1:
                self.eaf_tree.tier_handler.add_tier(dialog.tierId, dialog.tierType, "Symbolic_Subdivision", self.tier_words, dialog.tierDefaultLocale, dialog.tierParticipant)
                self.init_tier_morphemes()

    def new_tier_functions(self):
        if self.tier_morphemes == '':
            QtGui.QMessageBox.critical(self, self.tr("No morphemes tier"), self.tr("Please choose or create a morphemes tier before creating the gloss tier."), QtGui.QMessageBox.Ok)
        else:
            locale = self.eaf_tree.tier_handler.get_locale_for_tier(self.tier_morphemes)
            participant = self.eaf_tree.tier_handler.get_participant_for_tier(self.tier_morphemes)
            dialog = DialogNewTier(self.tier_morphemes,  'glosses',  locale, participant, self)
            ret = dialog.exec_()
            if ret == 1:
                self.eaf_tree.tier_handler.add_tier(dialog.tierId, dialog.tierType, "Symbolic_Subdivision", self.tier_morphemes, dialog.tierDefaultLocale, dialog.tierParticipant)
                self.init_tier_glosses()

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

