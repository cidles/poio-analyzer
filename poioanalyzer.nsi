; example2.nsi
;
; This script is based on example1.nsi, but it remember the directory, 
; has uninstall support and (optionally) installs start menu shortcuts.
;
; It will install example2.nsi into a directory that the user selects,

;--------------------------------

; The name of the installer
Name "PoioAnalyzer"

; The file to write
OutFile "setup-poioanalyzer.exe"

; The default installation directory
InstallDir $PROGRAMFILES\Poio\PoioAnalyzer

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\CIDLeS_PoioAnalyzer" "Install_Dir"

;--------------------------------

; Pages

Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------

; The stuff to install
Section "PoioAnalyzer (required)"

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File /r "dist_win\*"
  
  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\CIDLeS_PoioAnalyzer "Install_Dir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PoioAnalyzer" "DisplayName" "PoioAnalyzer"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PoioAnalyzer" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PoioAnalyzer" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PoioAnalyzer" "NoRepair" 1
  WriteUninstaller "uninstall.exe"
  
SectionEnd

; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\Poio Analyzer"
  CreateShortCut "$SMPROGRAMS\Poio Analyzer\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\Poio Analyzer\PoioAnalyzer.lnk" "$INSTDIR\bin\PoioAnalyzer.exe" "" "$INSTDIR\bin\PoioAnalyzer.exe" 0
  
SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PoioAnalyzer"
  DeleteRegKey HKLM SOFTWARE\CIDLeS_PoioAnalyzer

  ; Remove files and uninstaller
  Delete $INSTDIR\bin\*.*
  Delete $INSTDIR\data\examples\*.*
  Delete $INSTDIR\data\qml\*.*
  Delete $INSTDIR\data\*.*
  Delete $INSTDIR\*.*
  ;Delete $INSTDIR\uninstall.exe

  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\Poio Analyzer\Uninstall.lnk"
  Delete "$SMPROGRAMS\Poio Analyzer\Poio GRAID.lnk"
  Delete "$SMPROGRAMS\Poio Analyzer\*.*"

  ; Remove directories used
  RMDir "$SMPROGRAMS\PoioAnalyzer"
  RMDir "$INSTDIR\bin"
  RMDir "$INSTDIR\data\examples"
  RMDir "$INSTDIR\data\qml"
  RMDir "$INSTDIR\data"
  RMDir "$INSTDIR"

SectionEnd
