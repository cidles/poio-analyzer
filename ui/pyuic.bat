set DIALOGSDIR=..\src\poio\ui
set PYQTTOOLSDIR=C:\Python33\Lib\site-packages\PyQt4
call %PYQTTOOLSDIR%\pyuic4 MainWindow.ui > %DIALOGSDIR%\Ui_MainWindow.py
call %PYQTTOOLSDIR%\pyuic4 MainWindowGRAID.ui > %DIALOGSDIR%\Ui_MainWindowGRAID.py
call %PYQTTOOLSDIR%\pyuic4 MainAnalyzer.ui > %DIALOGSDIR%\Ui_MainAnalyzer.py
call %PYQTTOOLSDIR%\pyuic4 MainAnalyzerQML.ui > %DIALOGSDIR%\Ui_MainAnalyzerQML.py
call %PYQTTOOLSDIR%\pyuic4 MainAnalyzerHTML.ui > %DIALOGSDIR%\Ui_MainAnalyzerHTML.py
call %PYQTTOOLSDIR%\pyuic4 TabWidgetSearch.ui > %DIALOGSDIR%\Ui_TabWidgetSearch.py
call %PYQTTOOLSDIR%\pyuic4 Options.ui > %DIALOGSDIR%\Ui_Options.py
call %PYQTTOOLSDIR%\pyuic4 NewTier.ui > %DIALOGSDIR%\Ui_NewTier.py
call %PYQTTOOLSDIR%\pyuic4 NewFileGraid.ui > %DIALOGSDIR%\Ui_NewFileGraid.py
call %PYQTTOOLSDIR%\pyuic4 FindReplaceForm.ui > %DIALOGSDIR%\Ui_FindReplaceForm.py
call %PYQTTOOLSDIR%\pyuic4 FindReplaceDialog.ui > %DIALOGSDIR%\Ui_FindReplaceDialog.py
call %PYQTTOOLSDIR%\pyrcc4 poio.ui.poio.qrc > %DIALOGSDIR%\poio_rc.py -py3
call %PYQTTOOLSDIR%\pyrcc4 poio.ui.poioanalyzer.qrc > %DIALOGSDIR%\poioanalyzer_rc.py -py3
