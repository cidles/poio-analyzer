.. documentação de projecto documentation master file, created by
   sphinx-quickstart on Thu May 24 17:17:21 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

**********
Tutorials
**********

This is the documentation for Python Linguistic Annotation Libary (PyAnnotation).

Introduction
============  

This document represents a simple example how to access to the result elements with Python Linguistic Annotation Libary (PyAnnotation).

The Installion Guide can be consulted in https://github.com/cidles/Poio

Before we get to the example is important to be familiar with the data structure used in PyAnnotation.

The data structure used in it is based in GRAID annotations (For more detailed information http://www.linguistik.uni-kiel.de/GRAID_manual6.0_08sept.pdf)

Data Structure [GRAID Structure]
::
	[ 'utterance',
		[ 'clause unit',
			[ 'word', 'wfw', 'graid1' ],
		'graid2' ],
	  'translation', 'comment' ]
   
Retrieve Elements
=================

The first step is to initialize the variable:
::
	annotation_tree = annotationtree.AnnotationTree(data.GRAID)

The AnnotationTree will contain the hierarchy and relations between the elements between which sentence, word, wfw and it's translation.
In this step what is done is to set the data structure type of the tree with **AnnotationTree(data.GRAID)**.

The second step is to open the file (in the example_data folder there are some example files):
::
	file = open('example_file.pickle', "rb")
	annotation_tree.tree = pickle.load(file)

At this point is important to know that the file should be a **pickle** file and must be previously created with PoioUI (https://github.com/cidles/Poio).

The third step is to examine the resulted elements:
::
	for element in annotation_tree.elements():
		print(element)

		
Results
-------

The result to the second element should be like this (using the provided file :download:`Balochi Text1.pickle<_resources/Balochi Text1.pickle>`):

Original Result:
::
	[{'id': 20, 'annotation': u'ki\tyag\tb\u0101di\u0161\u0101=(y)\u0113=at'}, [[{'id': 18, 'annotation': u'ki\tyag\tb\u0101di\u0161\u0101=(y)\u0113=at'}, [[{'id': 9, 'annotation': u'ki'}, {'id': 10, 'annotation': u'SUB'}, {'id': 11, 'annotation': u'comp'}], [{'id': 12, 'annotation': u'yag'}, {'id': 13, 'annotation': u'one'}, {'id': 14, 'annotation': u'deti'}], [{'id': 15, 'annotation': u'b\u0101di\u0161\u0101=(y)\u0113=at'}, {'id': 16, 'annotation': u'king=IND=COP.PST.3SG'}, {'id': 17, 'annotation': u'np.h:s=cop:predp'}]], {'id': 19, 'annotation': u''}]], {'id': 21, 'annotation': u'that there was a king.'}, {'id': 22, 'annotation': u''}]

Indenting to the data structure format:
::
	[{'id': 20, 'annotation': u'ki\tyag\tb\u0101di\u0161\u0101=(y)\u0113=at'},
		[[{'id': 18, 'annotation': u'ki\tyag\tb\u0101di\u0161\u0101=(y)\u0113=at'},
			[[{'id': 9, 'annotation': u'ki'}, {'id': 10, 'annotation': u'SUB'}, {'id': 11, 'annotation': u'comp'}],
			 [{'id': 12, 'annotation': u'yag'}, {'id': 13, 'annotation': u'one'}, {'id': 14, 'annotation': u'deti'}],
			 [{'id': 15, 'annotation': u'b\u0101di\u0161\u0101=(y)\u0113=at'}, {'id': 16, 'annotation': u'king=IND=COP.PST.3SG'}, {'id': 17, 'annotation': u'np.h:s=cop:predp'}]],
		  {'id': 19, 'annotation': u''}]],
	 {'id': 21, 'annotation': u'that there was a king.'}, {'id': 22, 'annotation': u''}]

Changing 'annotation' to the GRAID annotations like in the data structure:
::
	[{'id': 20, 'utterance': u'ki\tyag\tb\u0101di\u0161\u0101=(y)\u0113=at'},
		[[{'id': 18, 'clause unit': u'ki\tyag\tb\u0101di\u0161\u0101=(y)\u0113=at'},
			[[{'id': 9, 'word': u'ki'}, {'id': 10, 'wfw': u'SUB'}, {'id': 11, 'graid1': u'comp'}],
			 [{'id': 12, 'word': u'yag'}, {'id': 13, 'wfw': u'one'}, {'id': 14, 'graid1': u'deti'}],
			 [{'id': 15, 'word': u'b\u0101di\u0161\u0101=(y)\u0113=at'}, {'id': 16, 'wfw': u'king=IND=COP.PST.3SG'}, {'id': 17, 'graid1': u'np.h:s=cop:predp'}]],
		  {'id': 19, 'graid2': u''}]],
	 {'id': 21, 'translation': u'that there was a king.'}, {'id': 22, 'comment': u''}]
 
In the end the realtion should be like this:

.. figure:: _static/images/relation.png
   :scale: 50%
   :width: 700px
   :align: center
   
   *Figure 1: Relation between the results and the data structure*
   
Resources
=========
Source File :download:`PyAnnotationExample.py<_resources/PyAnnotationExample.py>`.