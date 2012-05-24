# -*- coding: utf-8 -*-
# (C) 2011-2012 copyright by Peter Bouda

import sys, os.path, re, copy, codecs
import time
from PyQt4 import QtCore, QtGui
from PyQt4.QtDeclarative import QDeclarativeView

#from pyannotation.toolbox.data import ToolboxAnnotationFileObject
#from pyannotation.elan.data import EafAnnotationFileObject
#from pyannotation.data import AnnotationTree, AnnotationTreeFilter
#import pyannotation.data

#from pyannotation.corpusreader import GlossCorpusReader
#from pyannotation.corpus import CorpusTrees

#import pyannotation
import pyannotation.corpus
import pyannotation.annotationtree

from poio.ui.Ui_MainAnalyzerQML import Ui_MainWindow
#from poio.ui.PoioIlTextEdit import PoioIlTextEdit
from poio.ui.Ui_TabWidgetSearch import Ui_TabWidgetSearch

from poio.poioproject import PoioProject


class PoioAnalyzer(QtGui.QMainWindow):
    """The main window of the PoioAnalyzer application."""

    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)

        self.data_structure_type = pyannotation.data.DataStructureTypeGraid()
        self.vertical_position_of_file = {}

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init_connects()
        self.init_settings()
        self.project = PoioProject(os.getcwd())
        self.ui.listFiles.setModel(self.project)
        self.init_corpus()
        self.init_declarative_view()

        self.add_search_tab()


    def init_declarative_view(self):
        # init DeclarativeView
        #self.ui.declarativeviewResult.setResizeMode(QDeclarativeView.SizeRootObjectToView)
        self.ui.declarativeviewResult.setResizeMode(QDeclarativeView.SizeViewToRootObject)
        self.ui.declarativeviewResult.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.ui.declarativeviewResult.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        context = self.ui.declarativeviewResult.rootContext()
        context.setContextProperty("resultModel", [])

        self.ui.declarativeviewResult.setSource(QtCore.QUrl.fromLocalFile("qml/PoioIlView.qml"))

        #obj = self.ui.declarativeviewResult.rootObject()
        #QtCore.QObject.connect(obj, QtCore.SIGNAL("fileAdded(QString, int)"), self.upateVerticalPositionOfFile)
        
    def init_corpus(self):
        """
        Initializes an empty corpus.
        """
        #print sys.path
        self.corpus = pyannotation.corpus.CorpusTrees(self.data_structure_type)

    def update_corpus_reader(self):
        itemsCount = self.project.rowCount()
        progress = QtGui.QProgressDialog(self.tr("Loading Files..."), self.tr("Abort"), 0, itemsCount, self.parent())
        progress.setWindowModality(QtCore.Qt.WindowModal)
        for i in range(itemsCount):
            progress.setValue(i)
            poiofile = self.project.poioFileAt(i)
            if poiofile.isNew:
                #print poiofile.filepath
                self.corpus.addFile(poiofile.filepath)
                poiofile.setIsNew(False)
            if progress.wasCanceled():
                self.init_corpus()
                break
        progress.setValue(itemsCount)
        #self.updateCorpusReaderFilter()
        
    def init_connects(self):
        
        # Menu buttons
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionAboutPoioAnalyzer.triggered.connect(self.about_dialog)
        
        # Push Buttons
        self.ui.buttonAddFiles.pressed.connect(self.add_files)
        self.ui.buttonRemoveFiles.pressed.connect(self.remove_files)

        # Filter and Search
        self.ui.buttonSearch.pressed.connect(self.apply_filter)
        self.ui.buttonCloseThisSearch.pressed.connect(self.search_tab_closed)
        self.ui.buttonClearThisSearch.pressed.connect(self.search_tab_cleared)
        self.ui.tabWidget.currentChanged.connect(self.search_tab_changed)
        #QtCore.QObject.connect(self.ui.buttonSearch, QtCore.SIGNAL("pressed()"), self.applyFilter)
        #QtCore.QObject.connect(self.ui.buttonCloseThisSearch, QtCore.SIGNAL("pressed()"), self.searchTabClosed)
        #QtCore.QObject.connect(self.ui.buttonClearThisSearch, QtCore.SIGNAL("pressed()"), self.searchTabCleared)
        #QtCore.QObject.connect(self.ui.tabWidget, QtCore.SIGNAL("currentChanged(int)"), self.searchTabChanged)
        
        self.ui.listFiles.activated.connect(self.set_current_file_in_result_view)
        self.ui.actionExportSearchResult.triggered.connect(
            self.export_search_results)
        
        #QtCore.QObject.connect(self.ui.lineeditSearchUtterances, QtCore.SIGNAL("returnPressed()"), self.applyFilter)
        #QtCore.QObject.connect(self.ui.lineeditSearchWords, QtCore.SIGNAL("returnPressed()"), self.applyFilter)
        #QtCore.QObject.connect(self.ui.lineeditSearchMorphemes, QtCore.SIGNAL("returnPressed()"), self.applyFilter)
        #QtCore.QObject.connect(self.ui.lineeditSearchGlosses, QtCore.SIGNAL("returnPressed()"), self.applyFilter)
        #QtCore.QObject.connect(self.ui.lineeditSearchTranslations, QtCore.SIGNAL("returnPressed()"), self.applyFilter)
        
        # Quick Search
        #QtCore.QObject.connect(self.ui.actionQuickSearch, QtCore.SIGNAL("triggered()"), self.ui.lineeditQuickSearch.setFocus)
        #QtCore.QObject.connect(self.ui.lineeditQuickSearch, QtCore.SIGNAL("textChanged(const QString &)"), self.findFromStart)
        #QtCore.QObject.connect(self.ui.lineeditQuickSearch, QtCore.SIGNAL("returnPressed()"), self.findNext)

    def init_settings(self):
        QtCore.QCoreApplication.setOrganizationName(
            "Interdisciplinary Centre for Social and Language Documentation");
        QtCore.QCoreApplication.setOrganizationDomain("cidles.eu");
        QtCore.QCoreApplication.setApplicationName("PoioAnalyzer");
        settings = QtCore.QSettings()

    def remove_files(self):
        countRemoved = 0
        for i in self.ui.listFiles.selectedIndexes():
            self.project.removeFilePathAt(i.row()-countRemoved)
            countRemoved = countRemoved + 1
        self.init_corpus()
        self.project.setAllFilesAsNew()
        self.update_corpus_reader()
        self.update_result_view()

    def add_files(self):
        # PySide version
        #filepaths, types = QtGui.QFileDialog.getOpenFileNames(self, self.tr("Add Files"), "", self.tr("Elan files (*.eaf);;Toolbox files (*.txt);;All files (*.*)"))
        # PyQt version
        filepaths = QtGui.QFileDialog.getOpenFileNames(self, self.tr("Add Files"), "", self.tr("Elan files (*.eaf);;Toolbox files (*.txt);;All files (*.*)"))
        #filepaths = QtGui.QFileDialog.getOpenFileNames(self, self.tr("Add Files"), "", self.tr("Elan files (*.eaf);;Toolbox files (*.txt);;Kura files (*.xml);;All files (*.*)"))
        self.project.addFilePaths(filepaths)
        start = time.time()
        self.update_corpus_reader()
        end = time.time()
        print "Time elapsed = ", end - start, "seconds"
        start = time.time()
        self.update_result_view()
        end = time.time()
        print "Time elapsed = ", end - start, "seconds"

    def set_current_file_in_result_view(self, modelIndex):
        obj = self.ui.declarativeviewResult.rootObject()
        # find my column items
        filenameObjects = obj.children()[0].children()
        # file items begin form index 1 in children()
        index = modelIndex.row() + 1
        if index < len(filenameObjects):
            yPosFilename = filenameObjects[index].mapToItem(None, 0, 0).y()
            self.ui.declarativeviewResult.verticalScrollBar().setValue(yPosFilename)
        #pass
        
    def update_result_view(self):
        files = []
        for filepath, annotationtree in self.corpus.items:
            filter = annotationtree.lastFilter()
            elements = []
            for e in annotationtree.elements():
