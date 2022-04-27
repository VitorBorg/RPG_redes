from game.system.player import player
from game.system.room import room
from game.system.area import area
from game.system.item import item

from game.actors.character import character
from game.actors.enemy import enemy


class rpg:
    def __init__(self, name):
        self.gameName = name
        self.boardTurn = 0
        self.characters = []
        self.area = []

        self.playerturn = 0
        self.players = []
        self.available_moves = ["left","right","up","down"]

    def play(self):
        #self.characters.append(character('Adalto', 'Atirador', '7', '3', '22', '1', '14', '6'))
        #self.characters.append(character('Luizinho', 'Suporte', '11', '6', '15', '1', '7', '12'))
        #self.characters.append(character('Dudu', 'Tanque', '6', '0', '55', '28', '9', '0'))
        #self.characters.append(character('Nati', 'Mago', '5', '2', '25', '0', '6', '55'))

        self.area.append(area('O castelo', 'Um velho castelo abandonado - Mas pode-se ouvir gritos de longe...'))
        self.area.append(area('Masmorra', 'Um lugar úmido, fedorento e nada acolhedor.'))

        self.area[0].setRoom(room('Saguão principal','Entrada do castelo.'))
        self.area[0].setRoom(room('Sala de jantar', 'Uma sala de jantar com uma grande mesa e cheia de comida.'))
        self.area[0].setRoom(room('Torre do norte', 'Uma grande torre com tesouros desconhecidos.'))
        self.area[0].setRoom(room('Laboratório','Um velho laboratório destruído, com vários equipamentos.'))

        self.area[1].setRoom(room('Celas','Celas para prisioneiros.'))

        self.area[0].getRoom()[2].setItem(item('Poção de cura', 'Uma poção solitária, esquecida atrás da porta. Parece que alguém saiu com pressa.',0,2,0,0))
        self.area[0].getRoom()[1].setItem(item('Frango', 'Indescutivelmente em bom estado. Mas parece que os outros alimentos não estão assim...',0,10,0,0))
        self.area[0].getRoom()[3].setItem(item('Pergaminho', '', 0, 10, 0, 0))

        return (f"\n##### BEM VINDO AO RPG {self.gameName}####\n Como jogar:\n\nAproveite!\n")
        #print("you are in: " + self.room + "- have " + str(self.room_enemies) + " enemies alive" + " and you can move to")
        #print(self.available_moves)

    def addPlayer(self, player):
        self.players.append(player)
    
    def getPlayers(self):
        return self.players

    def getCharacters(self):
        return self.characters

    def nextTurn(self):
        self.boardTurn += 1

        self.playerturn += 1

        if self.playerturn >= 3:
            self.playerturn = 0
    
    def getTurn(self):
        return self.boardTurn

    #MENU DE ESCOLHAS
    #1. MOVIMENTAR
    #2. COMBATE
    #3. ITEMS NA MOCHILA

    def menuPrint(self, menu):
        #RODADA DE SELECAO DE PERSONAGEM
        if menu == 'characters':
            return ('0.Criar personagem')
        #RODADA DE MOVIMENTACAO
        #RODADA DE USO DE ITENS NA MOCHILA
        #RODADA DE COMBATE

    def defaultPrint():
        return 


if __name__ == '__main__':
    game = rpg()
    game.play()
