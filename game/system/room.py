class room():
    def __init__(self, name, description):
        self.name = name
        self.description = description

        self.enemy = []
        self.item = []

    def setEnemy(self, enemy):
        self.enemy.append(enemy)

    def getEnemy(self):
        return self.enemy

    def setItem(self, item):
        self.item.append(item)

    def getItem(self):
        return self.Item 
    
    def getInfo(self):
        return [self.name, self.description]

