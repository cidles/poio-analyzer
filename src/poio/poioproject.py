# -*- coding: utf-8 -*-
# (C) 2009 copyright by Peter Bouda

from poio.poiofile import PoioFile

class PoioProject(object):

    def __init__(self, projectdir):
        self.projectfiles = []
        self.projectdir = projectdir

    def addFilePath(poiofilepath):
        poiofile = PoioFile(poiofilepath)
        self.projectfiles.append(poiofile)

