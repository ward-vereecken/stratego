from tkinter import *

class Handleiding(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        pic = PhotoImage(file="pics\\spelregels_achter.png")
        pic2 = PhotoImage(file="pics\\terug2.png").zoom(4, 4).subsample(5, 5)
        pic3 = PhotoImage(file="pics\\start.png")

        label = Label(self, image=pic)
        label.image = pic
        label.place(x=0, y=0)

        button = Button(self, text="Terug", bg="gray", image=pic2,
                        command=lambda: controller.show_frame("Startpagina"))
        button.image = pic2
        button2 = Button(self, text="Terug", bg="gray", image=pic3,
                         command=lambda: controller.show_frame("Spel"))
        button2.image = pic3
        button.place(x=910, y=75, anchor="center")
        button2.place(x=675, y=75, anchor="center")


