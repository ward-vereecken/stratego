from tkinter import *
import winsound


class Startpagina(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        controller.minsize(1100, 800)
        controller.maxsize(1100, 800)
        titelsch = PhotoImage(file="pics\\startscherm2.png").zoom(10, 10).subsample(9, 9)
        labels = Label(self, image=titelsch)
        labels.image = titelsch
        labels.place(x=0, y=0)

        pic = PhotoImage(file="pics\\start.png")
        pic2 = PhotoImage(file="pics\\regels.png")
        pic3 = PhotoImage(file="pics\\verlaten.png")

        button1 = Button(self, text="Nieuw spel", image=pic,
                         command=lambda: controller.show_frame("Spel"))
        button1.image = pic
        button1.config(bg="gray")
        # 8 en 23
        button2 = Button(self, image=pic2, text="Handleiding",
                         command=lambda: controller.show_frame("Handleiding"))
        button2.image = pic2
        button2.config(bg="gray")

        button3 = Button(self, image=pic3, command=self.quit, anchor='s')
        button3.image = pic3
        button3.config(bg="gray")

        button1.place(x=238, y=456, anchor="center")
        button2.place(x=238, y=516, anchor="center")
        button3.place(x=238, y=576, anchor="center")
