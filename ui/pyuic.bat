set DIALOGSDIR=..\src\poio\ui
set PYQTTOOLSDIR=C:\Python27\Lib\site-packages\PyQt4
call %PYQTTOOLSDIR%\pyuic4 MainWindow.ui > %DIALOGSDIR%\Ui_MainWindow.py
call %PYQTTOOLSDIR%\pyuic4 MainWindowGRAID.ui > %DIALOGSDIR%\Ui_MainWindowGRAID.py
call %PYQTTOOLSDIR%\pyuic4 MainAnalyzer.ui > %DIALOGSDIR%\Ui_MainAnalyzer.py
call %PYQTTOOLSDIR%\pyuic4 MainAnalyzerQML.ui > %DIALOGSDIR%\Ui_MainAnalyzerQML.py
call %PYQTTOOLSDIR%\pyuic4 TabWidgetSearch.ui > %DIALOGSDIR%\Ui_TabWidgetSearch.py
call %PYQTTOOLSDIR%\pyuic4 Options.ui > %DIALOGSDIR%\Ui_Options.py
call %PYQTTOOLSDIR%\pyuic4 NewTier.ui > %DIALOGSDIR%\Ui_NewTier.py
call %PYQTTOOLSDIR%\pyrcc4 poio.qrc > %DIALOGSDIR%\poio_rc.py
call %PYQTTOOLSDIR%\pyrcc4 poioanalyzer.qrc > %DIALOGSDIR%\poioanalyzer_rc.py