#                utterance = annotationtree.getUtteranceById(id)
#                if id in filter.matchobject["utterance"]:
#                    offset = 0
#                    for g in filter.matchobject["utterance"][id]:
#                        utterance = utterance[:g[0]+offset] + "<span style=\"color:green;\">" + utterance[g[0]+offset:]
#                        offset = offset + len("<span style=\"color:green;\">")
#                        utterance = utterance[:g[1]+offset] + "</span>" + utterance[g[1]+offset:]
#                        offset = offset + len("</span>")
#                translations = annotationtree.getTranslationsForUtterance(id)
#                if len(translations) == 0:
#                    translationId = annotationtree.newTranslationForUtteranceId(id, "")
#                    translations = [ [translationId, self.strEmptyCharacter] ]
#                else:
#                    new_translations = []
#                    for t in translations:
#                        if t[1] == "":
#                            new_t = self.strEmptyCharacter
#                            new_translations.append([t[0], new_t])
#                        if t[0] in filter.matchobject["translation"]:
#                            offset = 0
#                            new_t = t[1]
#                            for g in filter.matchobject["translation"][t[0]]:
#                                new_t = new_t[:g[0]+offset] + "<span style=\"color:green;\">" + new_t[g[0]+offset:]
#                                offset = offset + len("<span style=\"color:green;\">")
#                                new_t = new_t[:g[1]+offset] + "</span>" + new_t[g[1]+offset:]
#                                offset = offset + len("</span>")
#                            new_translations.append([t[0], new_t])
#                        else:
#                            new_translations.append([t[0], t[1]])
#                        translations = new_translations
#                wordIds = annotationtree.getWordIdsForUtterance(id)
#                ilElements = []
#                for wid in wordIds:
#                    strWord = annotationtree.getWordById(wid)
#                    if strWord == "":
#                        strWord = self.strEmptyCharacter
#                    strMorphemes = annotationtree.getMorphemeStringForWord(wid)
#                    #print strMorphemes
#                    if strMorphemes == "":
#                        strMorphemes = strWord
#                    strGlosses = annotationtree.getGlossStringForWord(wid)
#                    if strGlosses == "":
#                        strGlosses = self.strEmptyCharacter
#
#                    markWord = False
#                    if wid in filter.matchobject["word"]:
#                        markWord = True
#                    ilElements.append([wid, strWord, strMorphemes, strGlosses, markWord])
#
#                if len(ilElements) == 0:
#                    ilElements = [['None', self.strEmptyCharacter, self.strEmptyCharacter, self.strEmptyCharacter, self.strEmptyCharacter, False]]
                elements.append(e)

            if elements == []:
                elements = None
            files.append({ "filename" : os.path.basename(filepath), "elements" : elements})
        context = self.ui.declarativeviewResult.rootContext()
        context.setContextProperty("resultModel", files)
        #size = self.ui.declarativeviewResult.sceneRect()

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
        filterChain = []
        for i in range(0, self.ui.tabWidget.currentIndex()+1):
            currentFilter = pyannotation.annotationtree.AnnotationTreeFilter(self.data_structure_type)
            for ann_type in self.data_structure_type.flat_data_hierarchy:
                inputfield = self.ui.tabWidget.findChild(QtGui.QLineEdit, "lineedit_{0}_{1}".format(ann_type, i+1))
                currentFilter.set_filter_for_type(ann_type, unicode(inputfield.text()))

            checkbox = self.ui.tabWidget.findChild(QtGui.QCheckBox, "checkboxInvert_%i"%(i+1))
            currentFilter.set_inverted_filter(checkbox.isChecked())
            checkbox = self.ui.tabWidget.findChild(QtGui.QCheckBox, "checkboxContained_%i"%(i+1))
            currentFilter.set_contained_matches(checkbox.isChecked())
            
            radiobuttonAnd = self.ui.tabWidget.findChild(QtGui.QRadioButton, "radiobuttonAnd_%i"%(i+1))
            radiobuttonOr = self.ui.tabWidget.findChild(QtGui.QRadioButton, "radiobuttonOr_%i"%(i+1))
            if radiobuttonAnd.isChecked():
                currentFilter.set_boolean_operation(pyannotation.annotationtree.AnnotationTreeFilter.AND)
            elif radiobuttonOr.isChecked():
                currentFilter.set_boolean_operation(pyannotation.annotationtree.AnnotationTreeFilter.OR)
            filterChain.append(currentFilter)
    
        for _, annotationtree in self.corpus.items:
            annotationtree.clearFilters()
            for filter in filterChain:
                annotationtree.append_filter(copy.deepcopy(filter))

        #self.updateCorpusReaderFilter()
        self.update_result_view()
        
    def search_tab_changed(self, index):
        if index == self.ui.tabWidget.count() - 1:
            self.add_search_tab()
        else:
            self.apply_filter()
        
    def add_search_tab(self):
        nr_of_new_tab = self.ui.tabWidget.count()
        widget_search = QtGui.QWidget()
        ui = Ui_TabWidgetSearch()
        ui.setupUi(widget_search)
        widget_search.setObjectName("%s_%i" % (widget_search.objectName(), nr_of_new_tab))

        for i, ann_type in enumerate(self.data_structure_type.flat_data_hierarchy):
            #layoutSearch = QtGui.QHBoxLayout(self)
            label = QtGui.QLabel(widget_search)
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(label.sizePolicy().hasHeightForWidth())
            label.setSizePolicy(sizePolicy)
            label.setSizeIncrement(QtCore.QSize(1, 0))
            label.setText(QtGui.QApplication.translate("TabWidgetSearch", "{0}:".format(ann_type), None, QtGui.QApplication.UnicodeUTF8))
            label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
            ui.layoutLabels.addWidget(label)

            lineedit = QtGui.QLineEdit(self.ui.tabWidget)
            lineedit.setSizeIncrement(QtCore.QSize(2, 0))
            lineedit.setObjectName("lineedit_{0}".format(ann_type))
            ui.layoutLineedits.addWidget(lineedit)

            lineedit.returnPressed.connect(self.apply_filter)

            #ui.layoutSearches.addLayout(layoutSearch)

        for childWidget in widget_search.findChildren(QtGui.QWidget):
            if re.match(u"lineeditSearch", childWidget.objectName()):
                QtCore.QObject.connect(childWidget, QtCore.SIGNAL("returnPressed()"), self.apply_filter)
            childWidget.setObjectName("%s_%i" % (childWidget.objectName(), nr_of_new_tab))
        self.ui.tabWidget.insertTab(nr_of_new_tab - 1, widget_search, "Search %i" % nr_of_new_tab)
        self.ui.tabWidget.setCurrentIndex(nr_of_new_tab - 1)    

    def update_search_tab_widget_names(self):
        for i in range(0, self.ui.tabWidget.count()-1):
            widget = self.ui.tabWidget.widget(i)
            for childWidget in widget.findChildren(QtGui.QWidget):
                childWidget.setObjectName("%s_%i" % (childWidget.objectName()[:-2], i+1))
            self.ui.tabWidget.setTabText(i, "Search %i" % (i+1))
            
    def search_tab_closed(self):
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
        widget = self.ui.tabWidget.currentWidget()
        for childWidget in widget.findChildren(QtGui.QWidget):
            if re.match(u"lineeditSearch", childWidget.objectName()):
                childWidget.setText("")
        self.apply_filter()
        
    def about_dialog(self):
        QtGui.QMessageBox.about(self,
            "Poio Analyzer",
            """<b>Poio Analyzer v0.1</b><br><br>
                Linguistic Analyzation Tool for interlinear data,
                developed by Peter Bouda at the<br>
                <b><a href=\"http://www.cidles.eu/ltll/poio\">
                Interdisciplinary Centre for Social and Language Documentation</a></b><br><br>
                Please send bug reports and comments to <b><a href=\"mailto:pbouda@cidles.eu\">
                pbouda@cidles.eu</a></b>."""
        )
    
    def export_search_results(self):
        export_file =  QtGui.QFileDialog.getSaveFileName(self, self.tr("Export Search Result"), "", self.tr("Text file UTF-8 (*.txt)"))
        export_file = unicode(export_file)
        OUT  = codecs.open(export_file, "w", "utf-8")
        for [filepath, annotationtree] in self.corpusreader.annotationtrees:
            OUT.write(filepath + "\n\n")
            utterancesIds = annotationtree.getFilteredUtteranceIds()
            filter = annotationtree.lastFilter()
            utterances = []
            for id in utterancesIds:
                utterance = annotationtree.getUtteranceById(id)

                OUT.write(id + "\n")
                OUT.write(utterance + "\n")

                word_ids = annotationtree.getWordIdsForUtterance(id)
                line_words = ""
                line_morphemes = ""
                line_glosses = ""
                for wid in word_ids:
                    str_word = annotationtree.getWordById(wid)
                    if str_word == "":
                        str_word = self.strEmptyCharacter
                    str_morphemes = annotationtree.getMorphemeStringForWord(wid)
                    #print strMorphemes
                    if str_morphemes == "":
                        str_morphemes = str_word
                    str_glosses = annotationtree.getGlossStringForWord(wid)
                    if str_glosses == "":
                        str_glosses = self.strEmptyCharacter
                        
                    line_words += str_word + " "
                    line_morphemes += str_morphemes + " "
                    line_glosses += str_glosses + " "

                line_words = line_words.rstrip()
                line_morphemes = line_morphemes.rstrip()
                line_glosses = line_glosses.rstrip()
                OUT.write(line_words + "\n")
                OUT.write(line_morphemes + "\n")
                OUT.write(line_glosses + "\n")
                    
                translations = annotationtree.getTranslationsForUtterance(id)
                if len(translations) == 0:
                    translationId = annotationtree.newTranslationForUtteranceId(id, "")
                    translations = [ [translationId, self.strEmptyCharacter] ]
                    
                for t in translations:
                    OUT.write(t[1] +"\n")
                    
                OUT.write("\n")
            OUT.write("\n")
        OUT.close