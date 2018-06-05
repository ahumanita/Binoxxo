# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 14:05:43 2018

@author: ullrich
"""

class Binoxxo_Matrix :
    def __init__(self,rows,cols,init_value) :
        self.matrix = [[init_value for _ in range(rows)] for _ in range(cols)]
        