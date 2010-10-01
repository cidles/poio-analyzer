@echo off

set DIALOGSDIR=..\src\poio\ui
set PYQTTOOLSDIR=C:\Python27\Lib\site-packages\PyQt4\bin
%PYQTTOOLSDIR%\pyuic4 MainWindow.ui > %DIALOGSDIR%\Ui_MainWindow.py
%PYQTTOOLSDIR%\pyuic4 MainAnalyzer.ui > %DIALOGSDIR%\Ui_MainAnalyzer.py
%PYQTTOOLSDIR%\pyuic4 Options.ui > %DIALOGSDIR%\Ui_Options.py
%PYQTTOOLSDIR%\pyuic4 NewTier.ui > %DIALOGSDIR%\Ui_NewTier.py
%PYQTTOOLSDIR%\pyrcc4 poio.qrc > %DIALOGSDIR%\poio_rc.py

