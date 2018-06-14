# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 14:05:43 2018

@author: ullrich
"""

from copy import deepcopy
from pprint import pprint

class Binoxxo_Matrix :
    def __init__(self,rows,cols,init_value) :
        try :
            cols == rows
        except :
            raise ValueError
        self.matrix = [[init_value for _ in range(rows)] for _ in range(cols)]
        self.rows = rows
        self.cols = cols
        self.init = init_value
        
    def get_matrix(self) :
        return deepcopy(self.matrix)
        
    def __getitem__(self,row,col) :
        return self.matrix[row][col]
        
    def get_entry(self,row,col) :
        return self.matrix[row][col]
        
    def set_entry(self,row,col,entry) :
        self.matrix[row][col] = entry
        return
        
    def delete_entry(self,row,col) :
        self.matrix[row][col] = self.init
        return
        
    def transpose(self) :
        matrix = deepcopy(self.matrix)
        for i in range(self.rows) :
            for j in range(i) :
                if i != j :
                    tmp = matrix[i][j]
                    matrix[i][j] = matrix[j][i]
                    matrix[j][i] =  tmp
        return matrix
        
    ### RULES
    # dont count 9s as they are only placeholders
    def has_not_three_in_a_rowcol(self) :
        for row in range(self.rows) :
            for col in range(self.cols) :
                if col > 0 and col < self.cols-1 :
                    if (self.matrix[row][col-1] == self.matrix[row][col] == self.matrix[row][col+1])  and self.matrix[row][col] != 9 :
                        return False
                if row > 0 and row < self.rows-1 :
                    if (self.matrix[row-1][col] == self.matrix[row][col] == self.matrix[row+1][col]) and self.matrix[row][col] != 9 :
                        return False
        return True
        
    def rule_three(self) :
        return self.has_not_three_in_a_rowcol()
        
    #geht 100% einfacher mit list comprehension
    def has_exactly_four_xo_in_rowcol(self) :
        for matrix in [self.matrix,self.transpose()] :
            for line in matrix :
                if line.count(1) > self.rows/2 or line.count(0) > self.rows/2 :
                    return False
        return True
        
    def rule_four(self) :
        return self.has_exactly_four_xo_in_rowcol()
    
    def has_unique_rowcol(self) :
        for row in range(self.rows) :
            for _ in range(row+1,self.rows) :
                # cant check on uniqueness if two entries are missing
                if self.matrix[row].count(9) >= 2 :
                    continue
                if self.matrix[row] == self.matrix[_] :
                    return False
                    
        trans = self.transpose()
        for col in range(self.cols) :
            for _ in range(col+1,self.cols) :
                if trans[col].count(9) >= 2 :
                    continue
                if trans[col] == trans[_] :
                    return False
        return True
        
    def rule_unique(self) :
        return self.has_unique_rowcol()
    ###END RULES    
    
    def is_valid(self) :
        if self.rule_three() and self.rule_four() and self.rule_unique() :
             return True
        else :
            if not self.rule_three() :
                print("THREE")
            elif not self.rule_four() :
                print("FOUR")
            elif not self.rule_unique() :
                print("UNIQUE")
            return False