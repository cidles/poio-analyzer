# -*- coding: utf-8 -*-
# (C) 2011 copyright by Peter Bouda

import re
import pyannotation.data

class PoioFile(object):

    def __init__(self, filepath = ""):
        """
        Initializes PoioFile

        ...

        Parameters
        ----------
        self.filepath : str
            File Path
        self.isNew : bool
        self.type : int
            Data Format
        f : Open file
        """
        self.filepath = filepath
        self.isNew = True
        self.type = None
        if re.search(r"\.eaf$", filepath):
            f = open(filepath)
            data = f.read()
            if re.search("LINGUISTIC_TYPE_ID=\"ref\"", data) and re.search("LINGUISTIC_TYPE_ID=\"tx\"", data) and re.search("LINGUISTIC_TYPE_ID=\"ft\"", data):
                self.type = pyannotation.data.EAFFROMTOOLBOX
            else:
                self.type = pyannotation.data.EAF
            f.close()
        elif re.search(r"\.txt$", filepath):
            self.type = pyannotation.data.TOOLBOX
        elif re.search(r"\.txt$", filepath):
            self.type = pyannotation.data.KURA

    def setIsNew(self, value = True):
        """
        Defines isNew
        """
        self.isNew = value

