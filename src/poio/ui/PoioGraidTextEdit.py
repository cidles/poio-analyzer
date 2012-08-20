# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2012 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://www.cidles.eu/ltll/poio>
# For license information, see LICENSE.TXT

from __future__ import unicode_literals
import re
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFont, QApplication

class NoStructureTypeHandlerError(Exception): pass

class PoioGraidTextEdit(QtGui.QTextEdit):

    FIRST_DATA_COLUMN = 2
    ROW_NAMES_COLUMNS = 1
    NUMBERS_COLUMN = 0

    def __init__(self, parent):
        """
        Initializes the Text Edit
        """
        QtGui.QTextEdit.__init__(self, parent)
        self.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.setAcceptRichText(False)
        self.setUndoRedoEnabled(True)
        self.setTabChangesFocus(True)
        self.structure_type_handler = None

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, QtGui.QColor("yellow"))
        self.setPalette(palette)

        #self.setStyleSheet(".match { color:green; }")

        cursor = self.textCursor()
        cursor.setPosition(0)
        self.setTextCursor(cursor)

        QtCore.QObject.connect(
            self, QtCore.SIGNAL("cursorPositionChanged()"),
            self.check_cursor_position)

    def keyPressEvent(self, event):
        """
        Event handler for "Return Key", "Enter Key" and "Tab Key"

        ...

        Parameters
        ----------
        event : QEvent
        """
        c = self.textCursor()
        t = c.currentTable()

        if not t or \
                c.charFormat().fontCapitalization() == QtGui.QFont.SmallCaps:
            event.accept()
            return

        if event.key() == QtCore.Qt.Key_Return or \
                event.key() == QtCore.Qt.Key_Enter or \
                event.key() == QtCore.Qt.Key_Tab:
            cell = t.cellAt(c)
            if cell.column() + cell.columnSpan() == t.columns():
                pass
            else:
                c.movePosition(QtGui.QTextCursor.NextCell)
            if c.charFormat().fontCapitalization() == QtGui.QFont.SmallCaps:
                c.movePosition(QtGui.QTextCursor.NextCell)

            self.setTextCursor(c)
            event.accept()
            return

        QtGui.QTextEdit.keyPressEvent(self, event)

    def insertFromMimeData(self, source):
        """
        Insert text from Mime Data

        ...

        Parameters
        ----------
        source : QMimeData
        """
        text = source.text()
        text = re.sub(r"[\r\n\a]", "", text)
        self.insertPlainText(text)
        #QtGui.QTextEdit.insertFromMimeData(self, source)
        
    def check_cursor_position(self):
        """
        Check the cursor position
        """
        c = self.textCursor()
        t = c.currentTable()

        if not t or \
                c.charFormat().fontCapitalization() == QtGui.QFont.SmallCaps:
            self.setCursorWidth(0)
        else:
            self.setCursorWidth(1)

    def insert_column_at_cursor(self, id, after):
        """
        Inserts column before or after the current cursor position.

        ...

        Parameters
        ----------
        id : int
        after : bool

        """
        if not self.structure_type_handler:
            raise NoStructureTypeHandlerError

        cursor = self.textCursor()
        table = cursor.currentTable()
        if table:
            cell = table.cellAt(cursor)
            r = cell.row()
            c = cell.column()
            c_span = cell.columnSpan()
            type = self.structure_type_handler.flat_data_hierarchy[r]

            # check if the cursor is in utterance or an annotation of the
            # same level
            for s in self.structure_type_handler.get_siblings_of_type(
                    "utterance"):
                if r == self.structure_type_handler.flat_data_hierarchy.\
                        index(s):
                    return id

            if r >  0 and c > 0:
                new_column_pos = c
                if after:
                    new_column_pos = c + c_span
                else:
                    c += 1
                table.splitCell(0,0,1,1)
                table.insertColumns(new_column_pos, 1)
                table.mergeCells(0,0,8,1)
                # set text format to normal text and add id
                for row in range(table.rows()):
                    new_cell = table.cellAt(row, new_column_pos)
                    f = new_cell.format()
                    f.setFontCapitalization(QtGui.QFont.MixedCase)
                    f.setForeground(QtGui.QBrush("black"))
                    f.setAnchorNames([str(id)])
                    new_cell.setFormat(f)
                    id += 1

                for p in self.structure_type_handler.get_parents_of_type(type):
                    r_parent = self.structure_type_handler.\
                        flat_data_hierarchy.index(p)
                    cell_parent = table.cellAt(r_parent, c)
                    c_parent = cell_parent.column()
                    c_span_parent = cell_parent.columnSpan()
                    # if this cell was appended after the parent cell
                    # then merge in parent row
                    if after:
                        if (c_parent + c_span_parent) == c + c_span:
                            table.mergeCells(r_parent,
                                c_parent, 1, c_span_parent + 1)
                    # if this cell was inserted before parent then merge
                    # parent now
                    else:
                        if c_parent == c:
                            table.mergeCells(r_parent,
                                c_parent - 1, 1, c_span_parent + 1)
        return id

    def delete_column_at_cursor(self):
        """
        Removes the column with the current cursor.
        """
        cursor = self.textCursor()
        table = cursor.currentTable()
        if table:
            cell = table.cellAt(cursor)
            if cell.row() >= PoioGraidTextEdit.FIRST_DATA_COLUMN \
                and cell.column() >= PoioGraidTextEdit.FIRST_DATA_COLUMN:
                #print cell.column()
                #print cell.columnSpan()
                for i in range(cell.columnSpan()):
                    table.removeColumns(cell.column(), 1)
                #table.removeColumns(cell.column(), cell.columnSpan() + 1)
                #print unicode(table.document().toPlainText()).encode("utf-8")

    def delete_current_cell(self, merge_cells = False):
        """
        Removes the cell with the current cursor.
        """
        cursor = self.textCursor()
        table = cursor.currentTable()
        if table:
            cell = table.cellAt(cursor)
            r = cell.row()
            c = cell.column()
            c_span = cell.columnSpan()
            if r > 0:
                parent_cell = table.cellAt(r - 1, c)
                # do not delete if this cell already spans all columns of parent
                if parent_cell.columnSpan() > c_span:
                    if not merge_cells:
                        # remove the text in the cell
                        cursor.setPosition(
                            cell.firstCursorPosition().position())
                        cursor.setPosition(
                            cell.lastCursorPosition().position(),
                            QtGui.QTextCursor.KeepAnchor)
                        cursor.removeSelectedText()

                    # merge the cells
                    start_merge_column = c
                    # if this cell is not the last element of parent then we merge with previous neighbour
                    # otherwise we merge with next neighbour
                    if (parent_cell.column() + parent_cell.columnSpan()) == \
                            (c + c_span):
                        neighbour_cell = table.cellAt(r, c - 1)
                        start_merge_column = neighbour_cell.column()
                    else:
                        neighbour_cell = table.cellAt(r, c + c_span)
                    table.mergeCells(
                        r, start_merge_column, 1,
                        c_span + neighbour_cell.columnSpan())

    def append_title(self, title):
        """
        Add title to the document

        ...

        Parameters
        ----------
        title : str
        """
        self.setDocumentTitle(title)
        # margin is not working :-(
        self.append("<div style=\"font-size:14pt;\">&nbsp;</div>")
        self.append("<div style=\"font-size:14pt;font-weight:bold;text-decoration:underline;\" id=\"title\" class=\"title\">" + title + "</div>")

    def delete_current_element(self):
        """
        Remove element with the current cursor
        """
        cursor = self.textCursor()
        table = cursor.currentTable()
        current_id = None
        if table:
            cell = table.cellAt(0, PoioGraidTextEdit.FIRST_DATA_COLUMN)
            f = cell.format()
            current_id = f.anchorNames()[0]
            cursor.setPosition(table.firstPosition() - 1)
            cursor.setPosition(
                table.lastPosition() + 1, QtGui.QTextCursor.KeepAnchor)
            cursor.removeSelectedText()
        return current_id

    def insert_element(self, element, after = False):
        """
        Adds element at the current cursor

        ...

        Parameters
        ----------
        element : list
        after : bool
        """
        if not self.structure_type_handler:
            raise NoStructureTypeHandlerError

        c = self.textCursor()
        table = c.currentTable()

        current_id = None

        if table:
            cell = table.cellAt(0, PoioGraidTextEdit.FIRST_DATA_COLUMN)
            f = cell.format()
            current_id = f.anchorNames()[0]
            if after:
                pos = table.lastPosition() + 1
            else:
                pos = table.firstPosition() - 1

            self._insert_element_at_position(element, pos)
            self.update_numbers()

        return current_id

    def append_element(self, element):
        """
        Adds element at the end of the file

        ...

        Parameters
        ----------
        element : list
        """
        if not self.structure_type_handler:
            raise NoStructureTypeHandlerError

        c = self.textCursor()
        c.movePosition(QtGui.QTextCursor.End)
        table = self._insert_element_at_position(element, c.position())

        number = 0
        root = self.document().rootFrame()
        for frame in root.childFrames():
            if frame.__class__.__name__ == "QTextTable":
                number += 1
        self._update_number_of_table(table, number)

    def _insert_element_at_position(self, element, pos):
        """
        Adds element at the given position

        ...

        Parameters
        ----------
        element : list
        pos : int
        """
        c = self.textCursor()
        c.setPosition(pos)

        # create table
        count_rows = self.structure_type_handler.nr_of_types
        table = c.insertTable(count_rows,
            PoioGraidTextEdit.FIRST_DATA_COLUMN + 1)
        format = table.format()
        format.setCellPadding(2)
        format.setCellSpacing(-1)
        format.setTopMargin(10)
        format.setBorder(1)
        format.setBorderStyle(QtGui.QTextFrameFormat.BorderStyle_Solid)
        table.setFormat(format)

        self._insert_annotation_cell(element,
            self.structure_type_handler.flat_data_hierarchy,
            self.structure_type_handler.data_hierarchy,
            table,
            PoioGraidTextEdit.FIRST_DATA_COLUMN)

        # merge the cells for the element numbers
        table.mergeCells(0, PoioGraidTextEdit.NUMBERS_COLUMN, count_rows, 1)
        # set format for number
        c = table.cellAt(0, PoioGraidTextEdit.NUMBERS_COLUMN)
        format = c.format()
        format.setFontCapitalization(QtGui.QFont.SmallCaps)
        format.setFontWeight(QtGui.QFont.Bold)
        format.setFontPointSize(12)
        format.setVerticalAlignment(QtGui.QTextCharFormat.AlignMiddle)
        c.setFormat(format)

        for i, row_name in enumerate(
            self.structure_type_handler.flat_data_hierarchy):
            c = table.cellAt(i, PoioGraidTextEdit.ROW_NAMES_COLUMNS)
            format = c.format()
            format.setFontCapitalization(QtGui.QFont.SmallCaps)
            format.setForeground(QtGui.QBrush(QtGui.QColor(150, 150, 150)))
            c.setFormat(format)
            c.firstCursorPosition().insertText(row_name)

        return table

    def update_numbers(self):
        """
        Updates the number of the utterances
        """
        root = self.document().rootFrame()
        #string_document_text = unicode(self.document().toPlainText())
        tree = []
        number = 1
        for frame in root.childFrames():
            if frame.__class__.__name__ == "QTextTable":
                self._update_number_of_table(frame, number)
                number += 1

    def _update_number_of_table(self, table, number):
        """
        Updates the number of a utterance

        ...

        Parameters
        ----------
        table : QTextTable
        number : int
        """
        c = table.cellAt(0, PoioGraidTextEdit.NUMBERS_COLUMN)
        cursor = c.firstCursorPosition()
        cursor.setPosition(
            c.lastCursorPosition().position(), QtGui.QTextCursor.KeepAnchor)
        #cursor.removeSelectedText()
        cursor.insertText(" {0} ".format(number))

    def _insert_annotation_cell(self, elements, flat_hierarchy, hierarchy,
                                table, column):
        """
        Adds annotation cell

        ...

        Parameters
        ----------
        elements : list
        flat_hierarchy :list
        hierarchy : list
        table: QTextTable
        column : int
        """
        inserted = 0
        for i, t in enumerate(hierarchy):
            if type(t) is list:
                elements_list = elements[i]
                for i, e in enumerate(elements_list):
                    inserted += self._insert_annotation_cell(
                        e, flat_hierarchy, t, table, column + i + inserted)
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
        """
        Adds a annotation

        ...

        Parameters
        ----------
        e : dict
        table : QTextTable
        row : int
        column : int
        """
        if (column + 1) > table.columns():
            table.appendColumns(1)
        c = table.cellAt(row, column)
        c.firstCursorPosition().insertText(e['annotation'])
        f = c.format()
        f.setAnchorNames(str([e['id']]))
        c.setFormat(f)

    def annotation_tree_from_document(self):
        """
        Returns the tree from a document
        """
        if not self.structure_type_handler:
            raise NoStructureTypeHandlerError

        root = self.document().rootFrame()
        #string_document_text = unicode(self.document().toPlainText())
        tree = []
        for frame in root.childFrames():
            if frame.__class__.__name__ == "QTextTable":
                utterance = list()
                self._annotation_cell(utterance,
                    self.structure_type_handler.flat_data_hierarchy,
                    self.structure_type_handler.data_hierarchy,
                    frame,
                    0, PoioGraidTextEdit.FIRST_DATA_COLUMN,
                    frame.columns() - PoioGraidTextEdit.FIRST_DATA_COLUMN)
                tree.append(utterance)
        return tree

    def _annotation_cell(self, elements, flat_hierarchy, hierarchy, table,
                         row, column, column_span):
        """
        Adds annotation cell

        ...

        Parameters
        ----------
        elements : list
        flat_hierarchy : list
        hierarchy : list
        table: QTextTable
        row : int
        column : int
        column_span : int
        """
        #processed = 0
        for i, t in enumerate(hierarchy):
            if type(t) is list:
                sub_tree = list()
                column_add = 0
                while column_add < column_span:
                    c = table.cellAt(row, column + column_add)
                    sub_element = list()
                    self._annotation_cell(
                        sub_element, flat_hierarchy, t, table, row,
                        column + column_add, c.columnSpan())
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
        """
        Adds annotation cell

        ...

        Parameters
        ----------
        table : QTextTable
        row : int
        column : int
        """
        element = dict()
        c = table.cellAt(row, column)
        start = int(c.firstCursorPosition().position())
        end = int(c.lastCursorPosition().position())
        element['id'] = c.format().anchorNames()[0]
        element['annotation'] = \
            self.document().toPlainText()[start:end]
        return element
