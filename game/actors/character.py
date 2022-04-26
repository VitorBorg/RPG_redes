class character():

    def __init__(self, name, classfunction, action, inventorySpace, life, defense, strength, intelligence):
        self.name = name
        self.classFunction = classfunction
        self.action = action
        self.inventorySpace = inventorySpace

        self.life = life
        self.defense = defense
        self.strength = strength
        self.intelligence = intelligence

    def getStatus(self):
        return self.name, self.classFunction, self.action, self.inventorySpace, self.life, self.defense, self.strength, self.intelligence

    def getDescription(self):
        return (f'\nnome:   {self.name}\nclasse:    {self.classFunction}\nPontos de ação:   {self.action}\nTamanho do inventário:    {self.inventorySpace}\nPontos de vida:  {self.life}\nPontos de defesa:  {self.defense}\nPontos de força:    {self.strength}\nPontos de inteligência:    {self.intelligence}\n')

    def setLife(self, atrib):
        self.life = self.life - atrib


