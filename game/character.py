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
        return self.name, self.classfunction, self.action, self.inventorySpace, self.life, self.defense, self.strength, self.intelligence

    def setLife(self, atrib):
        self.life = self.life - atrib;


