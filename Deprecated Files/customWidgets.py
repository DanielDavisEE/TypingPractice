'''
This file is not currently in use
'''

import tkinter as tk
import tkinter.ttk as ttk

class wordEntry(tk.Entry):
    def __init__(self, master, **kw):
        apply(tk.Entry.__init__, (self, master), kw)
        self.bind("<Return>", lambda e: "break")    
        