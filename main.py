# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 09:59:43 2018

@author: ullrich
"""

import tkinter as tk
import binoxxo as bi
from copy import deepcopy
from pprint import pprint
import random

class Application(tk.Frame) :
    def __init__(self,rows,columns,master=None) :
        super().__init__(master)
        
        if rows != columns or rows % 2 != 0 :
            raise ValueError("Binoxxo must be quadratic!")
        
        self.rows = rows
        self.cols = columns
        self.gridcols = columns
        self.gridrows = rows + 2
        self.cellwidth = 10
        self.cellheight = 10
        self.binoxxo = 0
        self.d = {}
        
        self.create_binoxxo()
        self.create_buttons()
        
            
    def leftclick(self,event,row,column) :
        if self.d["t%d%d" %(row,column)].get() == "X" :
            self.d["t%d%d" %(row,column)].set("")
            self.binoxxo.delete_entry(row,column,"X")
        else :
            self.d["t%d%d" %(row,column)].set("X")
            self.binoxxo.add_entry(row,column,"X")
        print("left")
       
    def rightclick(self,event,row,column) :
        if self.d["t%d%d" %(row,column)].get() == "O" :
            self.d["t%d%d" %(row,column)].set("")
            self.binoxxo.delete_entry(row,column,"O")
        else :
            self.d["t%d%d" %(row,column)].set("O")
            self.binoxxo.add_entry(row,column,"O")
        print("right")

    def label_to_dic(self,row,col,color,entry) :
        ltext = tk.StringVar()
        self.d["t%d%d" %(row,col)] = ltext
        self.d["e%d%d" %(row,col)] = tk.Label(width=2,bg=color,textvariable=ltext)
        ltext.set(entry)
        self.d["e%d%d" %(row,col)].grid(row=row,column=col)

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
                    self.label_to_dic(r,c,"lightgrey",entry)
                elif bin_mat[r][c] == 1 :
                    entry = "X"
                    self.label_to_dic(r,c,"lightgrey",entry)
                else :
                    self.label_to_dic(r,c,"white","")
                    self.d["e%d%d" %(r,c)].bind("<Button-1>",lambda event, r=r, c=c:self.leftclick(event,r,c))
                    self.d["e%d%d" %(r,c)].bind("<Button-3>",lambda event, r=r, c=c:self.rightclick(event,r,c))
                
    def check(self,checkm) :
        pprint(self.binoxxo.solution.get_matrix())
        if self.binoxxo.matrix.is_valid() == True :
            checkm.set("Correct!")
        else :  
            checkm.set("Wrong!")        

    def pop_up_reset(self) :
        popup = tk.Toplevel()
        popup.wm_title("Binoxxo: Reset Warning")
        label = tk.Label(popup, text="Do you really want to reset your Binoxxo?")
        label.pack(side="top", fill="x", pady=10)
        B1 = tk.Button(popup, text="Yes", bg = "green" , command = lambda: [self.reset(),popup.destroy()])
        B2 = tk.Button(popup, text="Maybe", bg = "orange", command = lambda: [self.maybe_reset(),popup.destroy()])
        B3 = tk.Button(popup, text="No", bg = "red", command = popup.destroy)
        B1.pack()
        B2.pack()
        B3.pack()

    # this function resets the binoxxo with a 0.5 chance
    def maybe_reset(self) :
        choice = random.randint(0,1)
        if choice == 1 :
            print("maybe resetted")
            self.reset()
        else :
            return

    def reset(self) :
        print("Reset")
        original = self.binoxxo.original.get_matrix()
        for r in range(self.rows) :
            for c in range(self.cols) :
                if original[r][c] != 9 :
                    if original[r][c] == 0 :
                        self.d["t%d%d" %(r,c)].set("O")
                    elif original[r][c] == 1 :
                        self.d["t%d%d" %(r,c)].set("X")
                    self.binoxxo.matrix.set_entry(r,c,deepcopy(original[r][c]))
                else :
                    self.d["t%d%d" %(r,c)].set("")
                    self.binoxxo.matrix.delete_entry(r,c)
                    
    def undo(self) :
        if self.binoxxo.stack == [] :
            return
        op = self.binoxxo.stack.pop()
        if op[2] == 0 :
            op[2] = "O"
        elif op[2] == 1 :
            op[2] = "X"
        elif op[2] == 9 :
            op[2] = ""
        self.binoxxo.matrix.set_entry(op[0],op[1],op[2])
        self.d["t%d%d" %(op[0],op[1])].set(op[2])

    def create_buttons(self) :
        checkm = tk.StringVar()
        checkm.set("")
        check = tk.Button(width=3,text="check",bg="green",command=lambda:self.check(checkm)).grid(row=self.gridrows-1,column=0,columnspan=3)
        message = tk.Label(width=6,textvariable=checkm).grid(row=self.gridrows,column=0,columnspan=3)
        #tk.Button(width=3,text="Reset",bg="yellow",command=lambda:self.reset()).grid(row=self.gridrows-1,column=3,columnspan=3)
        tk.Button(width=3,text="Reset",bg="yellow",command=lambda:self.pop_up_reset()).grid(row=self.gridrows-1,column=3,columnspan=3)
        
        tk.Button(state="normal",width=2,text="Undo",bg="lightblue",command=lambda:self.undo()).grid(row=self.gridrows-1,column=6,columnspan=3)

if __name__ == "__main__" :
    rows = 8
    cols = 8
    
    root = tk.Tk()
    root.title("Binoxxo")
    root.maxsize(width=200, height=300)
    app = Application(rows,cols,master=root)
    app.mainloop()