class Konto():

    def __init__(self, inhaber, guthaben, geheimzahl):
        self.inhaber = inhaber
        self.guthaben = guthaben
        self.geheimzahl=geheimzahl

    def getinhaber(self):
        return self.inhaber

    def getguthaben(self):
        return self.guthaben

    def getgeheimzahl(self):
        return self.geheimzahl

