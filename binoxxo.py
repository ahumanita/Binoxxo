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
        self.original = [[9 for i in range(rows)] for i in range(cols)]
        self.solution = [[9 for i in range(rows)] for i in range(cols)]
        self.entries = {}
        self.rows = rows
        self.cols = cols
        self.rows_zero = [[0 for _ in range(half)] for _ in range(self.rows)]
        self.rows_ones = [[1 for _ in range(half)] for _ in range(self.rows)]
        self.cols_zero = [[0 for _ in range(half)] for _ in range(self.cols)]
        self.cols_ones = [[1 for _ in range(half)] for _ in range(self.cols)]
        
    def set_entry(self,written,row,col,entry) :
        if entry == 1 :
            self.matrix[row][col] = 1
            self.rows_ones[row] = self.rows_ones[row][:-1]
            self.cols_ones[col] = self.cols_ones[col][:-1]
            written.append(col)
        if entry == 0 :
            self.matrix[row][col] = 0
            self.rows_zero[row] = self.rows_zero[row][:-1]
            self.cols_zero[col] = self.cols_zero[col][:-1]
            written.append(col)
        return    
    
    #operations that should be used after the creation
    #{
    def delete_entry(self,row,col,content) :
        self.matrix[row][col] = 9
        if content == "X" :
            self.rows_ones[row].append(1)
            self.cols_ones[col].append(1)
        elif content == "O" :
            self.rows_zero[row].append(0)
            self.cols_zero[col].append(0)
        
    #TODO: es kann nicht sien, dass manche felder von anfang an false sind, wenn ich es immer überprüfe. Was passiert bei der Überprüfung? muss ihc das noch abändern?
    
    
    
    def add_entry(self,row,col,content) :
        print("Row:", row)
        print("Col:", col)
        if content == "X" :
            self.matrix[row][col] = 1
            self.rows_ones[row] = self.rows_ones[row][:-1]
            self.cols_ones[col] = self.cols_ones[col][:-1]
        elif content == "O" :
            self.matrix[row][col] = 0
            self.rows_zero[row] = self.rows_zero[row][:-1]
            self.cols_zero[col]  =self.cols_zero[col][:-1]
        else :
            raise ValueError("the entries should be X or O, nothing else.")
        pprint(self.matrix)
    #}
    
    def reload_grid(self) :
        self.matrix = deepcopy(self.original)
    
    # after two same values will be a different one in a column
    def rule1_col(self,row,written) :
        if row > 1 :
            for col in range(self.cols) :
                if col not in written :
                    if self.matrix[row-1][col] == self.matrix[row-2][col] and self.matrix[row-1][col] != 9 :
                        if self.matrix[row-1][col] == 0 :
                            self.set_entry(written,row,col,1)
                        elif self.matrix[row-1][col] == 1:
                            self.set_entry(written,row,col,0)
                    elif row < self.rows-1 and self.matrix[row-1][col] == self.matrix[row+1][col] and self.matrix[row-1][col] != 9 :
                        if self.matrix[row-1][col] == 0 :
                            self.set_entry(written,row,col,1)
                        elif self.matrix[row-1][col] == 1:
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
        if col > 1 :
            if self.matrix[row][col-1] == self.matrix[row][col-2] and self.matrix[row][col-1] != 9 :
                if self.matrix[row][col-1] == 0 :
                    self.set_entry(written,row,col,1)
                elif self.matrix[row][col-1] == 1:
                    self.set_entry(written,row,col,0)
            elif col < self.cols-1 and self.matrix[row][col-1] == self.matrix[row][col+1] and self.matrix[row][col-1] != 9 :
                if self.matrix[row][col-1] == 0 :
                    self.set_entry(written,row,col,1)
                elif self.matrix[row][col-1] == 1:
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
                    self.entries[row,col] = self.matrix[row][col]
                else :
                    self.matrix[row][col] = 9
            
    def create(self) :
        for row in range(self.rows) :
            self.create_row(row)
        self.solution = deepcopy(self.matrix)
        self.set_shown()
        self.original = deepcopy(self.matrix)
        return
        
    # #check on valid part
    # def rule_three(self) :
    #     three = False
    #     for row in range(self.rows) :
    #         for col in range(self.cols) :
    #             if col > 0 and col < self.cols-1 :
    #                 three = self.matrix[row][col-1] == self.matrix[row][col] == self.matrix[row][col+1]
    #                 if three :
    #                     return not three
    #             if row > 0 and row < self.rows-1 :
    #                 three = self.matrix[row-1][col] == self.matrix[row][col] == self.matrix[row+1][col]
    #                 if three : 
    #                     return not three
    #     return not three
        #check on valid part
    def rule_three(self) :
        three = False
        for row in range(self.rows) :
            for col in range(self.cols) :
                if col > 0 and col < self.cols-1 :
                    three = self.original[row][col-1] == self.original[row][col] == self.original[row][col+1]
                    if three :
                        return not three
                if row > 0 and row < self.rows-1 :
                    three = self.original[row-1][col] == self.original[row][col] == self.original[row+1][col]
                    if three : 
                        return not three
        return not three
        
    # def rule_four(self) :
    #     four = True
    #     for _ in range(self.rows) :
    #         if len(self.rows_zero[_]) > 0 or len(self.rows_ones[_]) > 0 :
    #             four = False
    #     for _ in range(self.cols) :
    #         if len(self.cols_zero[_]) > 0 or len(self.cols_ones[_]) > 0 :
    #             four = False
    #     return four
    
    def rule_four(self) :
        four = True
        count_1 = 0
        count_0 = 0
        for i in range(self.rows) :
            for j in self.matrix[i] :
                if j == 1 :
                    count_1 += 1
                elif j == 0 :
                    count_0 += 1
            if count_0 > self.rows/2 or count_1 > self.rows/2 :
                four = False
            count_0 = 0
            count_1 = 0
        return four
        
    def rule_unique(self) :
        unique = True
        for row in range(self.rows) :
            for _ in range(row+1,self.rows) :
                if self.matrix[row] == self.matrix[_] :
                    unique = False
        transpose = [list(x) for x in zip(*self.matrix)]
        for col in range(self.cols) :
            for _ in range(col+1,self.cols) :
                if transpose[col] == transpose[_] :
                    unique = False
        return unique
        
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
         
    