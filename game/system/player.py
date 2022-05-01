class player():
    def __init__(self, charac, client):
        self.charac = charac
        self.client = client
        self.life = charac.getStatus()[4]
        self.action = charac.getStatus()[2]
        self.pos = ["O castelo", "Saguão principal"]
        self.items = []

    def setAction(self, value):
        self.action = (self.action - value)
    
    def getAction(self):
        return(self.action)
    
    def resetAction(self):
        self.action = self.charac.getStatus()[2]
    
    def getActionValue(self):
        return self.charac.getStatus()[2]

    def setLife(self, value):
        self.life = (self.life - value)
    
    def getLife(self):
        return (self.life)
        
    def setCure(self, value):
        if value + self.life > self.charac.getStatus()[4]:
            self.life = self.charac.getStatus()[4]
        else:
            self.life = (self.life + value)

    def setPos(self, newPos):
        self.pos[0] = newPos[0]
        self.pos[1] = newPos[1]

    def getPos(self):
        return (self.pos)
    
    def getCharac(self):
        return self.charac
    
    def getClient(self):
        return self.client

    def setItems(self, item):
        if self.charac.getStatus()[3] < len(self.items):
            self.items.append(item)
    
    def getItems(self):
        return self.items
