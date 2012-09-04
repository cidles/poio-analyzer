# -*- coding: utf-8 -*-
# (C) 2011 copyright by Peter Bouda

import re
import poioapi.data

class PoioFile(object):

    def __init__(self, filepath = ""):
        """
        Initializes PoioFile

        ...

        Parameters
        ----------
        filepath : str
        """
        self.filepath = filepath
        self.isNew = True
        self.type = None
        if re.search(r"\.eaf$", filepath):
            f = open(filepath)
            data = f.read()
            if re.search("LINGUISTIC_TYPE_ID=\"ref\"", data) and re.search("LINGUISTIC_TYPE_ID=\"tx\"", data) and re.search("LINGUISTIC_TYPE_ID=\"ft\"", data):
                self.type = poioapi.data.EAFFROMTOOLBOX
            else:
                self.type = poioapi.data.EAF
            f.close()
        elif re.search(r"\.txt$", filepath):
            self.type = poioapi.data.TOOLBOX
        elif re.search(r"\.txt$", filepath):
            self.type = poioapi.data.KURA

    def setIsNew(self, value = True):
        """
        Defines isNew

        ...

        Parameters
        ----------
        value : bool
        """
        self.isNew = value

