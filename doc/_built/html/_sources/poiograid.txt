.. documentação de projecto documentation master file, created by
   sphinx-quickstart on Thu May 24 17:17:21 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

**********
Poio GRAID
**********

This is the documentation for Poio GRAID. Last updated June 14, 2012.   


Introduction
============  

This document describes the basic funcionalities of Poio GRAID. It shows some of the
facilities that will help you do your work and a brief description of them.
These screenshots show you Poio GRAID's main window, how to create a new file, how
to add and delete utterances and the way to edit them, as well as individual
annotations.      
 

Create a new file
=================
In order to create a new file click on the button "Create a new annotation file"
or choose the menu option "File - New file...". 

.. figure:: _static/images/PoioGRAID_EmtpyStartWindow.png   
   :scale: 50%

   *Figure 1: Main window of Poio* 

A new window "Create a new file" will open (see Figure 2). The window has two options: "Plain Text" and "Toolbox-Style Text". The first option creates a new 
file from a text, the second option creates a new file from a text with given annotations. It is called "Toolbox-Style Text" because the format for
annotations is similar to Toolbox's format, like this:


\id

\sl	(1) ʾána šmíyənwa xa-tunìƟa' 1# yamríwala Gozáli ʾu-Nozàli,' 2# šəmma díya yáʿni tuníƟət Gozáli ʾu-Nozàli.ˈ

\wfw	x I have.heard a-story 1# they.used.to.call.it Gozali and-Nozali 2# name of.it that.is story.of Gozali and-Nozali

\gr_1	x pro.1:a v:pred-1 deti=np:p 1# v:pred-3=pro:p other other 2#

\gr_2	pst 1# pst 0.h:a 2#nc

\ft	I have heard a story called Gozali and Nozali. Its name is the story of Gozali and Nozali

\com


.. figure:: _static/images/Poio_Createanewfile.png 

   *Figure 2: Window "Create a new file"*
  

Plain text files
----------------

To add a file from plain text choose the option "Plain Text" and copy and paste any text into the text box. Each utterance should be in one line 
(see Figure 3).

.. figure:: _static/images/Screenshot_plaintext.png 

   *Figure 3: Adding plain text* 


After pasting the text press "OK". The text gets parsed and is displayed with tokens for clause units and words in the main window 
(see Figure 4).

.. figure:: _static/images/parsedtext.png 
   :scale: 80% 

   *Figure 4: Parsed text* 



Toolbox-Style Text
------------------

To add a file from Toolbox-Style Text choose the option "Toolbox-Style Text". Copy and paste the text into the text box and then press "OK" 
(see Figure 5). 


   *Figure 5: New file from a text with given annotations* 
.. figure:: _static/images/Screenshot_textonotoolbox.png 


The text gets parsed and is displayed with tokens for clause units, words and the translation in the main window (see Figure 6). 

.. figure:: _static/images/Screenshot3styletext.png 
   :scale: 70%

   *Figure 6: Parsed text* 

Saving and opening files
========================

Next to the button "Create a new annotation file" there are two buttons to open and save a file. 

To save a file click on the button "Save File". A file dialog will appear, choose the folder to save the file and enter a filename.
The file will be saved in a format called "pickle", which is an internal format. XML formats will be supported later. 

To open a file again click on "Open File". Choose the file to open. The data will be loaded and presented in the main window. 

Adding and deleting utterances
==============================

The user can add utterances before and after the currently edited utterance block. To insert an utterance before the block with 
the cursor press "Insert utterance before" (see Figure 7). 

.. figure:: _static/images/utterance_before.png 
   :scale: 80%

   *Figure 7: Adding utterance before cursor*

It is also possible to insert one utterance after the block with the cursor. You just need to select the previous utterance and
press the correct button at the top (see Figure 8). 

.. figure:: _static/images/utterance_after.png 
   :scale: 80%

   *Figure 8: Adding utterance after cursor* 

It is also possible to delete one utterance. To delete the utterance block at the cursor position click "Delete utterance". 

Adding and deleting columns
===========================

If you need a new column for a new annotation on the level of the cursor position you can add a new one. Press "Insert empty
column before". Check the utterance "I bought my car last year" at the part of words (see Figure 9). 

.. figure:: _static/images/Screenshot_insertcolbef.png  
   :scale: 80% 

   *Figure 9: Adding column before* 

It is also possible to add an annotation column after the cursor position. Press "Insert empty column after" (see Figure 10).

.. figure:: _static/images/Screenshot_insertcolaft.png 
   :scale: 80%  

   *Figure 10: Adding column after* 

With the option "Delete column" the user can delete a whole column of annotation. Be aware that all annotation of the current
level and all sub-levels are deleted (i.e. if you delete a clause unit all words and other annotations of the clause unit
are removed). 

Find and replace
================
In the menu Edit, select Find and Replace (see Figure 11). 

.. figure:: _static/images/Screenshot-PoioGRAID_edit.png 
   :scale: 50%  

   *Figure 11: Option Find and Replace* 

A new window displays possibilities to search and replace text in the file. Write what you want to find into the text-field
with the label "Find:" and click on the button "Find" to start the search. 

In case that the search string is found in the document, Poio GRAID will mark it with yellow color (see Figure 12). By
pressing "Find" continuously it will look for the same text throughout the document. 

.. figure:: _static/images/Screenshot_dear.png  
   :scale: 50%

   *Figure 12: Underlined text found* 

If no match is found the dialog will display a message "No text found.". 

You can replace strings in the document by entering the search string into the text field "Find:" and the replacement 
string into the text field "Replace with:". First, write the string into the text field "Find:" and press "Find". 
Poio GRAID will mark the found string (see Figure 12). Then, in the text field "Replace with:" enter the replacement 
string and click on the button "Replace" to make this specific change (see Figure 13). 

.. figure:: _static/images/Screenshot_replace.png 
   :scale: 50%  
 
   *Figure 13: Replaced string* 

Also, you can replace the same string in the whole document and not only in a particular place by clicking "Replace All".
Enter the search string into the text field "Find:" and press "Find" button. Next, write the replacement string into 
the text field "Replace with:". To finish, press "Replace All". The dialog will display a success message with the 
number of replacements (see Figure 14). 

.. figure:: _static/images/Screenshot_replaceall1.png 
   :scale: 50%  

   *Figure 14: Total of replaced occurrences*       

