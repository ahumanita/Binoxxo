# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 09:59:43 2018

@author: ullrich
"""

import tkinter as tk
import binoxxo as bi
from copy import deepcopy
from pprint import pprint

from variables_main import *
from helper_functions import *

class Application(tk.Frame) :
    def __init__(self,rows,columns,master=None) :
        super().__init__(master)
        
        if rows != columns or rows % 2 != 0 :
            raise ValueError("Binoxxo must be quadratic!")
        
        print("SIZE",master.winfo_width())
        
        self.rows = rows
        self.cols = columns
        self.gridcols = columns + 1
        self.gridrows = rows + 3
        self.cellwidth = CELLWIDTH
        self.cellheight = CELLHEIGHT
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

    def label_to_dic_sol(self,row,col,color,entry) :
        ltext = tk.StringVar()
        self.d["ts%d%d" %(row,col)] = ltext
        self.d["s%d%d" %(row,col)] = tk.Label(width=2,bg=color,textvariable=ltext)
        ltext.set(entry)
        self.d["s%d%d" %(row,col)].grid(row=row,column=col+self.cols+1)

    def create_binoxxo(self) :
        self.d = {}
        it = 0
        valid = False
        while not valid and it < MAX_IT :
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
                #create solution grid
                entry = ""
                self.label_to_dic_sol(r,c,"lightgrey",entry)
        #create dummy between binoxxo and solution
        #and between binoxxo and buttons
        tk.Label(width=2).grid(row=0,column=self.cols)
        tk.Label(height=1).grid(row=self.rows+1,column=0)
                
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
        choice = decision(CHANCE_RESET)
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
    
    def pop_up_new(self) :
        popup = tk.Toplevel()
        popup.wm_title("Binoxxo: Load New Warning")
        label = tk.Label(popup, text="Do you really want a new Binoxxo?")
        label.pack(side="top", fill="x", pady=10)
        B1 = tk.Button(popup, text="Yes", bg = "green" , command = lambda: [self.load_new(),popup.destroy()])
        B2 = tk.Button(popup, text="Maybe", bg = "orange", command = lambda: [self.maybe_load_new(),popup.destroy()])
        B3 = tk.Button(popup, text="No", bg = "red", command = popup.destroy)
        B1.pack()
        B2.pack()
        B3.pack()
        
    def maybe_load_new(self) :
        choice = decision(CHANCE_LOAD_NEW)
        if choice == 1 :
            print("maybe reloaded")
            self.load_new()
        else :
            return
        
    def load_new(self) :
        print("new")
        self.create_binoxxo()
        self.binoxxo.stack = []
        
    def show_solution(self) :
        print("solution")
        #if solution is hidden, show solution
        if self.d["ts%d%d" %(0,0)].get() == "" :
            sol = self.binoxxo.solution.get_matrix()
            for row in range(self.rows) :
                for col in range(self.cols) :
                    if sol[row][col] == 0 :
                        self.d["ts%d%d" %(row,col)].set("O")
                    elif sol[row][col] == 1 :
                        self.d["ts%d%d" %(row,col)].set("X")
        #if solution is shown, hide solution
        else :
            for row in range(self.rows) :
                for col in range(self.cols) :
                    self.d["ts%d%d" %(row,col)].set("")

    def create_buttons(self) :
        #Check-Button
        checkm = tk.StringVar()
        checkm.set("")
        check = tk.Button(width=3,text="Check",bg="green",command=lambda:self.check(checkm)).grid(row=self.gridrows-1,column=0,columnspan=3)
        message = tk.Label(width=6,textvariable=checkm).grid(row=self.gridrows,column=0,columnspan=3)
        #Reset-Button
        tk.Button(width=3,text="Reset",bg="yellow",command=lambda:self.pop_up_reset()).grid(row=self.gridrows-1,column=3,columnspan=3)
        #Undo-Button
        tk.Button(state="normal",width=2,text="Undo",bg="lightblue",command=lambda:self.undo()).grid(row=self.gridrows-1,column=6,columnspan=3)
        #New-Button
        tk.Button(width=2,text="New",bg="magenta",command=lambda:self.pop_up_new()).grid(row=self.gridrows,column=3,columnspan=3)
        #Solution-Button
        tk.Button(width=3,text="Solution",bg="black",command=lambda:self.show_solution()).grid(row=self.gridrows, column=6,columnspan=3)

if __name__ == "__main__" :
    rows = 8
    cols = 8
    
    root = tk.Tk()
    root.title("Binoxxo")
    root.maxsize(width=200, height=300)
    app = Application(rows,cols,master=root)
    app.mainloop()