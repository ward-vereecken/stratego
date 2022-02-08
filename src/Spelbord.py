from Pion import Pion

class Bord(object):
    def __init__(self, aantalPionnen=0, lengte=10, breedte=10):
        self.board = [[None]*(lengte) for _ in range(breedte)]
        self.water = [(4, 2), (4, 3), (4, 6), (4, 7),
                      (5, 2), (5, 3), (5, 6), (5, 7)]
        self.aantalPionnen = aantalPionnen
        self.lengte = lengte
        self.breedte = breedte
        self.opgevuld = []                          # houdt bij of er ergens een pion staat
        self.pionnen = {}  # houdt per coördinaat de pion bij
        self.aantalComp = {"Bom" : 6, "Spion" : 1, "Verkenner" : 8, "Mineur" :5,
                                          "Sergeant" : 4,"Luitenant" :4,"Kapitein" : 4,"Majoor" :3,"Kolonel" : 2,"Generaal" :1,"Maarschalk" :1,"Vlag" :1}
        self.aantalSpeler = {"Bom" : 6,"Spion" : 1,"Verkenner" : 8,"Mineur" :5,
                                          "Sergeant" : 4,"Luitenant" :4,"Kapitein" : 4,"Majoor" :3,"Kolonel" : 2,"Generaal" :1,"Maarschalk" :1,"Vlag" :1}
        n = 10
        m = 10
        for i in range(n):
            self.opgevuld = [[False]*n for _ in range(m)]        # eerst leeg bord => alles False

                         # als 0 wordt gereturned, geef error bericht

    def voeg_pion_toe_spel(self, pion, x, y, zijde):
        if self.opgevuld[x][y] is False:
            self.opgevuld[x][y] = True
            self.board[x][y] = pion
            self.pionnen[x, y] = Pion
            self.aantalPionnen += 1
            pion.kleur = zijde
            print("Naam: "+self.board[x][y].naam+" kracht: "+str(self.board[x][y].waarde))
        else:
            print("Er staat al een pion!")



    def verwijder_pion(self, x, y):
        if self.opgevuld[x][y] is True:
            self.opgevuld[x][y] = False
            self.board[x][y] = None
            self.aantalPionnen -= 1
        else:
            return 0
