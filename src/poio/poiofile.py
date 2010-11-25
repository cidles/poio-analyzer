# -*- coding: utf-8 -*-
# (C) 2009 copyright by Peter Bouda

import re
import pyannotation.data

class PoioFile(object):

    def __init__(self, filepath = ""):
        self.filepath = filepath
        if re.search(r"\.eaf$", filepath):
            self.type = pyannotation.data.EAF
        elif re.search(r"\.txt$", filepath):
            self.type = pyannotation.data.TOOLBOX


