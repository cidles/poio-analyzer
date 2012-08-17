# -*- coding: utf-8 -*-
# (C) 2011 copyright by Peter Bouda

import os
from PyQt4 import QtCore
from poio.poiofile import PoioFile

class PoioProject(QtCore.QAbstractListModel):

    def __init__(self, projectdir, parent = None):
        """
        The consctructor of the main application object.
        Calls a lot of other init methods.

        ...

        Parameters
        ----------
        parent : QModelIndex
        """
        QtCore.QAbstractListModel.__init__(self, parent)
        self.projectfiles = []
        self.projectdir = projectdir
        self.corpusreader = None

    def flags(self, index):
        """
        Flags

        ...

        Parameters
        ----------
        index : QModelIndex
        """
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        """
        Returns data

        ...

        Parameters
        ----------
        index : QModelIndex
        role : int
        """
        if role == QtCore.Qt.DisplayRole:
            if index.row() < len(self.projectfiles):
                return os.path.basename(self.projectfiles[index.row()].filepath)
            else:
                return QtCore.QVariant()

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        """
        Sets the data in the list of the open files

        ...

        Parameters
        ----------
        index : QModelIndex
        value : QVariant
        role : int
        """
        if role == QtCore.Qt.EditRole:
            if index.row() < len(self.projectfiles):
                self.projectfiles[index.row()] = PoioFile(value)
                self.emit(QtCore.SIGNAL("dataChanged"), index, index)
                return True
            else:
                return False
            
    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole):
        """
        Returns the header

        ...

        Parameters
        ----------
        section : int
        orientation : enum
        role : int
        """
        print orientation
        if role == QtCore.Qt.DisplayRole:
            return "File path"
        
    def rowCount(self, parent = QtCore.QModelIndex()):
        """
        Returns the number of rows
        ...

        Parameters
        ----------
        parent : QModelIndex
        """
        return len(self.projectfiles)
        
    def insertRows(self, row, count, parent = QtCore.QModelIndex()):
        """
        Insert rows
        ...

        Parameters
        ----------
        row : int
        count : int
        parent : QModelIndex
        """
        if row >= 0 and row <= self.rowCount():
            self.beginInsertRows(parent, row, row+count)
            for i in range(0,count):
                self.projectfiles.insert(row, PoioFile())
            self.endInsertRows()
            return True
        else:
            return False

    def removeRows(self, row, count, parent = QtCore.QModelIndex()):
        """
        Remove Rows
        ...

        Parameters
        ----------
        row : int
        count : int
        parent : QModelIndex
        """
        if row >= 0 and (row+count)<=self.rowCount():
            self.beginRemoveRows(parent, row, row+count)
            for i in range(0,count):
                self.projectfiles.pop(row)
            self.endRemoveRows()
            return True
        else:
            return False
        
    def addFilePath(self, poiofilepath):
        """
        Add a file to the project if it doesn't exist yet
        ...

        Parameters
        ----------
        poiofilepath : str
        """
        # does the file exist in the project?
        for poiofile in self.projectfiles:
            if poiofile.filepath == poiofilepath:
                return True
        if self.insertRows(self.rowCount(), 1):
            self.setData(self.index(self.rowCount(), 0), poiofilepath)
            return True
        return False

    def addFilePaths(self, poiofilepaths):
        """
        Add one or multiple files to the project
        ...

        Parameters
        ----------
        poiofilepaths : list
        """
        for filepath in poiofilepaths:
            self.addFilePath(unicode(filepath))

    def removeFilePathAt(self, index):
        """
        Remove file from the open files list
                ...

        Parameters
        ----------
        index : int
        """
        self.removeRows(index, 1)
        
    def poioFileAt(self, row):
        """
        Returns the Poio file at the given row

        ...

        Parameters
        ----------
        row : int
        """
        if row < self.rowCount():
            return self.projectfiles[row]
        else:
            return None

    def setAllFilesAsNew(self):
        """
        Set all files as new
        """
        for file in self.projectfiles:
            file.setIsNew(True)

    def clear(self):
            for row in range(0,self.rowCount()):
                self.projectfiles.pop(row)


