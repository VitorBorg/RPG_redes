class enemy():

    def __init__(self, nameType, life, defense, strength, intelligence):
        self.nameType = nameType

        self.life = life
        self.defense = defense
        self.strength = strength
        self.intelligence = intelligence

    def getStatus(self):
        return self.nameType, self.life, self.defense, self.strength, self.intelligence

    def getDescription(self):
        return (f'\nnome:   {self.nameType}\nPontos de vida:  {self.life}\nPontos de defesa:  {self.defense}\nPontos de força:    {self.strength}\nPontos de inteligência:    {self.intelligence}\n')

    def setLife(self, atrib):
        self.life = (self.life - atrib)
