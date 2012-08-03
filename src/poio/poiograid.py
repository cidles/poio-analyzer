# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2001-2012 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://www.cidles.eu/ltll/poio>
# For license information, see LICENSE.TXT

import re
import pickle
from PyQt4 import QtCore, QtGui

import pyannotation.annotationtree
import pyannotation.data

#from poio.ui.PoioGraidTextEdit import PoioGraidTextEdit
from poio.ui.Ui_MainWindowGRAID import Ui_MainWindow
from poio.ui.Ui_NewFileGraid import Ui_NewFileGraid
from poio.ui.FindReplaceDialog import FindReplaceDialog
from poio.ui.FindDialog import FindDialog


class PoioGRAID(QtGui.QMainWindow):
    """The main window of the PoioGRAID application."""

    def __init__(self, *args):
        """
        The consctructor of the main application object, i.e. the main window.
        Calls a lot of other init methods.
        """
        QtGui.QMainWindow.__init__(self, *args)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init_vars()
        self.init_connects()
        self.init_settings()

        self.init = 0

        self.ui.textedit.append_title(
            self.tr("Please create or open a file..."))

        self._dialog_find_and_replace = FindReplaceDialog(self)
        self._dialog_find_and_replace.setModal(False)
        self._dialog_find_and_replace.set_text_edit(self.ui.textedit)

        self._dialog_find = FindDialog(self)
        self._dialog_find.setModal(False)
        self._dialog_find.set_text_edit(self.ui.textedit)

    def init_vars(self):
        """
        Initializes several attributes of the application, for example
        creates an empty annotation tree and a data structure type.
        """
        self.annotation_tree = pyannotation.annotationtree.AnnotationTree(
            pyannotation.data.GRAID)
        self.ui.textedit.structure_type_handler = \
            self.annotation_tree.structure_type_handler

        self.filepath = None
        self.title = ''

    def init_settings(self):
        """
        Load application settings from QSettings object.
        """
        QtCore.QCoreApplication.setOrganizationName(
            "Interdisciplinary Centre for Social and Language Documentation");
        QtCore.QCoreApplication.setOrganizationDomain("cidles.eu");
        QtCore.QCoreApplication.setApplicationName("PoioGRAID");
        settings = QtCore.QSettings()
        settings.setValue("FontZoom", 100)

    def init_connects(self):
        """
        Initializes all signal/slots connections of the application.
        """

        # Files
        self.ui.actionOpenFile.triggered.connect(self.open_file)
        self.ui.actionSaveFile.triggered.connect(self.save_file)
        self.ui.actionSaveFileAs.triggered.connect(self.save_file_as)
        self.ui.actionNewFile.triggered.connect(self.new_file)

        # Application stuff
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionAboutPoioGRAID.triggered.connect(self.about_dialog)

        # insert and delete tables and columns
        self.ui.actionInsertUtteranceAfter.triggered.connect(
            self.insert_utterance_after)
        self.ui.actionInsertUtteranceBefore.triggered.connect(
            self.insert_utterance_before)
        self.ui.actionDeleteUtterance.triggered.connect(
            self.delete_utterance)

        self.ui.actionInsertColumnBefore.triggered.connect(
            self.insert_column_before)
        self.ui.actionInsertColumnAfter.triggered.connect(
            self.insert_column_after)
        self.ui.actionDeleteColumn.triggered.connect(self.delete_column)

        # find and replace
        self.ui.actionFindAndReplace.triggered.connect(
            self.find_and_replace)
        self.ui.actionFind.triggered.connect(self.find)

    def about_dialog(self):
        """
        Display the About dialog.
        """
        about = QtGui.QMessageBox(self)
        about.setTextFormat(QtCore.Qt.RichText)
        about.setWindowTitle(self.tr("About PoioGRAID"))
        about.setText(self.tr("<b>PoioGRAID 0.1.0</b><br/>Poio GRAID Editor "
                              "by the <a href=\"http://www.cidles.eu\">"
                              "Interdisciplinary Centre for Social and "
                              "Language Documentation</a>.<br/><br/>All "
                              "rights reserved. See LICENSE file for details."
                              "<br/><br/>For more information visit the "
                              "website:<br/><a href=\"http://www.cidles.eu/"
                              "ltll/poio\">http://www.cidles.eu/ltll/poio"
                              "</a>"))
        about.exec_()

    def update_textedit(self):
        """
        Updates the text edit view with the data from the annotation tree.
        """
        self.ui.textedit.clear()
        self.ui.textedit.append_title(self.title)

        for element in self.annotation_tree.elements():
            self.ui.textedit.append_element(element)

        self.ui.textedit.scrollToAnchor("title")

    def delete_utterance(self):
        """
        Delete one utterance from the text edit widget and from the annotation
        tree.
        """
        deleted_id = self.ui.textedit.delete_current_element()
        if deleted_id:
            self.annotation_tree.remove_element_with_id(deleted_id)

    def insert_utterance_before(self):
        """
        Insert an utteranance *before* the currently edited utterance in the
        text view. Then adds the utterance to the annotation tree.
        """
        element = self.annotation_tree.empty_element()
        current_id = self.ui.textedit.insert_element(element)
        if current_id:
            self.annotation_tree.insert_element(element, current_id)

    def insert_utterance_after(self):
        """
        Insert an utteranance *after* the currently edited utterance in the
        text view. Then adds the utterance to the annotation tree.
        """
        element = self.annotation_tree.empty_element()
        current_id = self.ui.textedit.insert_element(element, True)
        if current_id:
            self.annotation_tree.insert_element(element, current_id, True)

    def delete_column(self):
        """
        Deletes the column that is currently edited in the text view. Also
        remove all annotation and sub-elements belonging to this column.
        Then delete the elements from the annotation tree.
        """
        self.ui.textedit.delete_column_at_cursor()

    def insert_column_before(self):
        """
        Inserts an empty column at the current cursor position *before* the
        currently edited element. Then insert the element into the annotation
         tree.
        """
        next_id = self.ui.textedit.insert_column_at_cursor(
            self.annotation_tree.next_annotation_id, False)
        self.annotation_tree.next_annotation_id = next_id

    def insert_column_after(self):
        """
        Inserts an empty column at the current cursor position *after* the
        currently edited element. Then insert the element into the annotation
         tree.
        """
        next_id = self.ui.textedit.insert_column_at_cursor(
            self.annotation_tree.next_annotation_id, True)
        self.annotation_tree.next_annotation_id = next_id

    def new_file(self):
        """
        Create a new file from a given input text. The user has to enter the
        text in an input dialog. There are two types of input text: plain text
        or tb style text (with markup like ``\sl`` at the beginning of lines).
        """
        dialog = QtGui.QDialog(self)
        ui = Ui_NewFileGraid()
        ui.setupUi(dialog)
        ret = dialog.exec_()
        if ret == QtGui.QDialog.Accepted:
            self.annotation_tree = pyannotation.annotationtree.AnnotationTree(
                pyannotation.data.GRAID)
            self.title = ""
            self.statusBar().showMessage(self.tr("Parsing text..."), 5)
            if ui.radioButtoTbStyleText.isChecked():
                self._parse_tb_style_text(
                    unicode(ui.textedit.document().toPlainText()))
            else:
                self._parse_plain_text(
                    unicode(ui.textedit.document().toPlainText()))
            self.statusBar().showMessage(self.tr("Parsing done."), 5)
            self.update_textedit()

    def save_file(self):
        """
        Save the current data into a file. If no filename is specified yet
        then ask for the path and filename by opening a file dialog.
        """
        if not self.filepath:
            self.save_file_as()
        else:
            tree = self.ui.textedit.annotation_tree_from_document()
            file = open(self.filepath, "wb")
            pickle.dump(tree, file)
            file.close()
            self.statusBar().showMessage(self.tr("File saved."), 5)


    def save_file_as(self):
        """
        Open a file dialog and ask for path and filename for the file. Then
        call `PoioGRAID.save_file()`.
        """
        filepath = QtGui.QFileDialog.getSaveFileName(
            self,
            self.tr("Save File As"),
            "",
            self.tr("Pickle file (*.pickle);;All files (*.*)"))
        filepath = unicode(filepath)
        if filepath != '':
            if not filepath.endswith(".pickle"):
                filepath += ".pickle"
            self.filepath = filepath
            self.save_file()
        else:
            return

    def open_file(self):
        """
        Display a file dialog and let the user choose a file. Load the data
        into the annotation tree and then update the text edit widget.
        """
        filepath = QtGui.QFileDialog.getOpenFileName(
            self,
            self.tr("Add File"),
            "",
            self.tr("Pickle files (*.pickle);;All files (*.*)"))
        filepath = unicode(filepath)
        if filepath != '':
            file = open(filepath, "rb")
            self.annotation_tree.tree = pickle.load(file)
            file.close()
            self.update_textedit()
            self.filepath = filepath
            print self.annotation_tree.tree

    def find_and_replace(self):
        self._dialog_find_and_replace.show()

    def find(self):
        self._dialog_find.show()

    # Private functions #######################################################

    def _parse_plain_text(self, text):
        """
        Parses plain text data into an annotation tree.
        """
        lines = text.split("\n")

        progress = QtGui.QProgressDialog(self.tr("Parsing text..."), self.tr("Abort"), 0, len(lines), self.parent())
        progress.setWindowModality(QtCore.Qt.WindowModal)

        for i, line in enumerate(lines):
            progress.setValue(i)

            line = line.strip()
            utterance = line
            clause_unit = re.sub("[.,;:]", "", line)
            words = clause_unit.split()

            il_elements = list()
            for w in words:
                il_elements.append([
                        { 'id' : self.annotation_tree.next_annotation_id,
                          'annotation' :  w },
                        { 'id' : self.annotation_tree.next_annotation_id,
                          'annotation' : '' },
                        { 'id' : self.annotation_tree.next_annotation_id,
                          'annotation' : '' }])

            elements = [ [
                { 'id' : self.annotation_tree.next_annotation_id,
                  'annotation' : clause_unit },
                il_elements,
                { 'id' : self.annotation_tree.next_annotation_id,
                  'annotation' : '' }] ]

            utterance = [ { 'id' : self.annotation_tree.next_annotation_id,
                            'annotation' : utterance },
                          elements,
                          { 'id' : self.annotation_tree.next_annotation_id,
                            'annotation' : '' },
                          { 'id' : self.annotation_tree.next_annotation_id,
                            'annotation' : '' } ]

            self.annotation_tree.append_element(utterance)
            if (progress.wasCanceled()):
                initCorpusReader()
                break

        progress.setValue(len(lines))

    def _parse_tb_style_text(self, text):
        """
        Parses tb style data into an annotation tree. In tb style data lines
        start with markup like ``\sl``.
        """
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
                self.annotation_tree.append_element(utterance)
                block = list()
            elif line:
                if line.startswith("\\"):
                    block.append(line.strip())

        utterance = self._parse_element_from_tb_style(block)
        self.annotation_tree.append_element(utterance)

        #print self.annotation_tree.tree

    def _parse_element_from_tb_style(self, block):
        """
        Helper function for `PoioGRAID._parse_tb_style_text()`. Parse one
        paragraph of tb style data.
        """
        element_tb = dict()
        utterance = u""
        translation = u""
        comment = u""

        for line in block:
            line = re.sub(" +", " ", line)
            line = line.strip()
            line_elements = line.split(None, 1)
            if len(line_elements) < 2:
                type = line
                text = u""
            else:
                type = line_elements[0]
                text = line_elements[1]

            if type.startswith("\\"):
                if type[1:] == "sl":
                    #text = re.sub("\(\d+\) ?", "", text)
                    utterance = text
                    utterance = re.sub("\d?# ?", "", utterance)
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
                    for m in re.finditer("(?:\d?#|$)", text):
                        element_tb[type[1:]].append(
                            text[last_start:m.start(0)])
                        last_start = m.end(0)
        elements = []
        for i, phrase in enumerate(element_tb['sl']):
            words = phrase.split()
            wfw = []
            try:
                wfw = element_tb['wfw'][i].split()
            except IndexError:
                pass
            except KeyError:
                pass

            graid1 = []
            try:
                graid1 = element_tb['gr_1'][i].split()
            except IndexError:
                pass
            except KeyError:
                pass

            graid2 = ''
            try:
                graid2 = element_tb['gr_2'][i]
            except IndexError:
                pass
            except KeyError:
                pass

            il_elements = []
            for i in range(max(len(words), len(wfw), len(graid1))):
                e1 = u''
                e2 = u''
                e3 = u''
                if i < len(words):
                    e1 = words[i]
                if i < len(wfw):
                    e2 = wfw[i]
                if i < len(graid1):
                    e3 = graid1[i]
                il_elements.append([
                    { 'id' : self.annotation_tree.next_annotation_id,
                      'annotation' :  e1 },
                    { 'id' : self.annotation_tree.next_annotation_id,
                      'annotation' : e2 },
                    { 'id' : self.annotation_tree.next_annotation_id,
                      'annotation' : e3 }])

            elements.append([
                { 'id' : self.annotation_tree.next_annotation_id,
                  'annotation' : phrase },
                il_elements,
                { 'id' : self.annotation_tree.next_annotation_id,
                  'annotation' : graid2 }])

        return [ { 'id' : self.annotation_tree.next_annotation_id,
                   'annotation' : utterance },
                  elements,
                  { 'id' : self.annotation_tree.next_annotation_id,
                    'annotation' : translation },
                  { 'id' : self.annotation_tree.next_annotation_id,
                    'annotation' : comment } ]

