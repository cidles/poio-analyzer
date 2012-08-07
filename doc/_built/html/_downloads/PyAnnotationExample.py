# -*- coding: utf-8 -*-
# (C) 2012 copyright by António Lopes, CIDLeS

from pyannotation import annotationtree
from pyannotation import data

import pickle

# Initialize the variable
annotation_tree = annotationtree.AnnotationTree(data.GRAID)

# Open the file
file = open('example_data\Balochi Text1.pickle', "rb")
annotation_tree.tree = pickle.load(file)

# Verify the elements
for element in annotation_tree.elements():
    print(element)
    print("\n")