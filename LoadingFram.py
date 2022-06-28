from asyncio.windows_events import NULL
from cProfile import label
from cgitb import text
from tkinter import *

class LoadingFrame :

    fram=None
    #Initialize Welcome Frame Object Class
    def __init__(self,root):
        self.fram = Frame(root,height=100, width=500, bg="#3878AE", bd=10)
     

    def getFrame(self,root):
        self.fram.pack(anchor=N, fill=BOTH, expand=True, side=LEFT)

        self.Welcomlabel= Label(self.fram, text="Initilizing the database")
        self.Welcomlabel.pack()

    def OpenFram(self, root):
        pass