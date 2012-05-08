; example2.nsi
;
; This script is based on example1.nsi, but it remember the directory, 
; has uninstall support and (optionally) installs start menu shortcuts.
;
; It will install example2.nsi into a directory that the user selects,

;--------------------------------

; The name of the installer
Name "PoioGRAID"

; The file to write
OutFile "setup-poiograid.exe"

; The default installation directory
InstallDir $PROGRAMFILES\Poio\PoioGRAID

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\CIDLeS_PoioGRAID" "Install_Dir"

;--------------------------------

; Pages

Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------

; The stuff to install
Section "Poio GRAID (required)"

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File /r "dist_win\*"
  
  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\CIDLeS_PoioGRAID "Install_Dir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PoioGRAID" "DisplayName" "Poio GRAID"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PoioGRAID" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PoioGRAID" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PoioGRAID" "NoRepair" 1
  WriteUninstaller "uninstall.exe"
  
SectionEnd

; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\Poio GRAID"
  CreateShortCut "$SMPROGRAMS\Poio GRAID\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\Poio GRAID\Poio GRAID.lnk" "$INSTDIR\bin\PoioGRAID.exe" "" "$INSTDIR\bin\PoioGRAID.exe" 0
  
SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PoioGRAID"
  DeleteRegKey HKLM SOFTWARE\CIDLeS_PoioGRAID

  ; Remove files and uninstaller
  Delete $INSTDIR\bin\*.*
  Delete $INSTDIR\data\translations\*.*
  Delete $INSTDIR\data\*.*
  Delete $INSTDIR\*.*
  ;Delete $INSTDIR\uninstall.exe

  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\Poio GRAID\Uninstall.lnk"
  Delete "$SMPROGRAMS\Poio GRAID\Poio GRAID.lnk"
  Delete "$SMPROGRAMS\Poio GRAID\*.*"

  ; Remove directories used
  RMDir "$SMPROGRAMS\PoioGRAID"
  RMDir "$INSTDIR\bin"
  RMDir "$INSTDIR\data\translations"
  RMDir "$INSTDIR\data"
  RMDir "$INSTDIR"

SectionEnd
