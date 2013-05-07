# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2001-2012 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://www.cidles.eu/ltll/poio>
# For license information, see LICENSE.TXT

import sys
import os
import glob
from distutils.core import setup
from cx_Freeze import setup, Executable

# build targets
(DEFAULT, WINDOWS) = range(2)
target = DEFAULT

# import the poio module locally for module metadata
sys.path.insert(0, 'src')
import poio

# if we are running "setup.py sdist", include all targets (see below)
building_source = ('sdist' in sys.argv)

# build target
if 'TARGET' in os.environ:
    if os.environ['TARGET'].strip().lower() == 'windows':
        target = WINDOWS

base = None
if sys.platform == "win32":
    base = "Win32GUI"

# files to install
inst_desktop = [ 'data/poioile.desktop', 'data/poioanalyzer.desktop' ]
inst_examples = glob.glob('data/examples/*')
inst_templates = glob.glob('data/html/*.html')
#inst_pixmaps = glob.glob('data/pixmaps/*.png')

# data files
data_files = data_files=[
    ('share/poio/examples', inst_examples),
    ('share/poio/html', inst_templates),
#    ('share/poio/pixmaps', inst_pixmaps),
]

# packages
packages = [
  'poio',
  'poio.ui'
]

# target-specific installation data files
if target == DEFAULT or building_source:
    data_files += [
      ('share/applications', inst_desktop)
    ]

setup(
    name             = 'poio',
    version          = poio.__version__,
    url              = poio.__url__,
    description      = 'Poio, annotation and analysis software for linguists.',
    long_description = poio.__longdescr__,
    license          = poio.__license__,
    keywords         = poio.__keywords__,
    maintainer       = poio.__maintainer__,
    maintainer_email = poio.__maintainer_email__,
    classifiers      = poio.__classifiers__,
    author           = poio.__author__,
    author_email     = poio.__author_email__,

    package_dir      = { '':'src' },
    packages         = packages,
    scripts          = glob.glob('bin/*'),
    data_files       = data_files,
    install_requires = ['PyQt', 'poio-api', 'graf-python'],
    executables = [Executable("bin/PoioGRAID", base=base), Executable("bin/PoioAnalyzer", base=base)]
)


