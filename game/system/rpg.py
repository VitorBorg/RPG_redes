class rpg:
    def __init__(self, name):
        self.gameName = name
        self.boardTurn = 0

        self.playerturn = 0
        self.players = []
        self.available_moves = ["left","right","up","down"]

    def play(self):
        print( "##### WELCOME TO RPG ####")
        print("\n How to play:")
        print(" Something.")
        print("enjoy!")
        print("you are in: " + self.room + "- have " + str(self.room_enemies) + " enemies alive" + " and you can move to")
        print(self.available_moves)

    def addPlayer(self, player):
        self.players.append(player)
    
    def getPlayers(self):
        return self.players

    def nextTurn(self):
        self.boardTurn += 1

        self.playerturn += 1

        if self.playerturn >= 3:
            self.playerturn = 0
    
    def getTurn(self):
        return self.boardTurn

    def menuPrint(self):
        #RODADA DE SELECAO DE PERSONAGEM
        if self.boardTurn == 0:
            return (f'/n \n')
        #RODADA DE MOVIMENTACAO
        #RODADA DE USO DE ITENS NA MOCHILA
        #RODADA DE COMBATE

    def defaultPrint():
        return 


if __name__ == '__main__':
    game = rpg()
    game.play()
