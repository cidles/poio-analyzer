# -*- coding: utf-8 -*-
# (C) 2009 copyright by Peter Bouda

import sys, os.path, re
from PyQt4 import QtCore, QtGui

import pyannotation.annotationtree
import pyannotation.data

#from poio.ui.PoioGraidTextEdit import PoioGraidTextEdit
from poio.ui.Ui_MainWindowGRAID import Ui_MainWindow
from poio.ui.Ui_NewFileGraid import Ui_NewFileGraid


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

        self.ui.textedit.append_title("Please create or open a file...")

    def init_vars(self):
        self.annotation_tree = pyannotation.annotationtree.AnnotationTree(pyannotation.data.GRAID)
        #self.utterances_dict = []
        #self.clear_all_tier_vars()
        self.filename = ''
        self.title = ''
        #self.project = None

    def init_settings(self):
        QtCore.QCoreApplication.setOrganizationName("Interdisciplinary Centre for Social and Language Documentation");
        QtCore.QCoreApplication.setOrganizationDomain("cidles.eu");
        QtCore.QCoreApplication.setApplicationName("PoioGRAID");
        settings = QtCore.QSettings()
        #self.str_morpheme_seperator = unicode(settings.value("Ann/MorphSep", QtCore.QVariant("-")).toString())
        #self.str_gloss_sepereator = unicode(settings.value("Ann/GlossSep",  QtCore.QVariant(":")).toString())
        self.str_empty_character = unicode(settings.value("Ann/EmptyChar",  QtCore.QVariant("#")).toString())

    def init_connects(self):
        # Projects
        #QtCore.QObject.connect(self.ui.actionNew, QtCore.SIGNAL("triggered()"), self.new_project)
        #QtCore.QObject.connect(self.ui.actionOpen, QtCore.SIGNAL("triggered()"), self.open_project)
        #QtCore.QObject.connect(self.ui.actionSaveAs, QtCore.SIGNAL("triggered()"), self.saveProjectAs)
        #QtCore.QObject.connect(self.ui.actionSave, QtCore.SIGNAL("triggered()"), self.save_project)

        # Files
        QtCore.QObject.connect(self.ui.actionOpenFile, QtCore.SIGNAL("triggered()"), self.open_file)
        QtCore.QObject.connect(self.ui.actionSaveFile, QtCore.SIGNAL("triggered()"), self.save_file)
        QtCore.QObject.connect(self.ui.actionSaveFileAs, QtCore.SIGNAL("triggered()"), self.save_file_as)
        QtCore.QObject.connect(self.ui.actionNewFile, QtCore.SIGNAL("triggered()"), self.new_file)
        #QtCore.QObject.connect(self.ui.actionRemoveFile, QtCore.SIGNAL("triggered()"), self.remove_file)
        #self.ui.toolbuttonRemoveFile.setDefaultAction(self.ui.actionRemoveFile)

        QtCore.QObject.connect(self.ui.actionQuit, QtCore.SIGNAL("triggered()"), self.close)
        QtCore.QObject.connect(self.ui.actionAboutPoioGRAID, QtCore.SIGNAL("triggered()"), self.about_dialog)
        QtCore.QObject.connect(self.ui.actionInsertUtterance, QtCore.SIGNAL("triggered()"), self.insert_utterance_after_current)
        QtCore.QObject.connect(self.ui.actionDeleteUtterance, QtCore.SIGNAL("triggered()"), self.delete_current_utterance)
        QtCore.QObject.connect(self.ui.actionInsertWord, QtCore.SIGNAL("triggered()"), self.insert_word_after_current)
        QtCore.QObject.connect(self.ui.actionDeleteWord, QtCore.SIGNAL("triggered()"), self.delete_current_word)

        #QtCore.QObject.connect(self.ui.listwidgetUtterances, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.set_tier_utterances)
        #QtCore.QObject.connect(self.ui.listwidgetWords, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.set_tier_words)
        #QtCore.QObject.connect(self.ui.listwidgetWfw, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.set_tier_wfw)
        #QtCore.QObject.connect(self.ui.listwidgetGraid1, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.set_tier_graid1)
        #QtCore.QObject.connect(self.ui.listwidgetGraid2, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.set_tier_graid2)
        #QtCore.QObject.connect(self.ui.listwidgetTranslations, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.set_tier_translations)

        #QtCore.QObject.connect(self.ui.pushbuttonNewTierWfw, QtCore.SIGNAL("clicked()"), self.new_tier_wfw)
        #QtCore.QObject.connect(self.ui.pushbuttonNewTierGraid1, QtCore.SIGNAL("clicked()"), self.new_tier_graid1)
        #QtCore.QObject.connect(self.ui.pushbuttonNewTierGraid2, QtCore.SIGNAL("clicked()"), self.new_tier_graid2)
        #QtCore.QObject.connect(self.ui.pushbuttonNewTierTranslations, QtCore.SIGNAL("clicked()"), self.new_tier_translations)

    def about_dialog(self):
        about = QtGui.QMessageBox(self)
        about.setTextFormat(QtCore.Qt.RichText)
        about.setWindowTitle(self.tr("About PoioGRAID"))
        about.setText(self.tr("<b>PoioGRAID 0.1.0</b><br/>Poio GRAID Editor by the <a href=\"http://www.cidles.eu\">Interdisciplinary Centre for Social and Language Documentation</a>.<br/><br/>All rights reserved. See LICENSE file for details.<br/><br/>For more information visit the website:<br/><a href=\"http://www.cidles.eu/ltll/poio\">http://www.cidles.eu/ltll/poio</a>"))
        about.exec_()

    def update_textedit(self):
        self.ui.textedit.clear()
        self.ui.textedit.append_title(self.title)

        for element in self.annotation_tree.elements():
            self.ui.textedit.append_element(element, self.annotation_tree.structure_type_handler)

        self.ui.textedit.scrollToAnchor("title")

    def delete_current_utterance(self):
        pass

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

    def new_file(self):
        dialog = QtGui.QDialog(self)
        ui = Ui_NewFileGraid()
        ui.setupUi(dialog)
        ret = dialog.exec_()
        if ret == 1:
            if ui.radioButtoTbStyleText.isChecked():
                self._parse_tb_style_text(unicode(ui.textedit.document().toPlainText()))
            else:
                print "plain text"
        self.update_textedit()

    def _parse_tb_style_text(self, text):
        block = list()

        lines = text.split("\n")
        line = lines.pop(0)
        title = []
        while not line.startswith("\\"):
            if line:
                title.append(line)
            line = lines.pop(0)

        self.title = " ".join(title)

        for line in lines:
            if line and line.startswith("\\id") and len(block):
                utterance = self._parse_element_from_tb_style(block)
                self.annotation_tree.append_element_without_ids(utterance)
                block = list()
            elif line:
                if line.startswith("\\"):
                    block.append(line.strip())

        print self.annotation_tree.tree

    def _parse_element_from_tb_style(self, block):
        element_tb = dict()
        utterance = ""
        translation = ""
        comment = ""

        for line in block:
            line = re.sub(" +", " ", line)
            line = line.strip()
            line_elements = line.split(None, 1)
            if len(line_elements) < 2:
                type = line
                text = ""
            else:
                type = line_elements[0]
                text = line_elements[1]

            if type.startswith("\\"):
                if type[1:] == "sl":
                    #text = re.sub("\(\d+\) ?", "", text)
                    utterance = text
                    utterance = re.sub("\d# ?", "", utterance)
                    utterance = re.sub(" +", " ", utterance)
                    utterance = utterance.strip()

                if type[1:] == "ft":
                    translation = text

                elif type[1:] == "com":
                    comment = text

                else:
                    #text = re.sub("^x ", "", text)
                    element_tb[type[1:]] = list()
                    last_start = 0
                    for m in re.finditer("(?:\d#|$)", text):
                        element_tb[type[1:]].append(text[last_start:m.start(0)])
                        last_start = m.end(0)
        elements = []
        for i, phrase in enumerate(element_tb['sl']):
            words = phrase.split()
            wfw = element_tb['wfw'][i].split()
            graid1 = element_tb['gr_1'][i].split()
            graid2 = element_tb['gr_2'][i]
            il_elements = []
            for i in range(max(len(words), len(wfw), len(graid1))):
                e1 = ''
                e2 = ''
                e3 = ''
                if i < len(words):
                    e1 = words[i]
                if i < len(wfw):
                    e2 = wfw[i]
                if i < len(graid1):
                    e3 = graid1[i]
                il_elements.append([e1, e2, e3])

            elements.append([ phrase, il_elements, graid2 ])

        return [ utterance, elements, translation, comment]

    def save_file(self):
        pass

    def save_file_as(self):
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

    def open_file(self):
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

