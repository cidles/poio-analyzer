# -*- coding: utf-8 -*-
# (C) 2009 copyright by Peter Bouda

import os
from PySide import QtCore
from poio.poiofile import PoioFile

class PoioProject(QtCore.QAbstractListModel):

    def __init__(self, projectdir, parent = None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.projectfiles = []
        self.projectdir = projectdir
        self.corpusreader = None

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if index.row() < len(self.projectfiles):
                return os.path.basename(self.projectfiles[index.row()].filepath)
            else:
                return QtCore.QVariant()

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            if index.row() < len(self.projectfiles):
                self.projectfiles[index.row()] = PoioFile(value)
                self.emit(QtCore.SIGNAL("dataChanged"), index, index)
                return True
            else:
                return False
            
    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            return "File path"
        
    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.projectfiles)
        
    def insertRows(self, row, count, parent = QtCore.QModelIndex()):
        if row >= 0 and row <= self.rowCount():
            self.beginInsertRows(parent, row, row+count)
            for i in range(0,count):
                self.projectfiles.insert(row, PoioFile())
            self.endInsertRows()
            return True
        else:
            return False
        
    def addFilePath(self, poiofilepath):
        # does the file exist in the project?
        for poiofile in self.projectfiles:
            if poiofile.filepath == poiofilepath:
                return True
        if self.insertRows(self.rowCount(), 1):
            self.setData(self.index(self.rowCount(), 0), poiofilepath)
            return True
        return False

    def addFilePaths(self, poiofilepaths):
        for filepath in poiofilepaths:
            self.addFilePath(unicode(filepath))

    def poioFileAt(self, row):
        if row < self.rowCount():
            return self.projectfiles[row]
        else:
            return None
