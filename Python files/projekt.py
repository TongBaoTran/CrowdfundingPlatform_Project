class Projekt():

    def __init__(self, kennung, titel, beschreibung, finanzierungslimit, ersteller,vorgaenger,kategorie ):
        self.kennung = kennung
        self.titel = titel
        self.beschreibung=beschreibung
        self.finanzierungslimit = finanzierungslimit
        self.ersteller = ersteller
        self.vorgaenger = vorgaenger
        self.kategorie = kategorie

    def getkennung(self):
        return self.kennung


    def gettitel(self):
        return self.titel

    def getbeschreibung(self):
        return self.beschreibung

    def getfinanzierungslimit(self):
        return self.finanzierungslimit

    def getersteller(self):
        return self.ersteller

    def getvorgaenger(self):
        return self.vorgaenger

    def getkategorie(self):
        return self.kategorie






