class area():
    def __init__(self, name, description):
        self.name = name
        self.description = description

        self.room = []

    def setRoom(self, room):
        self.room.append(room)

    def getRoom(self):
        return self.room

    def getRoomByName(self, roomName):
        for rname in room:
            if rname.name == roomName:
                return rname 
    
    def getInfo(self):
        return [self.name, self.description]

