# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 09:59:43 2018

@author: ullrich
"""

import tkinter as tk
import binoxxo as bi
from copy import deepcopy
from pprint import pprint

class Application(tk.Frame) :
    def __init__(self,rows,columns,master=None) :
        super().__init__(master)
        
        if rows != columns or rows % 2 != 0 :
            raise ValueError
        
        self.rows = rows
        self.cols = columns
        self.columns = columns + 1
        self.cellwidth = 10
        self.cellheight = 10
        self.binoxxo = 0
        self.d = {}
        self.texts = {}
        self.create_binoxxo()
        self.create_buttons()
        
        #self.basic_matrix = deepcopy(binoxxo.matrix)
        
    def create_grid(self) :        
        d = {}
        for r in range(0,self.rows) :
            for c in range(0,self.coluns) :
                d["e%d%d" %(r,c)] = tk.Entry(width=2).grid(row=r,column=c)
            
    def leftclick(self,event,row,column) :
        if self.texts["e%d%d" %(row,column)].get() == "X" :
            self.texts["e%d%d" %(row,column)].set("")
            self.binoxxo.delete_entry(row,column,"X")
        else :
            self.texts["e%d%d" %(row,column)].set("X")
            self.binoxxo.add_entry(row,column,"X")
        print("left")
       
    def rightclick(self,event,row,column) :
        if self.texts["e%d%d" %(row,column)].get() == "O" :
            self.texts["e%d%d" %(row,column)].set("")
            self.binoxxo.delete_entry(row,column,"O")
        else :
            self.texts["e%d%d" %(row,column)].set("O")
            self.binoxxo.add_entry(row,column,"O")
        print("right")

    # def create_binoxxo(self) :
    #     d = {}
    #     it = 0
    #     valid = False
    #     while not valid and it < 100 :
    #         self.binoxxo = bi.Binoxxo(self.rows,self.cols)
    #        matrix self.binoxxo.create()
    #         valid = self.binoxxo.is_valid()
    #         it += 1
    #         print(valid)
    #         print(it)        
    #     for r in range(0,self.rows) :
    #         for c in range(0,self.cols) :
    #             if (r,c) in self.binoxxo.entries.keys() :
    #                 entry = ""
    #                 if self.binoxxo.entries[(r,c)] == 0 :
    #                     entry = "O"
    #                 elif self.binoxxo.entries[(r,c)] == 1:
    #                     entry = "X"
    #                 d["e%d%d" %(r,c)] = tk.Label(width=3,height=1,text=entry).grid(row=r,column=c)
    #             else :
    #                 d["d%d%d" %(r,c)] = tk.StringVar()
    #                 d["e%d%d" %(r,c)] = tk.Label(width=2,bg="white")
    #                 d["e%d%d" %(r,c)].grid(row=r,column=c)
    #                 d["e%d%d" %(r,c)].bind("<Button-1>",lambda event, r=r, c=c:self.leftclick(event,r,c))
    #                 d["e%d%d" %(r,c)].bind("<Button-3>",lambda event, r=r, c=c:self.rightclick(event,r,c))    
    
    def create_binoxxo(self) :
        self.d = {}
        it = 0
        valid = False
        while not valid and it < 1000 :
            self.binoxxo = bi.Binoxxo(self.rows,self.cols)
            self.binoxxo.create()
            valid = self.binoxxo.binoxxo_is_valid()
            it += 1
            print(valid)
            print(it)   
        bin_mat = self.binoxxo.matrix.get_matrix()     
        for r in range(0,self.rows) :
            for c in range(0,self.cols) :
                entry = ""
                if bin_mat[r][c] == 0 :
                    entry = "O"
                    ltext = tk.StringVar()
                    self.texts["e%d%d" %(r,c)] = ltext
                    self.d["e%d%d" %(r,c)] = tk.Label(width=3,height=1,textvariable=ltext)
                    ltext.set(entry)
                    self.d["e%d%d" %(r,c)].grid(row=r,column=c)
                elif bin_mat[r][c] == 1 :
                    entry = "X"
                    ltext = tk.StringVar()
                    self.texts["e%d%d" %(r,c)] = ltext
                    self.d["e%d%d" %(r,c)] = tk.Label(width=3,height=1,textvariable=ltext)
                    ltext.set(entry)
                    self.d["e%d%d" %(r,c)].grid(row=r,column=c)
                else :
                    ltext = tk.StringVar()
                    self.texts["e%d%d" %(r,c)] = ltext
                    self.d["e%d%d" %(r,c)] = tk.Label(width=2,bg="white",textvariable=ltext)
                    ltext.set("")
                    self.d["e%d%d" %(r,c)].grid(row=r,column=c)
                    self.d["e%d%d" %(r,c)].bind("<Button-1>",lambda event, r=r, c=c:self.leftclick(event,r,c))
                    self.d["e%d%d" %(r,c)].bind("<Button-3>",lambda event, r=r, c=c:self.rightclick(event,r,c))
                
    
    #TODO: nochmal testen, nachdem die Benutzereinträge gespeichert wurden
    #TODO: an neue Struktur anpassen!
    def check(self,checkm) :
        pprint(self.binoxxo.solution.get_matrix())
        # das passt so noch nicht zur neuen struktur!!
        if self.binoxxo.binoxxo_is_valid() == True :
            checkm.set("Correct!")
        else :  
            checkm.set("Wrong!")        

    def reset(self) :
        print("Reset")
        original = self.binoxxo.original.get_matrix()
        for r in range(self.rows) :
            for c in range(self.cols) :
                if original[r][c] != 9 :
                    if original[r][c] == 0 :
                        self.texts["e%d%d" %(r,c)].set("O")
                    elif original[r][c] == 1 :
                        self.texts["e%d%d" %(r,c)].set("X")
                    self.binoxxo.matrix.set_entry(r,c,deepcopy(original[r][c]))
                else :
                    self.texts["e%d%d" %(r,c)].set("")
                    self.binoxxo.matrix.delete_entry(r,c)
        return

    def create_buttons(self) :
        checkm = tk.StringVar()
        checkm.set("")
        check = tk.Button(width=3,text="check",bg="green",command=lambda:self.check(checkm)).grid(row=0,column=self.columns)
        message = tk.Label(width=6,textvariable=checkm).grid(row=1,column=self.columns)
        #print(self.d)
        tk.Button(width=3,text="Reset",bg="yellow",command=lambda:self.reset()).grid(row=3,column=self.columns)

if __name__ == "__main__" :
    rows = 8
    cols = 8
    
    root = tk.Tk()
    root.title("Binoxxo")
    root.maxsize(width=200, height=300)
    app = Application(rows,cols,master=root)
    app.mainloop()