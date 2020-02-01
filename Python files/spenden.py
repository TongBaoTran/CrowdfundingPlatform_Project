class Spenden:
    def __init__(self, spender, projekt, spendenbetrag, sichtbarkeit):
        self.spender = spender
        self.projekt = projekt
        self.spendenbetrag = spendenbetrag
        self.sichtbarkeit = sichtbarkeit

    def getspender(self):
        return self.spender

    def getprojekt(self):
        return self.projekt

    def getspendenbetrag(self):
        return self.spendenbetrag

    def getsichtbarkeit(self):
        return self.sichtbarkeit

