# -*- coding: utf-8 -*-
# (C) 2009-2012 copyright by Peter Bouda

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
        #self.init_settings()

        self.init = 0

        self.ui.textedit.append_title(
            self.tr("Please create or open a file..."))

    def init_vars(self):
        self.annotation_tree = pyannotation.annotationtree.AnnotationTree(
            pyannotation.data.GRAID)
        self.ui.textedit.structure_type_handler = \
            self.annotation_tree.structure_type_handler

        self.filename = ''
        self.title = ''

    def init_settings(self):
        QtCore.QCoreApplication.setOrganizationName(
            "Interdisciplinary Centre for Social and Language Documentation");
        QtCore.QCoreApplication.setOrganizationDomain("cidles.eu");
        QtCore.QCoreApplication.setApplicationName("PoioGRAID");
        settings = QtCore.QSettings()
        #self.str_empty_character = unicode(
        #    settings.value("Ann/EmptyChar",  QtCore.QVariant("#")).toString())

    def init_connects(self):
        # Files
        self.ui.actionOpenFile.triggered.connect(self.open_file)
        self.ui.actionSaveFile.triggered.connect(self.save_file)
        self.ui.actionSaveFileAs.triggered.connect(self.save_file_as)
        self.ui.actionNewFile.triggered.connect(self.new_file)

        # Application stuff
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionAboutPoioGRAID.triggered.connect(self.about_dialog)

        # insert and delete tables and columns
        #QtCore.QObject.connect(self.ui.actionInsertUtterance, QtCore.SIGNAL("triggered()"), self.insert_utterance_after_current)
        #QtCore.QObject.connect(self.ui.actionDeleteUtterance, QtCore.SIGNAL("triggered()"), self.delete_current_utterance)
        self.ui.actionInsertColumnBefore.triggered.connect(
            self.insert_column_before)
        self.ui.actionInsertColumnAfter.triggered.connect(
            self.insert_column_after)
        self.ui.actionDeleteColumn.triggered.connect(self.delete_column)

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
            self.ui.textedit.append_element(element)

        self.ui.textedit.scrollToAnchor("title")

    def delete_utterance(self):
        pass

    def insert_utterance_after(self):
        pass

    def delete_column(self):
        self.ui.textedit.delete_column_at_cursor()

    def insert_column_before(self):
        self.ui.textedit.insert_column_at_cursor(
            self.annotation_tree.next_annotation_id, False)

    def insert_column_after(self):
        self.ui.textedit.insert_column_at_cursor(
            self.annotation_tree.next_annotation_id, True)

    def new_file(self):
        dialog = QtGui.QDialog(self)
        ui = Ui_NewFileGraid()
        ui.setupUi(dialog)
        ret = dialog.exec_()
        if ret == 1:
            if ui.radioButtoTbStyleText.isChecked():
                self._parse_tb_style_text(
                    unicode(ui.textedit.document().toPlainText()))
            else:
                print "plain text"
        self.update_textedit()

    def save_file(self):
        tree = self.ui.textedit.anntation_tree_from_document(
            self.annotation_tree.structure_type_handler)
        print tree

    def save_file_as(self):
        filepath = QtGui.QFileDialog.getSaveFileName(
            self,
            self.tr("Export File"),
            "",
            self.tr("Elan files (*.eaf);;All files (*.*)"))
        filepath = unicode(filepath)
        if filepath != '':
            pass

    def open_file(self):
        filepath = QtGui.QFileDialog.getOpenFileName(
            self,
            self.tr("Add File"),
            "",
            self.tr("Elan files (*.eaf);;All files (*.*)"))
        filepath = unicode(filepath)
        if filepath != '':
            pass


    # Private functions #######################################################

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

        utterance = self._parse_element_from_tb_style(block)
        self.annotation_tree.append_element_without_ids(utterance)

        print self.annotation_tree.tree

    def _parse_element_from_tb_style(self, block):
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
                il_elements.append([e1, e2, e3])

            elements.append([ phrase, il_elements, graid2 ])

        return [ utterance, elements, translation, comment]

