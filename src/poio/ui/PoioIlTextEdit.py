# -*- coding: utf-8 -*-
# (C) 2009 copyright by Peter Bouda

import os, re
from PyQt4 import QtCore, QtGui
from evoque.template import Template
from lxml import etree

class PoioIlTextEdit(QtGui.QTextEdit):

    def __init__(self, parent):
        QtGui.QTextEdit.__init__(self, parent)
        self.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.setAcceptRichText(False)
        self.setUndoRedoEnabled(False)
        self.setStyleSheet(".match { color:green; }")
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, QtGui.QColor("yellow"))
        self.setPalette(palette)
        QtCore.QObject.connect(self, QtCore.SIGNAL("cursorPositionChanged()"), self.checkCursorPosition)
        settings = QtCore.QSettings()
        self.strEmptyCharacter = unicode(settings.value("Ann/EmptyChar",  QtCore.QVariant("#")).toString())

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            event.accept()
        else:
            QtGui.QTextEdit.keyPressEvent(self, event)

    def insertFromMimeData(self, source):
        text = unicode(source.text())
        text = re.sub(r"[\r\n\a]", "", text)
        self.insertPlainText(text)
        #QtGui.QTextEdit.insertFromMimeData(self, source)
        
    def checkCursorPosition(self):
        if self.isReadOnly():
            return
        c = self.textCursor()
        t = c.currentTable()
        if t == None or c.charFormat().fontCapitalization()==QtGui.QFont.SmallCaps:
            self.setReadOnly(True)
        else:
            self.setReadOnly(False)

    def utteranceIdOfCursor(self):
        c = self.textCursor()
        t = c.currentTable()
        for row in range(t.rows()):
            for column in range(t.columns()):
                cell = t.cellAt(row, column)
        
    def getCurrentUtteranceId(self):
        c = self.textCursor()
        if c == None:
            return ""
        t = c.currentTable()
        if t == None:
            return ""
        utteranceCell = t.cellAt(0, 0)
        utteranceId = unicode(utteranceCell.format().anchorNames()[0])
        utteranceId = re.sub(r"^utterance-", "", utteranceId)
        return utteranceId
        
    def getCurrentWordId(self):
        c = self.textCursor()
        if c == None:
            return ""
        t = c.currentTable()
        if t == None:
            return ""        
        currentCell = t.cellAt(c.position())
        wordidCell = t.cellAt(1, currentCell.column()-1)
        # find last cell that has data of current word
        lastCell = t.cellAt(3, currentCell.column())
        if wordidCell == None or len(wordidCell.format().anchorNames())<1:
            return ""
        wordId = unicode(wordidCell.format().anchorNames()[0])
        wordId = re.sub(r"^word-", "", wordId)
        return wordId

    def deleteCurrentWord(self):
        stringDocumenttext = unicode(self.document().toPlainText())
        c = self.textCursor()
        if c == None:
            return ""
        if not re.search(r"^word-", wordId):
            return ""
        if t == None:
            return ""        
        currentCell = t.cellAt(c.position())
        wordidCell = t.cellAt(1, currentCell.column()-1)
        # find last cell that has data of current word
        lastCell = t.cellAt(3, currentCell.column())
        if wordidCell == None or len(wordidCell.format().anchorNames())<1:
            return ""
        wordId = unicode(wordidCell.format().anchorNames()[0])
        iStart = int(wordidCell.firstCursorPosition().position())
        iEnd = int(lastCell.lastCursorPosition().position())
        c.setPosition(iStart)
        c.setPosition(iEnd, QtGui.QTextCursor.KeepAnchor)
        c.removeSelectedText()
        wordId = re.sub(r"^word-", "", wordId)
        return wordId
        
    def deleteCurrentUtterance(self):
        stringDocumenttext = unicode(self.document().toPlainText())
        c = self.textCursor()
        if c == None:
            return ""
        t = c.currentTable()
        if t == None:
            return ""
        utteranceCell = t.cellAt(0, 0)
        utteranceId = unicode(utteranceCell.format().anchorNames()[0])
        iStart = int(t.firstCursorPosition().position())-2
        iEnd = int(t.lastCursorPosition().position())
        c.setPosition(iStart)
        c.setPosition(iEnd, QtGui.QTextCursor.KeepAnchor)
        c.removeSelectedText()
        utteranceId = re.sub(r"^utterance-", "", utteranceId)
        return utteranceId
        
    def appendTitle(self, title):
        self.setDocumentTitle(title)
        # margin is not working :-(
        self.append("<div style=\"font-size:14pt;\">&nbsp;</div>")
        self.append("<div style=\"font-size:14pt;font-weight:bold;text-decoration:underline;\" id=\"title\" class=\"title\">" + title + "</div>")


    def appendUtterances(self, utterances):
        t = Template(os.path.abspath("html"), "PoioIlUtterances.html")
        text = t.evoque(vars(), quoting="str")
        self.append(text)

    def appendUtterance(self, id,  utterance, ilElements, translations):
        t = Template(os.path.abspath("html"), "PoioIlUtterance.html")
        countwords = len(ilElements)
        text = t.evoque(vars(), quoting="str")
        self.append(text)

        return
    
        c = self.textCursor()
        c.movePosition(QtGui.QTextCursor.End)
        
        # create table
        table = c.insertTable(4, countwords*2+1)
        table.mergeCells(0, 1, 1, countwords*2)
        format = table.format()
        format.setBorder(0)
        table.setFormat(format)
        
        # add utterace
        utteranceCell = table.cellAt(0, 0)
        utteranceCell.firstCursorPosition().insertText(id)
        format = utteranceCell.format()
        format.setFontCapitalization(QtGui.QFont.SmallCaps)
        format.setFontWeight(QtGui.QFont.Bold)
        format.setAnchorNames([id])
        utteranceCell.setFormat(format)
        
        utteranceCell = table.cellAt(0, 1)
        utteranceCell.firstCursorPosition().insertText(utterance)
        format = utteranceCell.format()
        format.setFontWeight(QtGui.QFont.Bold)
        format.setAnchorNames([id])
        utteranceCell.setFormat(format)
        
        elementCell = table.cellAt(1, 0)
        elementCell.firstCursorPosition().insertText("words")
        format = elementCell.format()
        format.setFontCapitalization(QtGui.QFont.SmallCaps)
        elementCell.setFormat(format)
        elementCell = table.cellAt(2, 0)
        elementCell.firstCursorPosition().insertText("morphemes")
        format = elementCell.format()
        format.setFontCapitalization(QtGui.QFont.SmallCaps)
        elementCell.setFormat(format)
        elementCell = table.cellAt(3, 0)
        elementCell.firstCursorPosition().insertText("glosses")
        format = elementCell.format()
        format.setFontCapitalization(QtGui.QFont.SmallCaps)
        elementCell.setFormat(format)
        
        for i in range(countwords):
            # add word
            elementCell = table.cellAt(1, i*2+1)
            format = elementCell.format()
            format.setAnchorNames([ilElements[i][0]])
            elementCell.setFormat(format)
            
            elementCell = table.cellAt(1, i*2+2)
            elementCell.firstCursorPosition().insertText(ilElements[i][1])
            if ilElements[i][4]:
                format = elementCell.format()
                format.setForeground(QGui.QBrush(0,1,0))
                elementCell.setFormat(format)
        
            # add morphemes
            elementCell = table.cellAt(2, i*2+1)
            format = elementCell.format()
            format.setAnchorNames([ilElements[i][0]])
            elementCell.setFormat(format)
            
            elementCell = table.cellAt(2, i*2+2)
            elementCell.firstCursorPosition().insertText(ilElements[i][2])
            if ilElements[i][4]:
                format = elementCell.format()
                format.setForeground(QGui.QBrush(0,1,0))
                elementCell.setFormat(format)

            # add glosses
            elementCell = table.cellAt(3, i*2+1)
            format = elementCell.format()
            format.setAnchorNames([ilElements[i][0]])
            elementCell.setFormat(format)
            
            elementCell = table.cellAt(3, i*2+2)
            elementCell.firstCursorPosition().insertText(ilElements[i][3])
            if ilElements[i][4]:
                format = elementCell.format()
                format.setForeground(QGui.QBrush(0,1,0))
                elementCell.setFormat(format)


    def getAnnotationDict(self):
        root = self.document().rootFrame()
        stringDocumenttext = unicode(self.document().toPlainText())
        dict = {}
        for frame in root.childFrames():
            if frame.__class__.__name__ == "QTextTable":
                # Utterance
                utteranceCell = frame.cellAt(0, 0)
                strUtteranceId = unicode(utteranceCell.format().anchorNames()[0])
                utteranceCell = frame.cellAt(0, 1)
                iStart = int(utteranceCell.firstCursorPosition().position())
                iEnd = int(utteranceCell.lastCursorPosition().position())
                strUtterance = stringDocumenttext[iStart:iEnd].strip()
                if strUtterance == self.strEmptyCharacter:
                    strUtterance = ""
                dict[strUtteranceId] = strUtterance
                # Translation
                translationCell = frame.cellAt(4, 0)
                anch = translationCell.format().anchorNames()
                strTranslationId = unicode(translationCell.format().anchorNames()[0])
                translationCell = frame.cellAt(4, 1)
                iStart = int(translationCell.firstCursorPosition().position())
                iEnd = int(translationCell.lastCursorPosition().position())
                strTranslation = stringDocumenttext[iStart:iEnd].strip()
                if strTranslation == self.strEmptyCharacter:
                    strTranslation = ""
                dict[strTranslationId] = strTranslation
                for i in range((frame.columns()-1)/2):
                    # Words
                    strWordId = unicode(frame.cellAt(1, i*2+1).format().anchorNames()[0])
                    wordCell = frame.cellAt(1, i*2+2)
                    iStart = int(wordCell.firstCursorPosition().position())
                    iEnd = int(wordCell.lastCursorPosition().position())
                    strWord = stringDocumenttext[iStart:iEnd].strip()
                    if strWord == self.strEmptyCharacter:
                        strWord = ""
                    dict[strWordId] = strWord
                    # Morphemes
                    strMorphemesId = re.sub(r"^word-", "morph-", strWordId)
                    morphemesCell = frame.cellAt(2, i*2+2)
                    iStart = int(morphemesCell.firstCursorPosition().position())
                    iEnd = int(morphemesCell.lastCursorPosition().position())
                    strMorphemes = stringDocumenttext[iStart:iEnd].strip()
                    if strMorphemes == self.strEmptyCharacter:
                        strMorphemes = ""
                    dict[strMorphemesId] = strMorphemes
                    # Glosses
                    strGlossesId = re.sub(r"^word-", "gloss-", strWordId)
                    glossesCell = frame.cellAt(3, i*2+2)
                    iStart = int(glossesCell.firstCursorPosition().position())
                    iEnd = int(glossesCell.lastCursorPosition().position())
                    strGlosses = stringDocumenttext[iStart:iEnd].strip()
                    if strGlosses == self.strEmptyCharacter:
                        strGlosses = ""
                    dict[strGlossesId] = strGlosses
                    #strInterlinear = "%s %s %s" % (strWord, strMorphemes, strGlosses)
                    #strInterlinear =strInterlinear.strip()
                    #arrWords.append([strWordId, strInterlinear])
        return dict
    
    def getAnnotationDict_old(self):
        html = unicode(self.toHtml())
        parser = etree.HTMLParser()
        tree  = etree.fromstring(html, parser)
        aElements = tree.findall(".//a[@name]")
        ret = {}
        for aElement in aElements:
            idAnnotation = aElement.attrib["name"]
            annotation = ""
            if idAnnotation == "title":
                for t in aElement.getparent().itertext():
                    annotation = annotation + t
            else:
                for t in aElement.getparent().getparent().getnext().itertext():
                    annotation = annotation + t
            annotation = annotation.strip()
            if annotation == self.strEmptyCharacter:
                annotation = ""
            ret[idAnnotation] = annotation
            #print "%s: %s" % (idAnnotation, annotation)
        return ret
        
    def getAnnotationTree(self):
        root = self.document().rootFrame()
        stringDocumenttext = unicode(self.document().toPlainText())
        tree = []
        for frame in root.childFrames():
            if frame.__class__.__name__ == "QTextTable":
                utteranceCell = frame.cellAt(0, 0)
                strUtteranceId = unicode(utteranceCell.format().anchorNames()[0])
                strUtteranceId = re.sub(r"^utterance-", "", strUtteranceId)
                utteranceCell = frame.cellAt(0, 1)
                iStart = int(utteranceCell.firstCursorPosition().position())
                iEnd = int(utteranceCell.lastCursorPosition().position())
                strUtterance = stringDocumenttext[iStart:iEnd].strip()
                arrWords = []
                for i in range((frame.columns()-1)/2):
                    strWordId = unicode(frame.cellAt(1, i*2+1).format().anchorNames()[0])
                    strWordId = re.sub(r"^word-", "", strWordId)
                    wordCell = frame.cellAt(1, i*2+2)
                    iStart = int(wordCell.firstCursorPosition().position())
                    iEnd = int(wordCell.lastCursorPosition().position())
                    strWord = stringDocumenttext[iStart:iEnd]
                    morphemesCell = frame.cellAt(2, i*2+2)
                    iStart = int(morphemesCell.firstCursorPosition().position())
                    iEnd = int(morphemesCell.lastCursorPosition().position())
                    strMorphemes = stringDocumenttext[iStart:iEnd]
                    glossesCell = frame.cellAt(3, i*2+2)
                    iStart = int(glossesCell.firstCursorPosition().position())
                    iEnd = int(glossesCell.lastCursorPosition().position())
                    strGlosses = stringDocumenttext[iStart:iEnd]
                    strInterlinear = "%s %s %s" % (strWord, strMorphemes, strGlosses)
                    strInterlinear =strInterlinear.strip()
                    arrWords.append([strWordId, strInterlinear])
                tree.append([strUtteranceId, strUtterance, arrWords])
        return tree
