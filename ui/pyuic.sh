#!/bin/bash
DIALOGSDIR=../src/poio/ui
pyuic4 NewTier.ui > $DIALOGSDIR/Ui_NewTier.py
pyuic4 MainWindow.ui > $DIALOGSDIR/Ui_MainWindow.py
pyuic4 MainAnalyzer.ui > $DIALOGSDIR/Ui_MainAnalyzer.py
pyuic4 Options.ui > $DIALOGSDIR/Ui_Options.py
pyrcc4 poio.qrc > $DIALOGSDIR/poio_rc.py

