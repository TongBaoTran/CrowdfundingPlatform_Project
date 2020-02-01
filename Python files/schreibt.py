class Schreibt:

    def __init__(self, benutzer, projekt, kommentar):
        self.benutzer = benutzer
        self.projekt = projekt
        self.kommentar=kommentar

    def getbenutzer(self):
        return self.benutzer

    def getprojekt(self):
        return self.projekt

    def getkommentar(self):
        return self.kommentar
