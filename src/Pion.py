class Pion:
    def __init__(self, waarde,x,y):
        self.lijst = ["Bom","Spion","Verkenner","Mineur","Sergeant","Luitenant","Kapitein","Majoor","Kolonel","Generaal","Maarschalk","Vlag"]
        self.waarde = int(waarde)
        self.kleur = ""
        self.moveable = True
        self.naam = self.lijst[self.waarde]
        self.visible = True
        self.x = x
        self.y = y
        self.aantal_stappen = 0
        if self.waarde == 0 or self.waarde > 10:
            self.moveable = False
            self.aantal_stappen = 0
        elif self.waarde == 2:
            self.aantal_stappen = 10
        else:
            self.aantal_stappen = 1
    def set_kleur(self, kleur):
        self.kleur = kleur

    def set_visible(self):
        self.visible = True

    def set_hidden(self):
        self.visible = False

    def is_bom(self):
        return self.waarde == 0

    def is_vlag(self):
        return self.waarde == 11
    
    def is_maarschalk(self):
        return self.waarde == 10

    def is_spion(self):
        return self.waarde == 1
    
    def set_visible(self,bool):
        if bool == True:
            self.visible = True
            self.pic = "pics\\"+self.naam+".png"
        else:
            self.visible = False
            self.pic = "pics\\Rood Achterkant.png"

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getKleur(self):
        return self.kleur


