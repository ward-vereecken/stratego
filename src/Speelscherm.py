
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

KLEUR_SPELER = "#2757a5"
KLEUR_SPELER_DOOD = "#011438"

KLEUR_COMPUTER = "#c1131f"
KLEUR_COMPUTER_DOOD = "#560404"

KLEUR_GRAS = "#266d30"

class Spel(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        winsound.PlaySound('Achtergrondlied.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)
        self.teller = 0
        self.AI = AI()
        self.move_coord = []
        self.labels = {}
        self.pionnenaantspeler = {}
        self.pionnenaantcomp = {}
        self.setupl = {}
        self.spell = {}
        self.plaatsen = {}
        self.controller = controller
        self.b = Bord()
        self.aib = Bord()
        self.plaats_knoppen()
        self.aantalOntplofteBommen = 0
        self.aantalVeroverdePionnen = 0
        self.verander_combo("Bom")
        self.plaats_computer()
        self.maak_lijst(True)
        self.timer()

    def plaats_knoppen(self):
        global buttons, buttonsComp, background
        buttons = []
        buttonsComp = []

        # Images:
        picr = PhotoImage(file="pics\\achter9.png")
        pic = PhotoImage(file="pics\\achterSetup.png")
        pic2 = PhotoImage(file="pics\\startspel.png")
        pic3 = PhotoImage(file="pics\\willekeurig.png")
        pic4 = PhotoImage(file="pics\\terug2.png")
        pic5 = PhotoImage(file="pics\\regelssetup.png")
        self.lab = Label(self, image=picr)
        self.lab.image = picr
        self.lab.place(x=-140, y=600)
        self.lab = Label(self, image=pic)
        self.lab.image = pic
        self.lab.place(x=-100, y=0)
        background = self.lab

        # Informatiebalk:
        self.e = Entry(self, font="Times 15 italic", width=40)
        self.e.place(x=600, y=220)

        self.pi = Pion(0, 0, 0)
        self.maak_bord()

        # Combobox:
        self.combo = ttk.Combobox(self, values=["Bom", "Spion (1)", "Verkenner (2)", "Mineur (3)",
                                                "Sergeant (4)", "Luitenant (5)", "Kapitein (6)", "Majoor (7)",
                                                "Kolonel (8)", "Generaal (9)", "Maarschalk (10)", "Vlag"])
        self.combo.set("Bom")

        # Radiobuttons:
        self.var = IntVar()
        picver = PhotoImage(file="pics\\verwijderen.png")
        pictoev = PhotoImage(file="pics\\toevoegen2.png")
        self.rad1 = Radiobutton(self, bg="gray", image=pictoev, indicatoron=0, text="Toevoegen", cursor="plus",
                                variable=self.var, value=0)
        self.rad1.image = pictoev
        self.rad1.place(x=575, y=145)
        buttons.append(self.rad1)
        self.rad2 = Radiobutton(self, bg="gray", image=picver, indicatoron=0, text="Verwijderen", cursor="pirate",
                                variable=self.var,
                                value=1)
        self.rad2.image = picver
        self.rad2.place(x=815, y=145)
        self.rad3 = Radiobutton(self, variable=self.var, value=2)
        self.rad4 = Radiobutton(self, variable=self.var, value=3)
        self.rad5 = Radiobutton(self, variable=self.var,value=4)
        buttons.append(self.rad2)

        # Knoppen regels, terug, start en willekeurig plaatsen:
        self.regels = Button(self, image=pic5,
                             command=lambda: self.controller.show_frame("Handleiding"))
        self.regels.iamge = pic5
        self.regels.config(bg="gray")
        self.regels.place(x=488, y=640)

        self.terug = Button(self, text="Terug", image=pic4, cursor="left_side",
                            command=lambda: self.controller.show_frame("Startpagina"))
        self.terug.image = pic4
        self.terug.config(bg="gray")
        self.terug.place(x=275, y=705)

        self.start = Button(self, text="Start Spel", image=pic2, cursor="X_cursor", command=lambda: self.start_spel())
        self.start.image = pic2
        self.start.config(bg="gray")
        self.start.place(x=50, y=705)
        buttons.append(self.start)

        self.will = Button(self, image=pic3, text="De rest willekeurig plaatsen", cursor="question_arrow",
                           command=lambda: self.rest_zetten())
        self.will.image = pic3
        self.will.config(bg="gray")
        self.will.place(x=50, y=640)
        buttons.append(self.will)

        # Timer-label:
        wit = PhotoImage(file="pics\\wit.png")
        self.achter = Label(self, image=wit, width=34, height=28)
        self.achter.image = wit
        self.timerl = Button(self, bg="#c1131f", fg="white")
        self.tijd = 0
        self.seconden = 0
        self.minuten = 0

        # Statistiek-labels:
        self.aantalVeroverdePionnen = 0
        self.aantalVeroverdePionnenLabel = Label(text=self.aantalVeroverdePionnen)

    def maak_bord(self):
        x, y = 0, 0
        w = 50
        canvas = Canvas(self, width=500, height=500)
        canvas.place(x=0, y=0)
        for rij in range(11):
            for kol in range(11):
                if (rij, kol) in self.b.water:
                    water = PhotoImage(file="pics\\water.png")
                    but = Button(canvas, width=55, image=water, bg="#27426d", height=55, borderwidth=5,
                                 command=lambda row=rij * 50, col=kol * 50: self.klik(row, col))
                    but.image = water

                else:
                    gras = PhotoImage(file="pics\\gras.png")
                    but = Button(canvas, bg=KLEUR_GRAS, image=gras, activebackground="blue", width=55, height=55,
                                 borderwidth=5,
                                 command=lambda row=rij * 50, col=kol * 50: self.klik(row, col))
                    but.image = gras
                    self.plaatsen[kol, rij] = but
                    but.bind("<Enter>", lambda event, row=rij, col=kol: self.on_enter(col, row, event))
                    but.bind("<Leave>", lambda event, row=rij, col=kol: self.on_leave(col, row, event))
                but.place(x=x, y=y)
                x = x + w
            y = y + w
            x = 0

    def maak_lijst(self, kant):
        # Spelerlijst:
        if kant:
            lijst = self.b.aantalSpeler
            self.xl = 590
            self.yl = 300
            y = self.yl
            kleur = KLEUR_SPELER
        # Computerlijst:
        else:
            lijst = self.b.aantalComp
            self.xl = 590
            self.yl = 30
            y = self.yl
            kleur = KLEUR_COMPUTER
        teller = 0
        i = 0
        for x in lijst:
            over = Button(self, fg="white", highlightbackground="gray", width=5, bg=kleur, text=str(lijst.get(x)))

            if kant is True:
                self.pionnenaantspeler[i] = over
            else:
                buttonsComp.append(over)
                self.pionnenaantcomp[i] = over
            over.place(x=self.xl + 8, y=self.yl + 49)
            i += 1
            teller += 1
            if kant:
                self.maak_label(x, self.xl / 50, self.yl / 50, "Setup")
            else:
                self.maak_label(x, self.xl / 50, self.yl / 50, "Computer_lijst")
            self.yl += 90
            if teller == 3:
                teller = 0
                self.xl += 120
                self.yl = y

    def update_lijst(self, naam, bool, kant):
        if kant:
            over = self.pionnenaantspeler[self.pi.lijst.index(naam)]
            lijst = self.b.aantalSpeler
            kleur = KLEUR_SPELER
            kleurdood = KLEUR_SPELER_DOOD
        else:
            over = self.pionnenaantcomp[self.pi.lijst.index(naam)]
            lijst = self.b.aantalComp
            kleur = KLEUR_COMPUTER
            kleurdood = KLEUR_COMPUTER_DOOD

        # Pion toegevoegd:
        if bool is True:
            if lijst[naam] != 0:
                lijst[naam] -= 1
                aantal = str(lijst[naam])
                over.config(text=aantal, bg=kleur)
        # Pion dood
        else:
            lijst[naam] += 1
            aantal = str(lijst[naam])
            if self.var.get() == 0 or self.var.get() == 1:
                over.config(text=aantal, bg=kleur)
            else:
                if lijst[naam] != self.aib.aantalSpeler[naam]:
                    over.config(text=aantal, bg=kleurdood)
                else:
                    over.config(text="DOOD", bg="black")

    def on_enter(self, x, y, event):
        but = self.plaatsen[x, y]
        but.config(bg="orange")

    def on_leave(self, x, y, event):
        but = self.plaatsen[x, y]
        but.config(bg=KLEUR_GRAS)

    def plaats_computer(self):
        ai = AI()
        dic = ai.plaatsen()
        for naam in dic:
            if naam != "Strategie AI":
                for i in range(int(len(dic[naam]) / 2)):
                    coord = dic[naam][i * 2], dic[naam][i * 2 + 1]
                    self.voeg_toe_computer(int(coord[0] * 50), int(coord[1] * 50), naam, "Computer")

    def maak_label(self, naam, xpos, ypos, kant):
        index = self.pi.lijst.index(naam)
        if kant == "Speler":
            pic = PhotoImage(file="pics\\" + naam + ".png").subsample(3, 3)
            label = Button(self, image=pic)
            label.image = pic
            label.config(bg=KLEUR_SPELER, width=30, height=40, borderwidth=3,
                         command=lambda: self.klik(ypos * 50, xpos * 50))
            # "#5a89ad"
        elif kant == "Computer":
            pic = PhotoImage(file="pics\\Rood achterkant.png").subsample(5, 6)
            #pic = PhotoImage(file="pics\\"+naam+".png").subsample(3, 3)
            label = Button(self, image=pic)
            label.image = pic
            label.config(bg=KLEUR_COMPUTER,cursor = "cross", width=30, height=40, borderwidth=3,
                         command=lambda: self.klik(ypos * 50, xpos * 50))
        elif kant == "Computer_lijst":
            # pic = PhotoImage(file="pics\\Rood achterkant.png").subsample(5, 6)
            pic = PhotoImage(file="pics\\" + naam + ".png").subsample(3, 3)
            label = Button(self, image=pic)
            label.image = pic
            label.config(bg=KLEUR_COMPUTER, width=40, height=40, command=lambda: self.klik(ypos * 50, xpos * 50))
            buttonsComp.append(label)
        else:
            pic = PhotoImage(file="pics\\" + naam + ".png").subsample(3, 3)
            label = Button(self, image=pic)
            label.image = pic
            label.config(bg=KLEUR_SPELER, width=40, height=40, cursor="hand1", command=lambda: self.verander_combo(naam))
            self.setupl[index] = label
        label.place(x=(xpos * 50) + 8, y=(ypos * 50) + 4)
        self.labels[xpos * 50, ypos * 50] = label

    def klik(self, rij, kol):
        naam = self.combo.get()
        # 'Toevoegen' aangeklikt:
        if self.var.get() == 0:
            self.voeg_toe(rij, kol, naam, "Speler")
        # 'Verwijderen' aangeklikt:
        elif self.var.get() == 1:
            self.verwijder(rij, kol)
        # Beurt speler, wachten op klik pion:
        elif self.var.get() == 2:
            self.vraag_move(kol, rij)
        # Wachten op coördinaten voor move:
        elif self.var.get() == 3:
            x = self.move_coord[0]
            y = self.move_coord[1]
            self.beurt(x, y, int(kol / 50), int(rij / 50))
            self.move_coord = []
        elif self.var.get() == 4:
            self.verander_info("De tegenstander is aan de beurt.")

    def vraag_move(self, x, y):
        xpos = int(x / 50)
        ypos = int(y / 50)
        if self.b.opgevuld[xpos][ypos]:
            if self.b.board[xpos][ypos].kleur == "Speler":
                label = self.labels[x, y]
                label.config(bg="orange")
                self.verander_info("Waar wil je deze pion plaatsen?")
                self.move_coord.append(xpos)
                self.move_coord.append(ypos)
                self.rad4.select()
            else:
                self.verander_info("Dit is niet één van jouw pionnen.")
                self.rad3.select()
        else:
            self.verander_info("Hier staat geen pion.")
            self.rad3.select()

    def voeg_toe_computer(self, x, y, name, kant):
        xpos = int(y / 50)
        ypos = int(x / 50)
        if 0 <= xpos <= 9 and 0 <= ypos <= 3 and (ypos, xpos) not in self.b.water:
            naam = name
            if " " in naam:
                self.subnaam = naam.split(" ")[0]
                self.waarde = naam.split(" ")[1][1]
            else:
                self.subnaam = naam
                teller = 0
                for n in self.pi.lijst:
                    if naam == n:
                        self.waarde = teller
                    teller += 1

            if self.b.opgevuld[xpos][ypos] is False and self.b.aantalComp[self.subnaam] > 0:
                self.b.aantalComp[self.subnaam] -= 1
                self.maak_label(self.subnaam, xpos, ypos, kant)
                pion = Pion(self.waarde, xpos, ypos)
                self.b.voeg_pion_toe_spel(pion, xpos, ypos,"Computer")

    def voeg_toe(self, x, y, name, kant):
        try:
            xpos = int(y / 50)
            ypos = int(x / 50)
            if 0 <= xpos <= 9 and 6 <= ypos <= 9 and (ypos, xpos) not in self.b.water:
                naam = name
                if " " in naam:
                    self.subnaam = naam.split(" ")[0]
                    index1 = naam.index("(")
                    index2 = naam.index(")")
                    kracht = naam[index1 + 1:index2]
                    self.waarde = int(kracht)
                else:
                    self.subnaam = naam
                    teller = 0
                    for n in self.pi.lijst:
                        if naam == n:
                            self.waarde = teller
                        teller += 1

                if self.b.opgevuld[xpos][ypos] is False and self.b.aantalSpeler[self.subnaam] > 0:
                    self.maak_label(self.subnaam, xpos, ypos, kant)
                    pion = Pion(self.waarde, xpos, ypos)
                    self.b.voeg_pion_toe_spel(pion, xpos, ypos,"Speler")
                    self.verander_info(
                        "Je plaatst de pion " + self.subnaam + " op plaats (" + str(xpos + 1) + "," + str(
                            ypos + 1) + ").")
                    if kant is "Speler":
                        self.update_lijst(self.subnaam, True, True)
                else:
                    if self.b.aantalSpeler[self.subnaam] == 0:
                        self.verander_info("Geen " + self.subnaam + " meer op overschot!")
                    else:

                        self.verander_info("Hier staat al een pion!")
            else:
                self.verander_info("Hier mag geen pion staan!")
        except ValueError:
            self.verander_info("Deze coördinaten bestaan niet!")

    def verwijder(self, x, y):
        try:
            xpos = int(y / 50)
            ypos = int(x / 50)
            if self.b.opgevuld[xpos][ypos] is True and ypos >= 6:
                l = self.labels[xpos * 50, ypos * 50]
                l.destroy()
                self.update_lijst(self.b.board[xpos][ypos].naam, False, True)
                self.b.verwijder_pion(xpos, ypos)
                self.verander_info("Je verwijdert een pion")
            elif ypos < 4:
                self.verander_info("Nice try!")
            else:
                self.verander_info("Hier staat nog geen pion.")
        except ValueError:
            self.verander_info("Deze coördinaten bestaan niet!")

    def verwijder_computer(self, x, y):
        try:
            xpos = x
            ypos = y
            if self.b.opgevuld[xpos][ypos] is True and self.b.board[xpos][ypos].kleur == "Computer":
                l = self.labels[xpos * 50, ypos * 50]
                l.destroy()
                self.update_lijst(self.b.board[xpos][ypos].naam, False, False)
                self.b.verwijder_pion(xpos, ypos)
        except ValueError:
            self.verander_info("Deze coördinaten bestaan niet!")

    def verwijder_speler(self, x, y):
        try:
            xpos = x
            ypos = y
            if self.AI.opgevuld_aimove(x, y):
                self.AI.verwijder_pion_aimove(x, y)
            if self.AI.opgevuld_ais(x, y):
                self.AI.verwijder_pion_aib(x, y)
            if self.b.opgevuld[xpos][ypos] is True and self.b.board[xpos][ypos].kleur == "Speler":
                naam = self.b.board[xpos][ypos].naam
                l = self.labels[xpos * 50, ypos * 50]
                l.destroy()
                self.update_lijst(self.b.board[xpos][ypos].naam, False, True)
                self.b.verwijder_pion(xpos, ypos)
                self.verander_info("Jouw " + naam + " werd verslagen!")
            elif self.b.opgevuld[xpos][ypos] is True and self.b.board[xpos][ypos].kleur == "Computer":
                self.verander_info("Nice try!")
            else:
                self.verander_info("Hier staat nog geen pion.")
        except ValueError:
            self.verander_info("Deze coördinaten bestaan niet!")

    def verander_info(self, tekst):
        self.e.delete(0, END)
        self.e.insert(0, tekst, )

    def verander_combo(self, naam):
        index = self.pi.lijst.index(naam)
        self.combo.current(index)
        for key in self.setupl:
            if self.b.aantalSpeler[self.pi.lijst[key]] != 0:
                self.setupl[key].config(bg="#2757a5")
                if self.var.get() == 0 or self.var.get() == 1:
                    self.setupl[index].config(bg="#c1131f")
            else:
                if self.var.get() == 0 or self.var.get() == 1:
                    self.setupl[key].config(bg="gray")
                else:
                    self.setupl[key].config(bg="#2757a5")

    def start_spel(self):
        if self.b.aantalPionnen == 80:
            self.rad3.select()
            self.verander_combo("Bom")
            self.tijd = 0
            self.tijd = 0
            self.seconden = 0
            self.minuten = 0
            self.timerl.place(x=362, y=670)
            self.achter.place(x=359, y=667)
            self.terug.place(x=50, y=640)
            self.regels.place(x=264, y=640)
            self.maak_lijst(False)
            self.e.place(x=50, y=550)
            self.verander_info("Jij begint!")
            pic5 = PhotoImage(file="pics\\achterSpel.png")
            lab = Label(self, image=pic5)
            lab.image = pic5
            lab.place(x=-100, y=0)
            lab.lower(belowThis=None)
            for x in buttons:
                x.lower(belowThis=None)
            background.lower(belowThis=None)
            pic2 = PhotoImage(file="pics\\nieuw_spel.png")
            self.start = Button(self, text="Start Spel", image=pic2, cursor="X_cursor",
                                command=lambda: self.nieuw_spel())
            self.start.image = pic2
            self.start.config(bg="gray")
            self.start.place(x=50, y=705)
        else:
            self.verander_info("Je hebt nog niet alle pionnnen gezet!")

    def rest_zetten(self):
        for naam in self.b.aantalSpeler.keys():
            while self.b.aantalSpeler[naam] > 0:
                kol = random.randint(0, 9)
                rij = random.randint(6, 9)
                while self.b.opgevuld[kol][rij] is True:
                    kol = random.randint(0, 9)
                    rij = random.randint(6, 9)
                self.voeg_toe(rij * 50, kol * 50, naam, "Speler")
        self.verander_info("Alle pionnen gezet. Het spel kan beginnen!")

    def nieuw_spel(self):
        self.aantalVeroverdePionnenLabel.place(x=0, y=-100)
        self.rad1.select()
        self.regels.place(x=488, y=640)
        self.terug.place(x=275, y=705)
        self.timerl.place(x=-200, y=-200)
        self.achter.place(x=-200, y=-200)
        self.e.place(x=600, y=220)
        self.lab.place(x=-100, y=0)
        for x in buttons:
            x.lift(aboveThis=None)
        for x in buttonsComp:
            x.place(x=-100, y=-100)
        for rij in range(10):
            for kol in range(10):
                self.verwijder_speler(rij, kol)
                self.verwijder_computer(rij, kol)
                self.AI.verwijder_pion_aimove(rij,kol)
        self.plaats_computer()
        self.verander_info("Kies je strategie")

    def is_legal_move(self, x, y):
        self.lijst = {}
        if self.b.opgevuld[x][y] is False or self.b.board[x][y].aantal_stappen == 0:
            self.lijst[x + 1, y] = False
            self.lijst[x - 1, y] = False
            self.lijst[x, y + 1] = False
            self.lijst[x, y - 1] = False

        elif self.b.opgevuld[x][y] and self.b.board[x][y].aantal_stappen == 1:
            if 0 <= x + 1 <= 9 and (
                    (self.b.opgevuld[x + 1][y] and self.b.board[x + 1][y].kleur != self.b.board[x][y].kleur) or (
                    self.b.opgevuld[x + 1][y] is False) and (y, x + 1) not in self.b.water):
                self.lijst[x + 1, y] = True
            else:
                self.lijst[x + 1, y] = False
            if 0 <= x - 1 <= 9 and (
                    (self.b.opgevuld[x - 1][y] and self.b.board[x - 1][y].kleur != self.b.board[x][y].kleur) or (
                    self.b.opgevuld[x - 1][y] is False) and (y, x - 1) not in self.b.water):
                self.lijst[x - 1, y] = True
            else:
                self.lijst[x - 1, y] = False
            if 0 <= y + 1 <= 9 and (
                    (self.b.opgevuld[x][y + 1] and self.b.board[x][y + 1].kleur != self.b.board[x][y].kleur) or (
                    self.b.opgevuld[x][y + 1] is False) and (y + 1, x) not in self.b.water):
                self.lijst[x, y + 1] = True
            else:
                self.lijst[x, y + 1] = False
            if 0 <= y - 1 <= 9 and (
                    (self.b.opgevuld[x][y - 1] and self.b.board[x][y - 1].kleur != self.b.board[x][y].kleur) or (
                    self.b.opgevuld[x][y - 1] is False) and (y - 1, x) not in self.b.water):
                self.lijst[x, y - 1] = True
            else:
                self.lijst[x, y - 1] = False
        elif self.b.opgevuld[x][y] and self.b.board[x][y].aantal_stappen == 10:
            teller1 = 1
            bool1 = True
            while bool1 is True and (y, x + teller1) not in self.b.water:
                if 0 <= x + teller1 <= 9 and self.b.opgevuld[x + teller1][y] is False:
                    self.lijst[x + teller1, y] = True
                elif 0 <= x + teller1 <= 9 and self.b.opgevuld[x + teller1][y] is True and self.b.board[x + teller1][
                    y].kleur != self.b.board[x][y].kleur:
                    self.lijst[x + teller1, y] = True
                    bool1 = False
                else:
                    self.lijst[x + teller1, y] = False
                    bool1 = False
                teller1 += 1

            teller2 = 1
            bool2 = True
            while bool2 is True and (y, x - teller2) not in self.b.water:
                if 0 <= x - teller2 <= 9 and self.b.opgevuld[x - teller2][y] is False:
                    self.lijst[x - teller2, y] = True
                elif 0 <= x - teller2 <= 9 and self.b.opgevuld[x - teller2][y] is True and self.b.board[x - teller2][
                    y].kleur != self.b.board[x][y].kleur:
                    self.lijst[x - teller2, y] = True
                    bool2 = False
                else:
                    self.lijst[x - teller2, y] = False
                    bool2 = False
                teller2 += 1

            teller3 = 1
            bool3 = True
            while bool3 is True and (y + teller3, x) not in self.b.water:
                if 0 <= y + teller3 <= 9 and self.b.opgevuld[x][y + teller3] is False:
                    self.lijst[x, y + teller3] = True
                elif 0 <= y + teller3 <= 9 and self.b.opgevuld[x][y + teller3] is True and self.b.board[x][
                    y + teller3].kleur != self.b.board[x][y].kleur:
                    self.lijst[x, y + teller3] = True
                    bool3 = False
                else:
                    self.lijst[x, y + teller3] = False
                    bool3 = False
                teller3 += 1

            teller4 = 1
            bool4 = True
            while bool4 == True and (y - teller4, x) not in self.b.water:
                if 0 <= y - teller4 <= 9 and self.b.opgevuld[x][y - teller4] is False:
                    self.lijst[x, y - teller4] = True
                elif 0 <= y - teller4 <= 9 and self.b.opgevuld[x][y - teller4] is True and self.b.board[x][
                    y - teller4].kleur != self.b.board[x][y].kleur:
                    self.lijst[x, y - teller4] = True
                    bool4 = False
                else:
                    self.lijst[x, y - teller4] = False
                    bool4 = False
                teller4 += 1
        return self.lijst

    def vergelijk(self, dix, x, y):
        b = False
        for coord in dix.keys():
            if (x, y) == coord and dix[x, y] is True:
                b = True
        return b

    def beurt(self, x1, y1, x2, y2):
        label = self.labels[x1 * 50, y1 * 50]
        try:
            if self.b.opgevuld[x1][y1]:
                dix = self.is_legal_move(x1, y1)
                b = self.vergelijk(dix, x2, y2)
                if b is True and self.b.opgevuld[x2][y2]:
                    self.val_aan(x1, y1, x2, y2)
                    self.rad5.select()
                    self.after(1000, lambda: self.zet_AI())
                elif b is True:
                    self.move(x1, y1, x2, y2)
                    self.rad5.select()
                    self.after(1000, lambda: self.zet_AI())
                else:
                    label.config(bg="#5a89ad")
                    self.verander_info("Ongeldige zet")
                    self.rad3.select()
            else:
                label.config(bg="#5a89ad")
                self.verander_info("Ongeldige zet")
                self.rad3.select()
        except IndexError:
            label.config(bg="#5a89ad")
            self.verander_info("Iets ging mis.")
            self.rad3.select()

    def aantal(self):
        getal = self.AI.aantal()
        return getal

    def move(self, x1, y1, x2, y2):
        if self.b.board[x1][y1].kleur == "Computer":
            naam = self.b.board[x1][y1].naam
            kleur = self.b.board[x1][y1].kleur
            self.verwijder_computer(x1, y1)
            self.voeg_toe_computer_spel(x2, y2, naam, kleur)
        else:
            naam = self.b.board[x1][y1].naam
            if self.AI.opgevuld_ais(x1, y1):
                self.AI.update_pion_aib(x1, y1, x2, y2, naam)
            kleur = self.b.board[x1][y1].kleur
            self.AI.update_pion_aimove(x1, y1, x2, y2, naam)
            self.verwijder_speler(x1, y1)
            self.voeg_toe_spel(x2, y2, naam, kleur)

    def eind(self, gewonnen):
        self.eindLabels = []
        doden = 0
        for naam in self.b.aantalSpeler.keys():
            doden += self.b.aantalSpeler[naam]
        self.nieuw_spel()
        if gewonnen:
            afb = PhotoImage(file="pics\\Victory_achter_final.png").zoom(9, 9).subsample(9, 9)
        else:
            afb = PhotoImage(file="pics\\Defeat_achter_final.png").zoom(9, 9).subsample(9, 9)
        self.vpLabel = Label(text=self.aantalVeroverdePionnen, font=("Times", 18), bg="#FADF86", fg= "black")
        self.bLabel = Label(text=self.aantalOntplofteBommen, font=("Times", 18), bg="#FADF86", fg="black")
        self.dLabel = Label(text=doden, font=("Times", 18), bg="#FADF86", fg="black")
        self.vpLabel.place(x=612, y=419)
        self.bLabel.place(x=612, y=333)
        self.dLabel.place(x=612, y=485)
        self.achtergr = Label(self, image=afb)
        self.achtergr.image = afb
        self.achtergr.place(x=0, y=0)
        self.timer_bijhouden()
        self.eindLabels.append(self.vpLabel)
        self.eindLabels.append(self.bLabel)
        self.eindLabels.append(self.dLabel)
        self.eindLabels.append(self.achtergr)
        pic = PhotoImage(file="pics\\start.png")
        pic3 = PhotoImage(file="pics\\regels.png")
        pic2 = PhotoImage(file="pics\\verlaten.png")

        button1 = Button(self, image=pic, command=lambda: self.na_eind())
        button2 = Button(self, image=pic2, command=self.quit)
        button1.image = pic
        button1.config(bg="grey")
        button1.place(x=422, y=720, anchor="center")
        button2.image = pic2
        button2.config(bg="gray")
        button2.place(x=632, y=720, anchor="center")
        self.eindLabels.append(button1)
        self.eindLabels.append(button2)

    def na_eind(self):
        self.nieuw_spel()
        self.nu.destroy()
        for label in self.eindLabels:
            label.destroy()

    def val_aan(self, x1, y1, x2, y2):
        waarde1 = self.b.board[x1][y1].waarde
        waarde2 = self.b.board[x2][y2].waarde
        if waarde1 == 11 or waarde2 == 11:
            gewonnen = False
            if waarde1 == 11:
                if self.b.board[x1][y1].kleur == "Computer":
                    print("test1")
                    winsound.PlaySound("victory", winsound.SND_FILENAME)
                    self.verander_info("Je hebt de vijandelijke vlag gevonden!!")
                    gewonnen = True
                else:
                    print("test2")
                    winsound.PlaySound("loser", winsound.SND_FILENAME)
                    self.verander_info("De tegenstander heeft jouw vlag gevonden...")
                    gewonnen = False
            else:
                if self.b.board[x1][y1].kleur == "Speler":
                    print("test3")
                    winsound.PlaySound("victory", winsound.SND_FILENAME)
                    self.verander_info("Je hebt de vijandelijke vlag gevonden!!")
                    gewonnen = True
                else:
                    print("test4")
                    winsound.PlaySound("loser", winsound.SND_FILENAME)
                    self.verander_info("De tegenstander heeft jouw vlag gevonden...")
                    gewonnen = False
            for x in range(10):
                for y in range(10):
                    print(x, ",", )
                    if self.b.opgevuld[x][y] is True and self.b.board[x][y].kleur == "Computer":
                        naam = self.b.board[x][y].naam
                        print(naam)
                        afb = PhotoImage(file="pics\\"+naam+".png").subsample(3, 3)
                        self.labels[x*50, y*50].config(image = afb)
                        self.labels[x*50, y*50].image = afb
            self.after(3000, lambda: self.eind(gewonnen))
        elif waarde1 == 0 and waarde2 != 3:
            if self.b.board[x2][y2].kleur == "Computer":
                name = self.b.board[x2][y2].naam
                self.verwijder_computer(x2, y2)
                naam = self.b.board[x1][y1].naam
                self.AI.update_pion_aib(x1, y1, x2, y2, naam)
                self.move(x1, y1, x2, y2)
                self.verander_info("Je versloeg de pion " + name + "!")
            else:
                self.teller = 0
                name = self.b.board[x1][y1].naam
                self.toon_pion(name, x1, y1)
                self.teller = 0
                self.verwijder_speler(x2, y2)
                self.move(x1, y1, x2, y2)
        elif waarde1 != 3 and waarde2 == 0:
            if self.b.board[x1][y1].kleur == "Computer":
                name = self.b.board[x1][y1].naam
                self.verwijder_computer(x1, y1)
                self.AI.voeg_pion_aan_aib(x2, y2, self.b.board[x2][y2].naam)
                self.verander_info("Je versloeg de pion " + name + "!")
                self.aantalOntplofteBommen = self.aantalOntplofteBommen + 1
            else:
                self.teller = 0
                name = self.b.board[x2][y2].naam
                self.toon_pion(name, x2, y2)
                self.teller = 0
                self.verwijder_speler(x1, y1)
                self.aantalOntplofteBommen = self.aantalOntplofteBommen + 1
        elif waarde1 == 1 and waarde2 == 10:
            if self.b.board[x2][y2].kleur == "Computer":
                name = self.b.board[x2][y2].naam
                self.verwijder_computer(x2, y2)
                naam = self.b.board[x1][y1].naam
                self.AI.update_pion_aib(x1, y1, x2, y2, naam)
                self.move(x1, y1, x2, y2)
                self.verander_info("Je versloeg de pion " + name + "!")
                self.aantalVeroverdePionnen = self.aantalVeroverdePionnen + 1
            else:
                self.teller = 0
                name = self.b.board[x1][y1].naam
                self.toon_pion(name, x1, y1)
                self.teller = 0
                self.verwijder_speler(x2, y2)
                self.move(x1, y1, x2, y2)
        elif waarde1 == 10 and waarde2 == 1:
            if self.b.board[x2][y2].kleur == "Computer":
                name = self.b.board[x2][y2].naam
                self.verwijder_computer(x2, y2)
                naam = self.b.board[x1][y1].naam
                self.AI.update_pion_aib(x1, y1, x2, y2, naam)
                self.move(x1, y1, x2, y2)
                self.verander_info("Je versloeg de pion " + name + "!")
                self.aantalVeroverdePionnen = self.aantalVeroverdePionnen + 1
            else:
                self.teller = 0
                name = self.b.board[x1][y1].naam
                self.toon_pion(name, x1, y1)
                self.teller = 0
                self.verwijder_speler(x2, y2)
                self.move(x1, y1, x2, y2)
        elif waarde1 == waarde2:
            if self.b.board[x1][y1].kleur == "Computer":
                name = self.b.board[x1][y1].naam
                self.verwijder_computer(x1, y1)
                self.verander_info("Je versloeg de pion " + name + "!")
                self.aantalVeroverdePionnen = self.aantalVeroverdePionnen + 1
            elif self.b.board[x1][y1].kleur == "Speler":
                self.teller = 0
                name = self.b.board[x2][y2].naam
                self.toon_pion(name, x2, y2)
                self.teller = 0
                self.AI.verwijder_pion_aib(x1, y1)
                self.verwijder_speler(x1, y1)
            if self.b.board[x2][y2].kleur == "Computer":
                name = self.b.board[x2][y2].naam
                self.verwijder_computer(x2, y2)
                self.verander_info("Je versloeg de pion " + name + "!")
                self.aantalVeroverdePionnen = self.aantalVeroverdePionnen + 1
            elif self.b.board[x2][y2].kleur == "Speler":
                #self.teller = 0
                #name = self.b.board[x1][y1].naam
                #self.toon_pion(name, x1, y1)
                #self.teller = 0
                self.AI.verwijder_pion_aib(x2, y2)
                self.verwijder_speler(x2, y2)
        elif waarde1 > waarde2:
            if self.b.board[x2][y2].kleur == "Computer":
                name = self.b.board[x2][y2].naam
                self.verwijder_computer(x2, y2)
                naam = self.b.board[x1][y1].naam
                self.AI.update_pion_aib(x1, y1, x2, y2, naam)
                self.move(x1, y1, x2, y2)
                self.verander_info("Je versloeg de pion "+name+"!")
                self.aantalVeroverdePionnen = self.aantalVeroverdePionnen + 1
            else:
                self.teller = 0
                name = self.b.board[x1][y1].naam
                self.toon_pion(name, x1, y1)
                self.teller = 0
                self.verwijder_speler(x2, y2)
                self.move(x1, y1, x2, y2)
        else:
            if self.b.board[x1][y1].kleur == "Computer":
                name = self.b.board[x1][y1].naam
                self.verwijder_computer(x1, y1)
                self.AI.voeg_pion_aan_aib(x2, y2, self.b.board[x2][y2].naam)
                if self.b.board[x2][y2].aantal_stappen != 0:
                    self.AI.voeg_pion_aan_aimove(x2,y2,self.b.board[x2][y2].naam)
                self.verander_info("Je versloeg de vijandelijke " + name + "!")
                self.aantalVeroverdePionnen += 1
            else:
                self.teller = 0
                name = self.b.board[x2][y2].naam
                self.toon_pion(name, x2, y2)
                self.teller = 0
                self.AI.verwijder_pion_aib(x1, y1)
                self.verwijder_speler(x1, y1)

    def timer_bijhouden(self):
        seconden_nu = self.seconden
        minuten_nu = self.minuten
        self.nu = Label(bg="#FADF86",font=("Times", 18),fg="black",text=(str(minuten_nu)+":"+str(seconden_nu)))
        self.nu.place(x=585, y=572)

    def timer(self):
        self.tijd += 1
        if self.tijd > 60:
            self.seconden = self.tijd % 60
            self.minuten = int(self.tijd / 60)
        else:
            self.seconden = self.tijd
        if self.seconden < 10:
            self.seconden = "0" + str(self.seconden)
        self.timerl.config(text=str(self.minuten) + ":" + str(self.seconden))
        self.after(1000, lambda: self.timer())

    def toon_pion(self, naam, x, y):
        try:
            if self.teller % 2 == 0:
                pic = PhotoImage(file="pics\\" + naam + ".png").subsample(3, 3)
            else:
                pic = PhotoImage(file="pics\\Rood achterkant.png").subsample(5, 6)
            lab = self.labels[x * 50, y * 50]
            lab.config(image=pic)
            lab.image = pic
            if self.teller < 1:
                self.teller += 1
                self.after(1000, lambda: self.toon_pion(naam, x, y))
        except:
            pass

    def voeg_toe_computer_spel(self, x, y, name, kant):
        xpos = x
        ypos = y
        if 0 <= xpos <= 9 and 0 <= ypos <= 9 and (ypos, xpos) not in self.b.water:

            naam = name
            if " " in naam:
                self.subnaam = naam.split(" ")[0]
                self.waarde = naam.split(" ")[1][1]
            else:
                self.subnaam = naam
                teller = 0
                for n in self.pi.lijst:
                    if naam == n:
                        self.waarde = teller
                    teller += 1

            if self.b.opgevuld[xpos][ypos] is False:
                self.maak_label(self.subnaam, xpos, ypos, kant)
                pion = Pion(self.waarde, xpos, ypos)
                self.b.voeg_pion_toe_spel(pion, xpos, ypos, kant)
                self.update_lijst(self.b.board[xpos][ypos].naam, True, False)

    def voeg_toe_spel(self, x, y, name, kant):
        try:
            xpos = x
            ypos = y

            naam = name
            if " " in naam:
                self.subnaam = naam.split(" ")[0]
                self.waarde = naam.split(" ")[1][1]
            else:
                self.subnaam = naam
                teller = 0
                for n in self.pi.lijst:
                    if naam == n:
                        self.waarde = teller
                    teller += 1

            self.maak_label(self.subnaam, xpos, ypos, kant)
            pion = Pion(self.waarde, xpos, ypos)
            self.b.voeg_pion_toe_spel(pion, xpos, ypos, kant)
            self.verander_info(
                "Je plaatst de pion " + self.subnaam + " op plaats (" + str(xpos + 1) + "," + str(ypos + 1) + ").")
            if kant is "Speler":
                self.update_lijst(self.subnaam, True, True)

        except ValueError:
            self.verander_info("Deze coördinaten bestaan niet!")

    def get_bommen(self):
        return self.aantalOntplofteBommen

    def zet_AI(self):
        lijst_goede_pionnen = []
        bordAi = self.b.board
        #dix = self.is_legal_move(0, 0)
        for rij in bordAi:
            for pion in rij:
                if pion is not None:
                    if pion.getKleur() == "Computer":
                        x1 = pion.getX()
                        y1 = pion.getY()
                        dix = self.is_legal_move(x1, y1)
                        b = self.vergelijk(dix, x1, y1 + 1)     #vergelijkt enkel met plaats voor de pion
                        blinks = self.vergelijk(dix, x1-1, y1)  #vergelijkt enkel met de plaats links van de pion
                        brechts = self.vergelijk(dix, x1+1, y1) #vergelijkt enkel met de plaats rechts van de pion
                        if b or blinks or brechts:
                            lijst_goede_pionnen.append(pion)      #Opvullen van lijst met goede pionnen
        if len(lijst_goede_pionnen) == 0 :
            self.eind(True)
        wilpion = random.choice(lijst_goede_pionnen)
        xcoor = wilpion.getX()
        ycoor = wilpion.getY()
        dix = self.is_legal_move(xcoor, ycoor)
        lijst = []
        lijst_aanval = []
        for key in dix:
            value = dix[key]
            x = key[0]
            y = key[1]
            if value == True and self.b.opgevuld[x][y] and self.b.board[x][y].kleur == "Speler" and y >= ycoor:
                lijst_aanval.append(key)
            elif value == True and self.b.opgevuld[x][y] == False and y >= ycoor:
                lijst.append(key)

        if len(lijst_aanval) != 0:
            if len(lijst_aanval) == 1:
                aantal = 1
                x = lijst_aanval[aantal - 1]
                if self.AI.opgevuld_ais(x[0], x[1]) and self.b.board[xcoor][ycoor].waarde < self.b.board[x[0]][x[1]].waarde and len(lijst) > 0:
                    if len(lijst) == 1:
                        aantal = 1
                    else:
                        aantal = randint(1, len(lijst))
                    Y = lijst[aantal - 1]
                    self.move(xcoor, ycoor, Y[0], Y[1])
                else:
                    self.val_aan(xcoor, ycoor, x[0], x[1])

            else:
                aantal = randint(1, len(lijst_aanval))
                x = lijst_aanval[aantal-1]
                teller = 0
                if self.AI.opgevuld_ais(x[0], x[1]) and self.b.board[xcoor][ycoor].waarde == 3 and self.b.board[x[0]][x[1]].waarde == 0:
                    self.val_aan(xcoor, ycoor, x[0], x[1])
                elif self.AI.opgevuld_ais(x[0], x[1]) and self.b.board[xcoor][ycoor].waarde != 3 and self.b.board[x[0]][x[1]].waarde == 0:
                    aantal = randint(1, len(lijst_aanval))
                    x = lijst_aanval[aantal - 1]
                    self.val_aan(xcoor, ycoor, x[0], x[1])
                while self.AI.opgevuld_ais(x[0], x[1]) and self.b.board[xcoor][ycoor].waarde < self.b.board[x[0]][x[1]].waarde and teller < 5:
                    aantal = randint(1, len(lijst_aanval))
                    x = lijst_aanval[aantal - 1]
                    teller += 1
                if teller == 5 and len(lijst) > 0:
                    if len(lijst) == 1:
                        aantal = 1
                    else:
                        aantal = randint(1, len(lijst))
                    x = lijst[aantal - 1]
                    self.move(xcoor, ycoor, x[0], x[1])

                else:
                    self.val_aan(xcoor, ycoor, x[0], x[1])
        else:
            if len(lijst) == 1:
                aantal = 1
            else:
                aantal = randint(1, len(lijst))
            x = lijst[aantal-1]
            self.move(xcoor, ycoor,  x[0], x[1])
        self.rad3.select()

    def get_veroverde_pionnen(self):
        return self.aantalVeroverdePionnen

    def bevat_pion(self, x, y):
        if self.b.opgevuld[x][y] is None:
            return False
        else:
            return True

    def get_kleur_pion(self, x, y):
        if self.b.opgevuld[x][y] is not None:
            pion = self.b.board[x][y]
            kleur = pion.getKleur()
            return kleur
        else:
            return ""
