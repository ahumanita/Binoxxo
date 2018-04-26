# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 09:59:43 2018

@author: ullrich
"""

import tkinter as tk
import binoxxo as bi

class Application(tk.Frame) :
    def __init__(self,master=None) :
        super().__init__(master)
        self.rows = 8
        self.columns = 8 + 1
        self.cellwidth = 10
        self.cellheight = 10
        self.binoxxo = 0
        self.create_binoxxo()
        self.create_buttons()
        
    def create_grid(self) :        
        d = {}
        for r in range(0,8) :
            for c in range(0,8) :
                d["e%d%d" %(r,c)] = tk.Entry(width=2).grid(row=r,column=c)
            
    def leftclick(self,event) :
        event.widget.config(text="X")
        print("left")
       
    def rightclick(self,event) :
        event.widget.config(text="O")
        print("right")

    def create_binoxxo(self) :
        d = {}
        it = 0
        valid = False
        while not valid and it < 100 :
            self.binoxxo = bi.Binoxxo(8,8)
            self.binoxxo.create()
            valid = self.binoxxo.is_valid()
            it += 1
            print(valid)
            print(it)        
        for r in range(0,8) :
            for c in range(0,8) :
                if (r,c) in self.binoxxo.entries.keys() :
                    d["e%d%d" %(r,c)] = tk.Label(width=3,height=1,text=str(self.binoxxo.entries[(r,c)])).grid(row=r,column=c)
                else :
                    d["d%d%d" %(r,c)] = tk.StringVar()
                    d["d%d%d" %(r,c)].set("test")
                    d["e%d%d" %(r,c)] = tk.Label(width=2,bg="white")
                    d["e%d%d" %(r,c)].grid(row=r,column=c)
                    d["e%d%d" %(r,c)].bind("<Button-1>",lambda event:self.leftclick(event))
                    d["e%d%d" %(r,c)].bind("<Button-3>",lambda event:self.rightclick(event))
                    
                    
    #TODO: nochmal testen, nachdem die Benutzereinträge gespeichert wurden
    def check(self,checkm) :
        if self.binoxxo.is_valid() == True :
            checkm.set("Correct!")
        else :  
            checkm.set("Wrong!")        

    def create_buttons(self) :
        checkm = tk.StringVar()
        checkm.set("")
        check = tk.Button(width=3,text="check",bg="green",command=lambda:self.check(checkm)).grid(row=0,column=7+1)
        message = tk.Label(width=6,textvariable=checkm).grid(row=1,column=7+1)

if __name__ == "__main__" :
    root = tk.Tk()
    root.title("Binoxxo")
    root.maxsize(width=200, height=300)
    app = Application(master=root)
    app.mainloop()