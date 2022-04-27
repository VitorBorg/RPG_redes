class item():
    def __init__(self, name, description, strength, life, defense, intelligence):
        self.name = name
        self.description = description

        self.life = life
        self.defense = defense
        self.strength = strength
        self.intelligence = intelligence
    
    def getInfo(self):
        return self.name, self.description

    def getAtrib(self):
        return self.life, self.defense, self.strength, self.intelligence

