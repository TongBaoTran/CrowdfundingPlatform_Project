class Kategorie():

    def __init__(self, id, name, icon):
        self.id = id
        self.name = name
        self.icon=icon

    def getid(self):
        return self.id

    def getname(self):
        return self.name

    def geticon(self):
        return self.icon
