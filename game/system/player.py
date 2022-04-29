class player():
    def __init__(self, charac, client):
        self.charac = charac
        self.client = client
        self.life = 0
        self.action = 0
        self.pos = ["O castelo", "Saguão principal"]

    def setAction(self, value):
        self.action = value

    def setPos(self, newPos):
        self.pos[0] = newPos[0]
        self.pos[1] = newPos[1]
    
    def getCharac(self):
        return self.charac
    
    def getClient(self):
        return self.client
