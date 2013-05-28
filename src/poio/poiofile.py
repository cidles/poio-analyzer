# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

import re
import codecs
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
        self.is_new = True
        self.type = None
        if re.search("\.eaf$", filepath):
            f = codecs.open(filepath, "r", "utf-8")
            data = f.read()
            if re.search("LINGUISTIC_TYPE_ID=\"ref\"", data) and re.search("LINGUISTIC_TYPE_ID=\"tx\"", data) and re.search("LINGUISTIC_TYPE_ID=\"ft\"", data):
                self.type = poioapi.data.EAFFROMTOOLBOX
            else:
                self.type = poioapi.data.EAF
            f.close()
        elif re.search("\.xml$", filepath):
            self.type = poioapi.data.TYPECRAFT
        elif re.search("\.pickle$", filepath):
            self.type = poioapi.data.TREEPICKLE
        elif re.search("\.txt$", filepath):
            self.type = poioapi.data.TOOLBOX


