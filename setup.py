#!/usr/bin/env python

#
# Poio - software for linguists
# Copyright (c) 2009, 2010 Peter Bouda
#
# Poio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Poio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import os
import glob
from distutils.core import setup

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
    install_requires = ['PyQt']
)


