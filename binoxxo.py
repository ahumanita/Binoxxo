# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 14:48:55 2018

@author: ullrich
"""

#TODO: written als Klassenvariable setzen

from random import randint
from pprint import pprint
from copy import deepcopy

import bin_matrix as bm

#do i fill the last row with respect to all other entries in this row

class Binoxxo :
    def __init__(self,rows,cols) :
        try :
            rows % 2 == 0
        except ValueError:
            print("the number of rows and columns must be even.")    
        
        half = int(rows/2)
        
        self.matrix = bm.Binoxxo_Matrix(rows,cols,9)
        self.original = bm.Binoxxo_Matrix(rows,cols,9)
        self.solution = [[9 for i in range(rows)] for i in range(cols)]
        self.entries = {}
        self.rows = rows
        self.cols = cols
        self.rows_zero = [[0 for _ in range(half)] for _ in range(self.rows)]
        self.rows_ones = [[1 for _ in range(half)] for _ in range(self.rows)]
        self.cols_zero = [[0 for _ in range(half)] for _ in range(self.cols)]
        self.cols_ones = [[1 for _ in range(half)] for _ in range(self.cols)]
        self.stack = []
        
    # save the operations in the stack for undo()
    # structure is as follows: [row,col,entry]
    # row and col define the location in the grid
    # entry is the original entry before changes
    def op_to_stack(self,row,col,entry) :
        self.stack.append([row,col,entry])
        
    def set_entry(self,written,row,col,entry) :
        if entry == 1 :
            self.matrix.set_entry(row,col,1)
            self.rows_ones[row] = self.rows_ones[row][:-1]
            self.cols_ones[col] = self.cols_ones[col][:-1]
            written.append(col)
        if entry == 0 :
            self.matrix.set_entry(row,col,0)
            self.rows_zero[row] = self.rows_zero[row][:-1]
            self.cols_zero[col] = self.cols_zero[col][:-1]
            written.append(col)
        return    
    
    #operations that should be used after the creation
    #{
    def delete_entry(self,row,col,content) :
        self.matrix.delete_entry(row,col)
        self.op_to_stack(row,col,content)
        if content == "X" :
            self.rows_ones[row].append(1)
            self.cols_ones[col].append(1)
        elif content == "O" :
            self.rows_zero[row].append(0)
            self.cols_zero[col].append(0)
    
    # add_entry is called, if the user fills an empty grid field
    # set_entry is called, if the program fills a field
    def add_entry(self,row,col,content) :
        print("Row:", row)
        print("Col:", col)
        if content == "X" :
            self.op_to_stack(row,col,self.matrix.get_entry(row,col))
            self.matrix.set_entry(row,col,1)
            self.rows_ones[row] = self.rows_ones[row][:-1]
            self.cols_ones[col] = self.cols_ones[col][:-1]
        elif content == "O" :
            self.op_to_stack(row,col,self.matrix.get_entry(row,col))
            self.matrix.set_entry(row,col,0)
            self.rows_zero[row] = self.rows_zero[row][:-1]
            self.cols_zero[col]  =self.cols_zero[col][:-1]
        else :
            raise ValueError("the entries should be X or O, nothing else.")
    #}
    
    def reload_grid(self) :
        self.matrix = deepcopy(self.original)
    
    # after two same values will be a different one in a column
    def rule1_col(self,row,written) :
        matrix = self.matrix.get_matrix()
        if row > 1 :
            for col in range(self.cols) :
                if col not in written :
                    if matrix[row-1][col] == matrix[row-2][col] and matrix[row-1][col] != 9 :
                        if matrix[row-1][col] == 0 :
                            self.set_entry(written,row,col,1)
                        elif matrix[row-1][col] == 1:
                            self.set_entry(written,row,col,0)
                    elif row < self.rows-1 and matrix[row-1][col] == matrix[row+1][col] and matrix[row-1][col] != 9 :
                        if matrix[row-1][col] == 0 :
                            self.set_entry(written,row,col,1)
                        elif matrix[row-1][col] == 1:
                            self.entry(written,row,col,0)
            return
        else :
            return
            
    def rule2_col(self,row,written) :
        if row == int(self.rows/2) :
            for col in range(self.cols) :
                if col not in written :
                    if len(self.cols_zero[col]) < 2 :
                        self.set_entry(written,row,col,1)
                    elif len(self.cols_ones[col]) < 2 :
                        self.set_entry(written,row,col,0)
            return
        else :
            return
            
    def rule1_row(self,row,col,written) :
        matrix = self.matrix.get_matrix()
        if col > 1 :
            if matrix[row][col-1] == matrix[row][col-2] and matrix[row][col-1] != 9 :
                if matrix[row][col-1] == 0 :
                    self.set_entry(written,row,col,1)
                elif matrix[row][col-1] == 1:
                    self.set_entry(written,row,col,0)
            elif col < self.cols-1 and matrix[row][col-1] == matrix[row][col+1] and matrix[row][col-1] != 9 :
                if matrix[row][col-1] == 0 :
                    self.set_entry(written,row,col,1)
                elif matrix[row][col-1] == 1:
                    self.set_entry(written,row,col,0)
            return
        else :
            return
        
    def rule2_row(self,row,col,written) :
        if col == int(self.cols/2) and col not in written :
            if len(self.rows_zero[row]) < 2 :
                self.set_entry(written,row,col,1)
            elif len(self.rows_ones[row]) < 2 :
                self.set_entry(written,row,col,0)
            return
        else :
            return
            
    def fill_rest(self,row,col,written) :
        if col not in written :
            if len(self.rows_zero[row]) == 0 or len(self.cols_zero[col]) == 0 :
                self.set_entry(written,row,col,1)
            elif len(self.rows_ones[row]) == 0  or len(self.cols_ones[col]) == 0 :
                self.set_entry(written,row,col,0)
            else :
                e = randint(0,1)
                if e == 1 :
                    self.set_entry(written,row,col,1)
                elif e == 0 :
                    self.set_entry(written,row,col,0)
        return
        
    def create_row(self,row) :
        written = []
        if row < self.rows - 1 :
            self.rule1_col(row,written)
            self.rule2_col(row,written)
            if len(written) < self.cols :
                for col in range(self.cols) :
                    if col not in written :
                        self.rule1_row(row,col,written)
                        self.rule2_row(row,col,written)
                        self.fill_rest(row,col,written)
        elif row == self.rows - 1 :
            for col in range(self.cols) :
                self.fill_rest(row,col,written)
        return
        
    def set_shown(self)  :    
        for row in range(self.rows) :
            for col in range(self.cols) :
                show = randint(0,1)
                if show :
                    self.entries[row,col] = self.matrix.get_entry(row,col)
                else :
                    self.matrix.set_entry(row,col,9)
            
    def create(self) :
        for row in range(self.rows) :
            self.create_row(row)
        self.solution = deepcopy(self.matrix)
        self.set_shown()
        self.original = deepcopy(self.matrix)
        return
        
    def binoxxo_is_valid(self) :
        return self.solution.is_valid()
         
    