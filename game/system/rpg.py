import sys
from os.path import dirname, abspath

from game.system.player import player
from game.system.room import room
from game.system.area import area
from game.system.item import item

from game.actors.character import character
from game.actors.enemy import enemy

sys.path.append(dirname(dirname(abspath(__file__))))
from utils.utils import utils


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

        self.area[0].setRoom(room('Saguão principal', 'Entrada do castelo.'))
        self.area[0].setRoom(room('Sala de jantar', 'Uma sala de jantar com uma grande mesa e cheia de comida.'))
        self.area[0].setRoom(room('Torre do norte', 'Uma grande torre com tesouros desconhecidos.'))
        self.area[0].setRoom(room('Laboratório', 'Um velho laboratório destruído, com vários equipamentos.'))

        self.area[1].setRoom(room('Celas', 'Celas para prisioneiros.'))

        self.area[0].getRoom()[2].setItem(item('Poção de cura', 'Uma poção solitária, esquecida atrás da porta. Parece que alguém saiu com pressa.',0,2,0,0))
        self.area[0].getRoom()[1].setItem(item('Frango', 'Indescutivelmente em bom estado. Mas parece que os outros alimentos não estão assim...',0,10,0,0))
        self.area[0].getRoom()[3].setItem(item('Pergaminho', '', 0, 10, 0, 0))
        
        return (f"\n##### BEM VINDO AO RPG {self.gameName}####\n Como jogar:\n\nAproveite!\n")
        #print("you are in: " + self.room + "- have " + str(self.room_enemies) + " enemies alive" + " and you can move to")
        #print(self.available_moves)

    def story(self):
        storyText = []
        storyText.append(['\n\nDiferente do que pensavam, a névoa se intensificou a ponto de quase se tornar uma chuva.', 2])
        storyText.append(['Sem muitas possibilidades o que resta é continuar andando.', 4])
        storyText.append(['Mas exaustão já atinge a ambos.', 4])
        storyText.append(['E o silêncio expõe a desesperança.',5])
        storyText.append(['Um estranho brilho, amarelado, entre a névoa, se mostra.', 3])
        storyText.append(['Vocês caminham em direção a ela.', 4])
        storyText.append(['... e caminham...', 3])
        storyText.append(['... e caminham...', 3])
        storyText.append(['... e caminham...', 4])
        storyText.append(['É uma mansão. Não parece bem cuidada. Apenas um lampião da rua está aceso.', 3])
        storyText.append(['Mas vocês entram mesmo assim...', 0])

        return storyText


    def addPlayer(self, player):
        self.players.append(player)
    
    def getPlayers(self):
        return self.players

    def findPlayer(self, client):
        for c in self.players:
            if players[c].client == client:
                return c

    def getCharacters(self):
        return self.characters

    def nextTurn(self):
        self.boardTurn += 1

        #resetando os pontos de acao no final da rodada
        for act in self.players:
            act.setAction(act.charac.action)


        self.playerturn += 1

        if self.playerturn >= 3:
            self.playerturn = 0
    
    def getTurn(self):
        return self.boardTurn

    def getAreas(self):
        return self.area

    #MENU DE ESCOLHAS
    def menuPrint(self, menu):
        #padrao
        if menu == 'default':
            return('1.Movimentar-se\n2.Atacar\n3.Curar\n4.Acessar Mochila\n5.Informações da mesa\n6. Finalizar rodada')
        #RODADA DE SELECAO DE PERSONAGEM
        elif menu == 'characters':
            return ('0.Criar personagem')

    def dataPrint(self, data, num):
        if data == 'default':

            indexArea = utils.getIndexArea(self.area, self.players[num].getPos()[0])
            indexRoom = utils.getIndexRoom(self.area[indexArea].room, self.players[num].getPos()[1])
            
            roomData = self.area[indexArea].room[indexRoom]
            roomEnemys = 'Onde, aparentemente, não há inimigos.'
            if len(roomData.getEnemy()) > 0:
                roomEnemys = f'Onde tem {len(roomData.getEnemy())} {roomData.getEnemy()[0].getName()}.'

            return(f'Você está na {self.players[num].getPos()[1]}, na area {self.players[num].getPos()[0]}. {roomEnemys}')
        
    def enemyTurn(self):
        #index = 0
        rooms = []
        #indexArea = utils.getIndexArea(self.area, self.players[0].pos[0])
        #indexRoom = utils.getIndexRoom(self.area[indexArea].room, self.players[0].pos[1])

        for player in self.players:
            attack = True
            indexArea = utils.getIndexArea(self.area, player.getPos()[0])
            indexRoom = utils.getIndexRoom(self.area[indexArea].room, player.getPos()[1])

            enemy = self.area[indexArea].room[indexRoom].getEnemy()

            for place in rooms:
                if place[0] == indexArea and place[1] == indexRoom:
                    attack = False

            if len(enemy) > 0 and attack == True:
                rooms.append([indexArea, indexRoom])
                player.getCharac().setLife(enemy[0].getStatus()[2])

                
