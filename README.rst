========================
Poio Tools for Linguists
========================

Website
-------
`www.cidles.eu/ltll/poio <http://www.cidles.eu/ltll/poio>`_

Authors
-------
- Peter Bouda: `pbouda@cidles.eu <mailto:pbouda@cidles.eu>`_

Introduction
------------
Poio is a collection of software tools for linguists working in language
documentation, descriptive linguistics and/or language typology. It allows
linguists to manage and analyze their data. The Poio Interlinear Editor allows
to add morpho-syntactic and other annotations to transcriptions. It supports
various file formats for input, but will only output standardized XML defined
by the Corpus Encoding Standard and the Text Encoding Initiative. Several
tools for analyzing linguistic data will be made available to further process
annotated data. Poio tools are written in Python and are based on PyQt.

Documentation
-------------
You can find the documentation for Poio on the `Github Pages
<http://cidles.github.com/Poio/>`_.

Develop
-------

How to start with PyCharm
=========================

1. Clone Poio from Github (https://github.com/cidles/Poio);
2. Clone Pyannotation from Github (https://github.com/cidles/pyannotation);
3. Start PyCharm;
4. Choose "File" -> "Open Directory" in menu and open Poio directory;
5. Choose "File" -> "Settings" and set the "Project Interpreter" to Python 2.7;
6. Choose "File" -> "Settings" and in the "Project Structure" add a "Content Root" that points to the PyAnnotation directory; set the PyAnnotation "src" directory as the "Sources";
7. * Choose "Run" -> "Edit Configurations" and add a new configuration;
   * Select "Python" configuration;
   * Give it a name;
   * Point the "Script" to "Poio\\bin\\PoioGRAID";
8. Develop and run it.


Dependencies
------------
In order to develop Poio you need to install the folowing programs/libraries:

- Python 2.7: `http://www.python.org/download/ <http://www.python.org/download/>`_ ;
- Regex: `http://pypi.python.org/pypi/regex/ <http://pypi.python.org/pypi/regex/>`_ ;
- PyQt: `http://www.riverbankcomputing.co.uk/software/pyqt/download <http://www.riverbankcomputing.co.uk/software/pyqt/download>`_ ;
- PyAnnotation: `https://github.com/cidles/pyannotation <https://github.com/cidles/pyannotation>`_ ;


Donating
--------
Have you found Poio helpful? Please support Poio development by supporting the
`Centro Interdisciplinar de Documentação Linguística e Social
<http://www.cidles.eu/>`_ (click on ``Support`` to learn more).

Redistributing
--------------
Poio source code is distributed under the Apache 2.0 License.

Poio documentation is distributed under the Creative Commons
Attribution-Noncommercial-No Derivative Works 3.0 United States license.

Poio may be freely redistributed, subject to the provisions of these licenses.
For license information, see LICENSE.TXT

