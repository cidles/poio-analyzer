# -*- coding: utf-8 -*-
# (C) 2009 copyright by Peter Bouda

import re
import pyannotation.data

class PoioFile(object):

    def __init__(self, filepath = ""):
        self.filepath = filepath
        self.isNew = True
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

    def setIsNew(self, value = True):
        self.isNew = value

