class Kommentar:

    def __init__(self, id, text, sichtbarkeit):
        self.id = id
        self.text = text
        self.sichtbarkeit = sichtbarkeit


    def getid(self):
        return self.id

    def gettext(self):
        return self.text

    def getsichtbarkeit(self):
        return self.sichtbarkeit


