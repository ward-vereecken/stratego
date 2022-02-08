import random
from Pion import Pion
from Spelbord import Bord


class AI:
    def __init__(self):
        self.pi = Pion(0, 0, 0)
        self.aib = Bord()
        self.ais = Bord()
        self.aimove = Bord()
        self.dic = {}
        self.bin = random.randint(0, 1)
        if self.bin == 1:
            self.agressief = True
        else:
            self.agressief = False
    # Setup van AI:

    def coord_in_buurt(self, x, y, xoff, yoff):
        coord = []
        teller = 0
        xs = random.randint(x-xoff, x+xoff)
        ys = random.randint(y-yoff, y+yoff)
        try:
            while self.aib.opgevuld[xs][ys] is True or 10 <= xs or xs < 0 or 3 <= ys or ys < 0:
                xs = random.randint(x-xoff, x+xoff)
                ys = random.randint(y-yoff, y+xoff)
                teller += 1
                if teller == 7:

                    xoff += 1

                    yoff += 1
                    teller = 0
        except:
            print('EXCEPTION')
            coord = self.coord_in_buurt(x, y, xoff, yoff)
        print("\n")
        coord.append(xs)
        coord.append(ys)
        print(str(xs)+" "+str(ys))
        if 0 <= xs <= 9 and 0 <= ys <= 9:
            self.aib.opgevuld[xs][ys] = True
        return coord

    def vlag(self):
        vc = []
        kol = random.randint(0, 9)
        rij = 0
        vc.append(rij)
        vc.append(kol)
        self.aib.opgevuld[kol][rij] = True
        self.aib.aantalComp["Vlag"] -= 1
        return vc

    def bom(self):
        bc = []
        vc = self.dic["Vlag"]
        y = vc[0]
        x = vc[1]
        for i in range(3):
            coord = self.coord_in_buurt(x, y, 1, 1)
            bc.append(coord[1])
            bc.append((coord[0]))
            self.aib.aantalComp["Bom"] -= 1
            self.aib.opgevuld[coord[0]][coord[1]] = True
        for i in range(3):
            kol = random.randint(0, 9)
            rij = random.randint(0, 3)
            while self.aib.opgevuld[kol][rij] is True:
                kol = random.randint(0, 9)
                rij = random.randint(1, 3)
            bc.append(rij)
            bc.append(kol)
            self.aib.opgevuld[kol][rij] = True
            self.aib.aantalComp["Bom"] -= 1
        return bc

    def maarschalk(self, agg):
        mc = []
        if agg:
            x = random.randint(0, 9)
            y = 3
            while self.aib.opgevuld[x][y] is True:
                x = random.randint(0, 9)
            mc.append(y)
            mc.append(x)
            self.aib.opgevuld[x][y] = True
            self.aib.aantalComp["Maarschalk"] -= 1
        else:
            vc = self.dic["Vlag"]
            y = vc[0]
            x = vc[1]
            coord = self.coord_in_buurt(x, y, 1, 1)
            mc.append(coord[1])
            mc.append(coord[0])
            self.aib.aantalComp["Maarschalk"] -= 1
        return mc

    def mineurs(self, agg):
        mc = []
        for i in range(3):
            kol = random.randint(0, 9)
            rij = random.randint(0, 3)
            while self.aib.opgevuld[kol][rij] is True:
                kol = random.randint(0, 9)
                rij = random.randint(1, 3)
            mc.append(rij)
            mc.append(kol)
            self.aib.opgevuld[kol][rij] = True
            self.aib.aantalComp["Mineur"] -= 1
        for i in range(2):
            kol = random.randint(0, 9)
            rij = 0
            while self.aib.opgevuld[kol][rij] is True:
                kol = random.randint(0,9)
            mc.append(rij)
            mc.append(kol)
            self.aib.opgevuld[kol][rij] = True
            self.aib.aantalComp["Mineur"] -= 1
        return mc

    def plaatsen(self):

        vc = self.vlag()
        self.dic["Vlag"] = vc

        bc = self.bom()
        self.dic["Bom"] = bc

        mc = self.maarschalk(self.agressief)
        self.dic["Maarschalk"] = mc

        mic = self.mineurs(self.agressief)
        self.dic["Mineur"] = mic

        for naam in self.aib.aantalComp.keys():
            while self.aib.aantalComp[naam] > 0:
                res = []
                self.aib.aantalComp[naam] -= 1
                kol = random.randint(0, 9)
                rij = random.randint(0, 3)
                while self.aib.opgevuld[kol][rij] is True:
                    kol = random.randint(0, 9)
                    rij = random.randint(0, 3)
                res.append(rij)
                res.append(kol)
                if naam not in self.dic.keys():
                    self.dic[naam] = res
                else:
                    self.dic[naam] += res
                self.aib.opgevuld[kol][rij] = True

        if self.agressief:
            self.dic["Strategie AI"] = "Agressief"
        else:
            self.dic["Strategie AI"] = "Defensief"
        return self.dic

    # Vanaf hier spel AI:
    def update_pion_aib(self, x1, y1, x2, y2, naam):
        if self.ais.opgevuld[x1][y1]:
            if self.ais.opgevuld[x1][y1] and self.ais.board[x1][y1].kleur == "Speler":
                self.verwijder_pion_aib(x1, y1)
                self.voeg_pion_aan_aib(x2, y2, naam)

        else:
            self.voeg_pion_aan_aib(x2, y2, naam)

    def verwijder_pion_aib(self, x, y):
        if self.ais.opgevuld[x][y]:
            self.ais.opgevuld[x][y] = False
            self.ais.board[x][y] = None
            self.ais.aantalPionnen -= 1

    def voeg_pion_aan_aib(self, x, y, naam):
        xpos = x
        ypos = y
        teller = 0
        waarde = self.pi.lijst.index(naam)
        if self.ais.opgevuld[xpos][ypos] is False:
            pion = Pion(waarde, xpos, ypos)
            self.ais.voeg_pion_toe_spel(pion, xpos, ypos, "Speler")

    #AIMOVE
    def update_pion_aimove(self, x1, y1, x2, y2, naam):
        if self.aimove.opgevuld[x1][y1]:
            if self.aimove.opgevuld[x1][y1] and self.aimove.board[x1][y1].kleur == "Speler":
                self.verwijder_pion_aimove(x1, y1)
                self.voeg_pion_aan_aimove(x2, y2, naam)

        if self.aimove.opgevuld[x1][y1] == False and naam != "Bom":
            self.voeg_pion_aan_aimove(x2, y2, naam)

    def voeg_pion_aan_aimove(self, x, y, naam):
        xpos = x
        ypos = y
        teller = 0
        waarde = self.pi.lijst.index(naam)
        if self.aimove.opgevuld[xpos][ypos] is False:
            pion = Pion(waarde, xpos, ypos)
            self.aimove.voeg_pion_toe_spel(pion, xpos, ypos, "Speler")

    def verwijder_pion_aimove(self, x, y):
        if self.aimove.opgevuld[x][y]:
            self.aimove.opgevuld[x][y] = False
            self.aimove.board[x][y] = None
            self.aimove.aantalPionnen -= 1

    def opgevuld_aimove(self, x, y):
        if self.aimove.opgevuld[x][y]:
            return True
        else:
            return False

    def aantal_gekend(self):
        return self.ais.aantalPionnen

    def aantal_bewegen(self):
        return self.aimove.aantalPionnen

    def opgevuld_ais(self, x, y):
        if self.ais.opgevuld[x][y]:
            return True
        else:
            return False


