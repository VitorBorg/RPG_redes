class enemy():

    def __init__(self, nameType, life, strength, intelligence):
        self.nameType = nameType

        self.life = life
        self.strength = strength
        self.intelligence = intelligence

    def getName(self):
        return self.nameType

    def getStatus(self):
        return self.nameType, self.life, self.strength, self.intelligence

    def getDescription(self):
        return (f'\nnome:   {self.nameType}\nPontos de vida:  {self.life}\nPontos de força:    {self.strength}\nPontos de inteligência:    {self.intelligence}\n')

    def setLife(self, atrib):
        self.life = (self.life - atrib)
