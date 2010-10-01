; example2.nsi
;
; This script is based on example1.nsi, but it remember the directory, 
; has uninstall support and (optionally) installs start menu shortcuts.
;
; It will install example2.nsi into a directory that the user selects,

;--------------------------------

; The name of the installer
Name "PoioILE"

; The file to write
OutFile "setup-poioile.exe"

; The default installation directory
InstallDir $PROGRAMFILES\PoioILE

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\CIDLeS_PoioILE" "Install_Dir"

;--------------------------------

; Pages

Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------

; The stuff to install
Section "PoioILE (required)"

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File /r "dist_win\*"
  
  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\CIDLeS_PoioILE "Install_Dir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PoioILE" "DisplayName" "PoioILE"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PoioILE" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PoioILE" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PoioILE" "NoRepair" 1
  WriteUninstaller "uninstall.exe"
  
SectionEnd

; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\PoioILE"
  CreateShortCut "$SMPROGRAMS\PoioILE\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\PoioILE\PoioILE.lnk" "$INSTDIR\PoioILE.exe" "" "$INSTDIR\PoioILE.exe" 0
  
SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PoioILE"
  DeleteRegKey HKLM SOFTWARE\CIDLeS_PoioILE

  ; Remove files and uninstaller
  Delete $INSTDIR\*.*
  Delete $INSTDIR\examples\*.*
  Delete $INSTDIR\html\*.*
  Delete $INSTDIR\pixmaps\*.*
  ;Delete $INSTDIR\uninstall.exe

  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\PoioILE\*.*"

  ; Remove directories used
  RMDir "$SMPROGRAMS\PoioILE"
  RMDir "$INSTDIR\examples"
  RMDir "$INSTDIR\html"
  RMDir "$INSTDIR\pixmaps"
  RMDir "$INSTDIR"

SectionEnd
