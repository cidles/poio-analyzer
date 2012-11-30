***********
Development
***********

How to create a setup.exe on Windows
====================================

Requirements
------------

You need to install the following packages before you compile and create the "setup.exe":

1) Install cx_freeze: http://cx-freeze.sourceforge.net/
2) Install Poio API into local Python installation (run setup.py): https://github.com/cidles/poio-api
3) Install NSIS: http://sourceforge.net/projects/nsis/

To compile and create the "setup.exe":

1) Call "cxfreeze_poiograid.bat" in Poio's main directory. This will compile everything and create a "dist_win" folder, with a "bin" sub-folder.
2) Create an empty sub-folder "data" in "dist_win". This will be used to ship files with Poio.
3) Create an empty file "WINDOWS.txt" in "dist_win/bin". This is used to check whether Poio runs on Windows.
4) Compile "poiograid.nsi" in Poio's main folder with NSIS. This will create a file "setup-poiograid.exe".

To test the setup:

1) Uninstall any existing Poio installation.
2) Run the "setup-poiograid.exe" to test if everything is OK. The setup install Poio to the start menu.