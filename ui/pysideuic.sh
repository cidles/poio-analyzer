#!/bin/bash
DIALOGSDIR=../src/poio/ui
CMDUIC=pyside-uic
CMDRRC=pyside-rcc

$CMDUIC NewTier.ui > $DIALOGSDIR/Ui_NewTier.py
$CMDUIC MainWindow.ui > $DIALOGSDIR/Ui_MainWindow.py
$CMDUIC MainAnalyzer.ui > $DIALOGSDIR/Ui_MainAnalyzer.py
$CMDUIC MainAnalyzerQML.ui > $DIALOGSDIR/Ui_MainAnalyzerQML.py
$CMDUIC TabWidgetSearch.ui > $DIALOGSDIR/Ui_TabWidgetSearch.py
$CMDUIC Options.ui > $DIALOGSDIR/Ui_Options.py
$CMDRRC poio.qrc > $DIALOGSDIR/poio_rc.py
$CMDRRC poioanalyzer.qrc > $DIALOGSDIR/poioanalyzer_rc.py

