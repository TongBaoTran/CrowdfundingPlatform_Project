class Benutzer:

    def __init__(self, email, name, beschreibung):
        self.email = email
        self.name = name
        self.beschreibung=beschreibung

    def getemail(self):
        return self.email

    def getname(self):
        return self.name

    def getbeschreibung(self):
        return self.beschreibung
