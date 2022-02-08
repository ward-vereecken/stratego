from tkinter import *
from tkinter import ttk, Radiobutton
from typing import List, Union
import Pion
from Spelbord import Bord
from Pion import Pion
from AI import AI
import random
import winsound
from random import randint
from Handleiding import Handleiding
from Startpagina import Startpagina
from Speelscherm import Spel


class SampleApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Startpagina, Spel, Handleiding):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Startpagina")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = SampleApp()
    app.title("Stratego")
    app.mainloop()
