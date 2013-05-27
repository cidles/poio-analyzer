# -*- coding: utf-8 -*-
# (C) 2011-2012 copyright by Peter Bouda

from __future__ import unicode_literals
import os.path
import sys
import re
import copy
import codecs
import time
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QSettings
from PyQt4.QtGui import QPrinter, QPrintDialog, QAbstractPrintDialog, QTextDocument, QPageSetupDialog, QDialog

import poioapi.corpus
import poioapi.annotationtree

from poio.ui.Ui_MainAnalyzerHTML import Ui_MainWindow
from poio.ui.Ui_TabWidgetSearch import Ui_TabWidgetSearch

from poio.poioproject import PoioProject

class PoioAnalyzer(QtGui.QMainWindow):
    """The main window of the PoioAnalyzer application."""

    def __init__(self, *args):
        """
        Initialize Main Window
        """
        QtGui.QMainWindow.__init__(self, *args)

        #self.reset_data_structure_type(poioapi.data.GRAID)
        self.vertical_position_of_file = {}

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init_connects()
        self.init_settings()
        self.project = PoioProject(os.getcwd())
        self.ui.listFiles.setModel(self.project)
        self.init_corpus()

        self.add_search_tab()

    def init_corpus(self):
        """
        Initializes an empty corpus.
        """
        #print sys.path
        self.corpus = poioapi.corpus.CorpusGraphs()

    def init_connects(self):
        """
        Initializes all signal/slots connections of the application.
        """
        # Menu buttons
        self.ui.actionPrint.triggered.connect(self.printdoc)
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionAboutPoioAnalyzer.triggered.connect(self.about_dialog)
        self.ui.actionZoom_In.triggered.connect(self.zoom_in)
        self.ui.actionZoom_Out.triggered.connect(self.zoom_out)
        self.ui.actionReset_Zoom.triggered.connect(self.reset_zoom)

        # Push Buttons
        self.ui.buttonAddFiles.pressed.connect(self.add_files)
        self.ui.buttonRemoveFiles.pressed.connect(self.remove_files)

        # Filter and Search
        self.ui.buttonSearch.pressed.connect(self.apply_filter)
        self.ui.buttonCloseThisSearch.pressed.connect(self.search_tab_closed)
        self.ui.buttonClearThisSearch.pressed.connect(self.search_tab_cleared)
        self.ui.tabWidget.currentChanged.connect(self.search_tab_changed)

        self.ui.listFiles.activated.connect(self.set_current_file_in_result_view)
        self.ui.actionExportSearchResult.triggered.connect(
            self.export_search_results)

        # Quick Search
        #QtCore.QObject.connect(self.ui.actionQuickSearch, QtCore.SIGNAL("triggered()"), self.ui.lineeditQuickSearch.setFocus)
        #QtCore.QObject.connect(self.ui.lineeditQuickSearch, QtCore.SIGNAL("textChanged(const QString &)"), self.findFromStart)
        #QtCore.QObject.connect(self.ui.lineeditQuickSearch, QtCore.SIGNAL("returnPressed()"), self.findNext)

    def init_settings(self):
        """
        Initialize QSettings;
        Set default zoom to 100%
        """
        QtCore.QCoreApplication.setOrganizationName(
            "Interdisciplinary Centre for Social and Language Documentation");
        QtCore.QCoreApplication.setOrganizationDomain("cidles.eu");
        QtCore.QCoreApplication.setApplicationName("PoioAnalyzer");
        settings = QtCore.QSettings()
        settings.setValue("FontZoom", 100)

    #def reset_data_structure_type(self, data_structure_type):
    #    self.data_structure_type = data_structure_type
    #    self.structure_type_handler = poioapi.data.data_structure_handler_for_type(
    #        data_structure_type
    #    )

    def remove_files(self):
        """
        Remove files from the "Added files list"
        """
        countRemoved = 0
        for i in self.ui.listFiles.selectedIndexes():
            self.project.removeFilePathAt(i.row()-countRemoved)
            countRemoved = countRemoved + 1
        self.init_corpus()
        self.project.setAllFilesAsNew()
        self.update_corpus_reader()
        self.update_result_view()

    def add_files(self):
        """
        Loads the file as filepath;
        Tells the user the time it took to load the file selected.
        """
        # PySide version
        #filepaths, types = QtGui.QFileDialog.getOpenFileNames(self, self.tr("Add Files"), "", self.tr("Elan files (*.eaf);;Toolbox files (*.txt);;All files (*.*)"))
        # PyQt version
        filepaths = QtGui.QFileDialog.getOpenFileNames(self, self.tr("Add Files"), "", self.tr("Pickle files (*.pickle);;Elan files (*.eaf);;Typecraft files (*.xml)"))
        #filepaths = QtGui.QFileDialog.getOpenFileNames(self, self.tr("Add Files"), "", self.tr("Elan files (*.eaf);;Toolbox files (*.txt);;Kura files (*.xml);;All files (*.*)"))
        self.project.addFilePaths(filepaths)
        start = time.time()
        self.update_corpus_reader()
        end = time.time()
        print("Time elapsed = ", end - start, "seconds")
        start = time.time()
        self.update_result_view()
        end = time.time()
        print("Time elapsed = ", end - start, "seconds")

    def update_corpus_reader(self):
        """
        Updates the shown opened files view
        """
        itemsCount = self.project.rowCount()
        progress = QtGui.QProgressDialog(self.tr("Loading Files..."), self.tr("Abort"), 0, itemsCount, self.parent())
        progress.setWindowModality(QtCore.Qt.WindowModal)
        incompatible_files = []
        for i in range(itemsCount):
            progress.setValue(i)
            poiofile = self.project.poioFileAt(i)
            if poiofile.is_new:
                #print poiofile.filepath
                try:
                    self.corpus.add_item(poiofile.filepath, poiofile.type)
                except poioapi.data.UnknownFileFormatError:
                    incompatible_files.append(poiofile.filepath)
                poiofile.is_new = False
            if progress.wasCanceled():
                self.init_corpus()
                break
        progress.setValue(itemsCount)
        if len(incompatible_files) > 0:
            QtGui.QMessageBox.warning(self,
                "Cannot add files",
                "The following files could not be added to the project:"
                "<br/><br/><b>{0}</b><br/><br/>The file format was not "
                "recognized.<br/><b>The file will not be diplayed in the "
                "search result view</b>.".format(
                    ", ".join(incompatible_files)))
        #self.updateCorpusReaderFilter()

    def set_current_file_in_result_view(self, modelIndex):
        """
        Sets what shows up in the result view

        ...

        Parameters
        ----------
        modelIndex :
        """
        e_id = "#file_{0}".format(modelIndex.row())
        e = self.ui.webviewResult.page().mainFrame().findFirstElement(e_id)
        if not e.isNull():
            e.evaluateJavaScript("this.scrollIntoView(true);")

    def update_result_view(self):
        """
        Updates the view screen with the refreshed data and zoom settings
        """
        settings = QtCore.QSettings()
        html = "<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /></head><body>\n"
        i = 0
        for filepath, annotationgraph in self.corpus.items:
            html += "<h1 id=\"file_{1}\">{0}</h1>\n".format(os.path.basename(str(filepath)), i)
            html += annotationgraph.as_html_table(True, False)
            i += 1
        html += "</body></html>"

        #self.ui.webviewResult.settings().setUserStyleSheetUrl(
        #    QtCore.QUrl(":/css/css/resultview.css")) #.setStyleSheet("td { border: 1px solid black; }")

        #stylesheet_url = QtCore.QUrl.fromLocalFile("h:/ProjectsWin/git-github/Poio/ui/css/resultview.css")

        css = QtCore.QByteArray("td { border: 1px solid black; }\ntable { margin-top: 10px; }\ntd.element_id { margin-left: 10px; margin-right: 10px; font-weight:bold; }\ntd.ann_type { margin-left: 10px; margin-right: 10px; font-variant:small-caps; }\nbody {}")
        if sys.version_info < (3, 0):
            zoom = str(settings.value("FontZoom").toInt()[0])
            css = QtCore.QByteArray("td { font-size: " + zoom + "%; border: 1px solid black; }\ntable { margin-top: 10px; }\ntd.element_id { margin-left: 10px; margin-right: 10px; font-weight:bold; }\ntd.ann_type { margin-left: 10px; margin-right: 10px; font-variant:small-caps; }\nbody { font-size: " + zoom + "%; }")
        else:
            zoom = str(settings.value("FontZoom"))
            self.ui.webviewResult.setTextSizeMultiplier(int(zoom) / 100)

        self.ui.webviewResult.settings().setUserStyleSheetUrl(
            QtCore.QUrl("data:text/css;charset=utf-8;base64,"
            + str(css.toBase64())))
        self.ui.webviewResult.setHtml(html)


    def zoom_in(self):
        """
        Increase the zoom setting by 10 % when the menu button is clicked
        until the 200% zoom limit is reached
        """
        settings = QtCore.QSettings()
        if sys.version_info < (3, 0):
            currentzoom = settings.value("FontZoom").toInt()[0]
        else:
            currentzoom = settings.value("FontZoom")
        if currentzoom < 200:
            zoom = currentzoom + 10
            settings.setValue("FontZoom", zoom)
            self.update_result_view()


    def zoom_out(self):
        """
        Decreases the zoom setting by 10 % when the menu button is clicked
        until the 50% zoom limit is reached
        """
        settings = QtCore.QSettings()
        if sys.version_info < (3, 0):
            currentzoom = settings.value("FontZoom").toInt()[0]
        else:
            currentzoom = settings.value("FontZoom")
        if currentzoom > 50:
            zoom = currentzoom - 10
            settings.setValue("FontZoom", zoom)
            self.update_result_view()


    def reset_zoom(self):
        """
        Resets the zoom setting to the default value of 100%
        """
        settings = QtCore.QSettings()
        settings.setValue("FontZoom", 100)
        self.update_result_view()


    def printdoc(self):
        """
        Prints the document in the view
        """
        printer = QPrinter()

        setup = QPageSetupDialog(printer)
        setup.setWindowTitle("Print - Page Settings")

        if setup.exec_() == QDialog.Accepted:
            dialog = QPrintDialog(printer, self)
            dialog.setWindowTitle("Print Document")

            if dialog.exec_() == QDialog.Accepted:
                self.ui.webviewResult.print_(printer)


    def export_search_results(self):
        """
        Exports the current annotationtree as HTML
        """

        export_file =  QtGui.QFileDialog.getSaveFileName(self, self.tr("Export Search Result"), "", self.tr("HTML file (*.html)"))
        export_file = str(export_file)
        OUT  = codecs.open(export_file, "w", "utf-8")
        html = "<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /></head><body>\n"
        for filepath, annotation_graph in self.corpus.items:
            html += "<h1>{0}</h1>\n".format(os.path.basename(filepath))
            html += annotation_graph.as_html_table(True, False)
        html += "</body></html>"
        OUT.write(html)
        OUT.close()
    #def findFromStart(self, exp):
    #    self.ui.texteditInterlinear.setTextCursor(QtGui.QTextCursor(self.ui.texteditInterlinear.document()))
    #    if not self.ui.texteditInterlinear.find(exp) and exp != "":
    #        self.statusBar().showMessage(self.tr("No match found."), 2000)

    #def findNext(self):
    #    found = self.ui.texteditInterlinear.find(self.ui.lineeditQuickSearch.text())
    #    if not found:
    #        self.statusBar().showMessage(self.tr("Restarting search from beginning of document."), 2000)
    #        found = self.findFromStart(self.ui.lineeditQuickSearch.text())
    #    return found

    def apply_filter(self):
        """
        Check for the search options and update the resul view
        """
        filter_chain = []
        for i in range(0, self.ui.tabWidget.currentIndex()+1):
            search_terms = dict()
            for tier in self.corpus.tier_names:
                inputfield = self.ui.tabWidget.findChild(QtGui.QLineEdit, "lineedit_{0}_{1}".format(tier, i+1))
                if inputfield:
                    search_terms[tier] = str(inputfield.text())
                #currentFilter.set_filter_for_type(ann_type, str(inputfield.text()))

            checkbox = self.ui.tabWidget.findChild(QtGui.QCheckBox, "checkboxInvert_%i"%(i+1))
            is_inverted = checkbox.isChecked()
            checkbox = self.ui.tabWidget.findChild(QtGui.QCheckBox, "checkboxContained_%i"%(i+1))
            is_contained = checkbox.isChecked()

            radiobutton_or = self.ui.tabWidget.findChild(QtGui.QRadioButton, "radiobuttonOr_%i"%(i+1))
            boolean_op = poioapi.annotationtree.AnnotationTreeFilter.AND
            if radiobutton_or.isChecked():
                boolean_op = poioapi.annotationtree.AnnotationTreeFilter.OR

            for _, annotation_graph in self.corpus.items:
                annotation_graph.init_filters()
                filter = annotation_graph.create_filter_for_dict(search_terms)
                filter.inverted = is_inverted
                filter.contained_matches = is_contained
                filter.booleab_operation = boolean_op
                annotation_graph.append_filter(filter)

        #self.updateCorpusReaderFilter()
        self.update_result_view()

    def search_tab_changed(self, index):
        """
        Check if the search tab changed

        ...

        Parameters
        ----------
        index : int
        """

        if index == self.ui.tabWidget.count() - 1:
            self.add_search_tab()

        else:
            self.apply_filter()

    def add_search_tab(self):
        """
        Add a search tab
        """
        nr_of_new_tab = self.ui.tabWidget.count()
        widget_search = QtGui.QWidget()
        ui = Ui_TabWidgetSearch()
        ui.setupUi(widget_search)
        widget_search.setObjectName("%s_%i" % (widget_search.objectName(), nr_of_new_tab))

        for i, tier in enumerate(self.corpus.tier_names):
            #layoutSearch = QtGui.QHBoxLayout(self)
            label = QtGui.QLabel(widget_search)
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(label.sizePolicy().hasHeightForWidth())
            label.setSizePolicy(sizePolicy)
            label.setSizeIncrement(QtCore.QSize(1, 0))
            label.setText(QtGui.QApplication.translate("TabWidgetSearch", "{0}:".format(tier), None, QtGui.QApplication.UnicodeUTF8))
            label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
            ui.layoutLabels.addWidget(label)

            lineedit = QtGui.QLineEdit(self.ui.tabWidget)
            lineedit.setSizeIncrement(QtCore.QSize(2, 0))
            lineedit.setObjectName("lineedit_{0}".format(tier))
            ui.layoutLineedits.addWidget(lineedit)

            lineedit.returnPressed.connect(self.apply_filter)

            #ui.layoutSearches.addLayout(layoutSearch)

        for childWidget in widget_search.findChildren(QtGui.QWidget):
            if re.match("lineeditSearch", childWidget.objectName()):
                QtCore.QObject.connect(childWidget, QtCore.SIGNAL("returnPressed()"), self.apply_filter)
            childWidget.setObjectName("%s_%i" % (childWidget.objectName(), nr_of_new_tab))
        self.ui.tabWidget.insertTab(nr_of_new_tab - 1, widget_search, "Search %i" % nr_of_new_tab)
        self.ui.tabWidget.setCurrentIndex(nr_of_new_tab - 1)

    def update_search_tab_widget_names(self):
        """
        Updates the search tab
        """
        for i in range(0, self.ui.tabWidget.count()-1):
            widget = self.ui.tabWidget.widget(i)
            for childWidget in widget.findChildren(QtGui.QWidget):
                childWidget.setObjectName("%s_%i" % (childWidget.objectName()[:-2], i+1))
            self.ui.tabWidget.setTabText(i, "Search %i" % (i+1))

    def search_tab_closed(self):
        """
        Closes the search tab
        """
        # always leave at least one Search tab open
        if self.ui.tabWidget.indexOf(self.ui.tabNewSearch) < 2:
            return
        currentIndex = self.ui.tabWidget.currentIndex()
        if currentIndex < 1:
            return
        widgetSearch = self.ui.tabWidget.currentWidget()
        self.ui.tabWidget.setCurrentIndex(currentIndex-1)
        self.ui.tabWidget.removeTab(currentIndex)
        widgetSearch.close()
        widgetSearch.deleteLater()
        del widgetSearch
        self.update_search_tab_widget_names()

    def search_tab_cleared(self):
        """
        Clears the search tab
        """
        widget = self.ui.tabWidget.currentWidget()
        for childWidget in widget.findChildren(QtGui.QWidget):
            if re.match("lineeditSearch", childWidget.objectName()):
                childWidget.setText("")
        self.apply_filter()

    def about_dialog(self):
        """
        Popup a message box containing the "About Information"
        of Poio Analyser
        """
        QtGui.QMessageBox.about(self,
            "About Poio Analyzer",
            """<b>Poio Analyzer v0.3.0</b>
               <br/><br/>
               Poio Analyzer is an analysis tool for linguists
               to analyze interlinear data. It is developed by
               Peter Bouda at the
               <b><a href=\"http://www.cidles.eu\">
                  Interdisciplinary Centre for Social and Language
                  Documentation</a>
                </b>
                <br/><br/>
                Please send bug reports and
                comments to <b><a href=\"mailto:pbouda@cidles.eu\">
                pbouda@cidles.eu</a></b>.
                <br/><br/>
                For more information visit the website of the project:
                <br/>
                <b><a href="http://media.cidles.eu/poio/">
                    http://media.cidles.eu/poio/
                </a></b>
                <br/><br/>
                All rights reserved. See LICENSE file for details.
                """
        )
    
