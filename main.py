# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 09:59:43 2018

@author: ullrich
"""

import tkinter as tk
import binoxxo as bi
from copy import deepcopy

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
        self.create_binoxxo()
        self.create_buttons()
        #self.basic_matrix = deepcopy(binoxxo.matrix)
        
    def create_grid(self) :        
        d = {}
        for r in range(0,self.rows) :
            for c in range(0,self.coluns) :
                d["e%d%d" %(r,c)] = tk.Entry(width=2).grid(row=r,column=c)
            
    def leftclick(self,event,row,column) :
        if event.widget["text"] == "X" :
            event.widget.config(text="")
            self.binoxxo.delete_entry(row,column)
        else :
            event.widget.config(text="X")
            self.binoxxo.add_entry(row,column,"X")
        print("left")
       
    def rightclick(self,event,row,column) :
        if event.widget["text"] == "O" :
            event.widget.config(text="")
            self.binoxxo.delete_entry(row,column)
        else :
            event.widget.config(text="O")
            self.binoxxo.add_entry(row,column,"O")
        print("right")

    def create_binoxxo(self) :
        d = {}
        it = 0
        valid = False
        while not valid and it < 100 :
            self.binoxxo = bi.Binoxxo(self.rows,self.cols)
            self.binoxxo.create()
            valid = self.binoxxo.is_valid()
            it += 1
            print(valid)
            print(it)        
        for r in range(0,self.rows) :
            for c in range(0,self.cols) :
                if (r,c) in self.binoxxo.entries.keys() :
                    entry = ""
                    if self.binoxxo.entries[(r,c)] == 0 :
                        entry = "O"
                    elif self.binoxxo.entries[(r,c)] == 1:
                        entry = "X"
                    d["e%d%d" %(r,c)] = tk.Label(width=3,height=1,text=entry).grid(row=r,column=c)
                else :
                    d["d%d%d" %(r,c)] = tk.StringVar()
                    d["e%d%d" %(r,c)] = tk.Label(width=2,bg="white")
                    d["e%d%d" %(r,c)].grid(row=r,column=c)
                    d["e%d%d" %(r,c)].bind("<Button-1>",lambda event, r=r, c=c:self.leftclick(event,r,c))
                    d["e%d%d" %(r,c)].bind("<Button-3>",lambda event, r=r, c=c:self.rightclick(event,r,c))    
    
    #TODO: nochmal testen, nachdem die Benutzereinträge gespeichert wurden
    def check(self,checkm) :
        if self.binoxxo.is_valid() == True :
            checkm.set("Correct!")
        else :  
            checkm.set("Wrong!")        

    def create_buttons(self) :
        checkm = tk.StringVar()
        checkm.set("")
        check = tk.Button(width=3,text="check",bg="green",command=lambda:self.check(checkm)).grid(row=0,column=self.columns)
        message = tk.Label(width=6,textvariable=checkm).grid(row=1,column=self.columns)

if __name__ == "__main__" :
    rows = 8
    cols = 8
    
    root = tk.Tk()
    root.title("Binoxxo")
    root.maxsize(width=200, height=300)
    app = Application(rows,cols,master=root)
    app.mainloop()