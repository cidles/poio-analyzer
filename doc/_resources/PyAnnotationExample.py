# -*- coding: utf-8 -*-
# (C) 2012 copyright by Ant�nio Lopes, CIDLeS

from poioapi import annotationtree
from poioapi import data

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