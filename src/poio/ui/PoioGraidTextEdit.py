# -*- coding: utf-8 -*-
# (C) 2009 copyright by Peter Bouda

import os, re
from PyQt4 import QtCore, QtGui
#from evoque.template import Template
from xml import etree

class PoioGraidTextEdit(QtGui.QTextEdit):

    def __init__(self, parent):
        QtGui.QTextEdit.__init__(self, parent)
        self.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.setAcceptRichText(False)
        self.setUndoRedoEnabled(True)

        #self.setStyleSheet(".match { color:green; }")

        #palette = self.palette()
        #palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, QtGui.QColor("yellow"))
        #self.setPalette(palette)

        QtCore.QObject.connect(self, QtCore.SIGNAL("cursorPositionChanged()"), self.check_cursor_position)

    def keyPressEvent(self, event):
        c = self.textCursor()
        t = c.currentTable()
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter \
            or t == None or c.charFormat().fontCapitalization()==QtGui.QFont.SmallCaps:
            event.accept()
        else:
            QtGui.QTextEdit.keyPressEvent(self, event)

    def insertFromMimeData(self, source):
        text = unicode(source.text())
        text = re.sub(r"[\r\n\a]", "", text)
        self.insertPlainText(text)
        #QtGui.QTextEdit.insertFromMimeData(self, source)
        
    def check_cursor_position(self):
        c = self.textCursor()
        t = c.currentTable()
        if t == None or c.charFormat().fontCapitalization()==QtGui.QFont.SmallCaps:
            self.setCursorWidth(0)
        else:
            self.setCursorWidth(1)

    def append_title(self, title):
        self.setDocumentTitle(title)
        # margin is not working :-(
        self.append("<div style=\"font-size:14pt;\">&nbsp;</div>")
        self.append("<div style=\"font-size:14pt;font-weight:bold;text-decoration:underline;\" id=\"title\" class=\"title\">" + title + "</div>")

    def append_element(self, element, structure_type_handler):
        c = self.textCursor()
        c.movePosition(QtGui.QTextCursor.End)

        # create table
        count_rows = structure_type_handler.nr_of_tiers
        table = c.insertTable(count_rows, 2)
        format = table.format()
        format.setCellPadding(2)
        format.setCellSpacing(-1)
        format.setTopMargin(10)
        format.setBorder(1)
        format.setBorderStyle(QtGui.QTextFrameFormat.BorderStyle_Solid)
        table.setFormat(format)

        self._insert_annotation_cell(element,
                                     structure_type_handler.flat_data_hierarchy,
                                     structure_type_handler.data_hierarchy,
                                     table,
                                     1)

        for i, row_name in enumerate(structure_type_handler.flat_data_hierarchy):
            c = table.cellAt(i, 0)
            format = c.format()
            format.setFontCapitalization(QtGui.QFont.SmallCaps)
            format.setForeground(QtGui.QBrush(QtGui.QColor(150, 150, 150)))
            c.setFormat(format)
            c.firstCursorPosition().insertText(row_name)

    def _insert_annotation_cell(self, elements, flat_hierarchy, hierarchy, table, column):
        inserted = 0
        for i, t in enumerate(hierarchy):
            if type(t) is list:
                elements_list = elements[i]
                for i, e in enumerate(elements_list):
                    inserted += self._insert_annotation_cell(e, flat_hierarchy, t, table, column + i + inserted)
                inserted = inserted + len(elements_list) - 1
                merge_rows = [ r for r in hierarchy if type(r) is not list]
                for r in merge_rows:
                    row = flat_hierarchy.index(r)
                    table.mergeCells(row, column, 1, inserted + 1)
            else:
                row = flat_hierarchy.index(t)
                self._insert_annotation_cell2(elements[i], table, row, column)

        return inserted

    def _insert_annotation_cell2(self, e, table, row, column):
        if (column + 1) > table.columns():
            table.appendColumns(1)
        c = table.cellAt(row, column)
        c.firstCursorPosition().insertText(e['annotation'])
        f = c.format()
        f.setAnchorNames([unicode(e['id'])])
        c.setFormat(f)

    def anntation_tree_from_document(self, structure_type_handler):
        root = self.document().rootFrame()
        #string_document_text = unicode(self.document().toPlainText())
        tree = []
        for frame in root.childFrames():
            if frame.__class__.__name__ == "QTextTable":
                utterance = list()
                self._annotation_cell(utterance,
                    structure_type_handler.flat_data_hierarchy,
                    structure_type_handler.data_hierarchy,
                    frame,
                    0, 1, frame.columns()-1)
                tree.append(utterance)
        return tree

    def _annotation_cell(self, elements, flat_hierarchy, hierarchy, table, row, column, column_span):
        #processed = 0
        for i, t in enumerate(hierarchy):
            if type(t) is list:
                sub_tree = list()
                column_add = 0
                while column_add < column_span:
                    c = table.cellAt(row, column + column_add)
                    sub_element = list()
                    self._annotation_cell(sub_element, flat_hierarchy, t, table, row, column + column_add, c.columnSpan())
                    sub_tree.append(sub_element)
                    column_add += c.columnSpan()
                elements.append(sub_tree)
            else:
                row = flat_hierarchy.index(t)
                e = self._annotation_cell2(table, row, column)
                elements.append(e)

                row += 1

        #return processed

    def _annotation_cell2(self, table, row, column):
        element = dict()
        c = table.cellAt(row, column)
        start = int(c.firstCursorPosition().position())
        end = int(c.lastCursorPosition().position())
        element['id'] = int(unicode(c.format().anchorNames()[0]))
        element['annotation'] = unicode(self.document().toPlainText())[start:end]
        return element
