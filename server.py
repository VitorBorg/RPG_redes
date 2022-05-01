from ast import While
import threading
import socket
import time
from xml.dom.pulldom import CHARACTERS
from game.system.player import player
from game.actors.character import character
from game.system.rpg import rpg
from game.utils.utils import utils


clients = []
rpgGame = rpg('O castelo')
event = threading.Event()

DATASIZE = 2048
ADDRESS = 'localhost'
#'localhost'

def messagesTreatment(client):
    while True:
        try:
            msg = client.recv(DATASIZE)
            readingProtocol(msg.decode('utf-8'), client)

            #print('\n!!SERVER RECEIVE MESSAGE !!')

            if len(rpgGame.getPlayers()) >= 2:
                event.set()
                #print('\n!!SERVER PASS GAME WHILE !!')
        except:
            deleteClient(client)
            break


def sendMessageToAllClients(msg):
    for clientItem in clients:
        time.sleep(.3)
        try:
            clientItem.send(msg.encode('utf-8'))
        except:
            print('\nErro no envio da mensagem!\n')


def sendMessageToClient(msg, client):
        client.send(msg.encode('utf-8'))


def broadcast(msg, client):
    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(msg)            
            except:
                deleteClient(clientItem)


def deleteClient(client):
    clients.remove(client)


#CONEXAO E O LOOP
def network():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((ADDRESS, 7777))
        server.listen()
        print('\nServidor iniciado. Aguardando jogadores.\n')
    except:
        return print('\nNão foi possível iniciar o servidor!\n')

    while True and len(clients) < 2:
        client, addr = server.accept()
        clients.append(client)

        #INITIAL MESSAGES
        print(f'Cliente conectado! {len(clients)}/2 usuários!\n')
        sendMessageToClient(messageWrite('TEXT', "", "", f'Você entrou no lobby! Você é o usuário: {len(clients)}!\n'), client)

        #THREADS
        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()

        if len(clients) == 2:
            thread = threading.Thread(target=game)
            thread.start()

def game():
    #mensagem inicial
    sendMessageToAllClients(messageWrite('TEXT', "", "", rpgGame.play()))
    #mensagem de criacao de personagens
    sendMessageToAllClients(messageWrite('CHARAC', '', 'characters', ''))

    #loop da criacao de personagem
    while len(rpgGame.getPlayers()) < 2:
        time.sleep(5)
        print(f'Aguardando jogadores... {len(rpgGame.getPlayers())} de 2 players prontos.')

    
    #print dos atributos
    print('Jogadores cadastrados...')
    time.sleep(2)
    msg = ''
    for p in rpgGame.getPlayers():
        msg = msg + utils.completeDescription(p)
    
    sendMessageToAllClients(messageWrite('TEXT', "", "", msg))
    time.sleep(4)

    #set
    event.set()

    #historia de inicio
    #for line in rpgGame.story():
    #    sendMessageToAllClients(messageWrite('TEXT', "", "", line[0]))
    #    time.sleep(line[1])

    #inicio real do jogo
    while event.is_set():
        print('\nLOOP')
        turn = rpgGame.getTurn()

        if rpgGame.getBoss().getLife() <= 0:
            sendMessageToAllClients(messageWrite('TEXT', "", "", '\n Parabéns! Vocês venceram o Boss! O jogo acabou!'))
            break
        elif rpgGame.getAllAlive() == False:
            sendMessageToAllClients(messageWrite('TEXT', "", "", '\n Infelizmente vocês não conseguiram! Todos os jogadores estão com a vida zerada! O jogo acabou!'))
            break
        elif turn == 0 or turn == 1:
            sendMessageToAllClients(messageWrite('TEXT', "", "", 'Rodada de algum jogador'))

            if rpgGame.getPlayers()[turn].getLife() <= 0:
                sendMessageToAllClients(messageWrite('TEXT', "", "", 'O jogador dessa rodada não tem mais vida!'))
                rpgGame.nextTurn()
            else:
               sendMessageToClient(messageWrite('INFO', rpgGame.getPlayers()[turn], 'default', rpgGame.dataPrint('default', turn)), rpgGame.getPlayers()[turn].client)
        else:
            sendMessageToAllClients(messageWrite('TEXT', "", "", 'Rodada de inimigos'))

            rpgGame.enemyTurn()

            charac = [rpgGame.getPlayers()[0], rpgGame.getPlayers()[1]]
            textMessage = (f'Os inimigos jogaram...\nO {charac[0].getCharac().getStatus()[0]} está com {charac[0].getLife()} de vida!\nO {charac[1].getCharac().getStatus()[0]} está com {charac[1].getLife()} de vida!')
            sendMessageToAllClients(messageWrite('TEXT', "", "", textMessage))
        
        print('\nENVIOS DA RODADA FEITOS\n')
        print(f'\nturn: {rpgGame.getTurn()}')

        if rpgGame.getTurn() != 2:
            event.clear()
            event.wait()
        else:
            rpgGame.nextTurn()

        #print('\nCOMANDO RECEBIDO\n')
    
    sendMessageToAllClients(messageWrite('TEXT', "", "", 'Conexão finalizada!'))
    print('Finalizada')
    for c in clients:
        deleteClient(c)

#READING PROTOCOL MESSAGES
def readingProtocol(msg, client):
    typeMsg = msg[0:4]

    if typeMsg == 'UPDT':
        messageUPDT(msg[4:len(msg)], client)
    elif typeMsg == 'MOVE':
        messageMOVE(msg[4:len(msg)], client)
    elif typeMsg == 'BATT':
        messageBATT(msg[4:len(msg)], client)
    elif typeMsg == 'BPAC':
        messageBPAC(msg[4:len(msg)], client)
    elif typeMsg == 'PART':
        messagePART(client)
    elif typeMsg == 'NEXT':
        messageNEXT()

def messageUPDT(msg, client):
    name = msg[0:20].strip()
    classe = msg[20:40].strip()
    action = int(msg[40:42].strip())
    space = int(msg[42:44].strip())
    life = int(msg[44:46].strip())
    strength = int(msg[46:48].strip())
    intelligence = int(msg[48:50].strip())

    classe = utils.nameClass(classe)

    newPlayer = player(character(name, classe, action, space, life, strength, intelligence), client)
    rpgGame.addPlayer(newPlayer)
    event.set()
    #writingProtocol(codes, menuMsg, client)

def messageMOVE(msg, client):
    area = msg[0:100].strip()
    room = msg[100:200].strip()

    #player = rpgGame.findPlayer(client)
    turn = rpgGame.getTurn()
    player = rpgGame.getPlayers()[turn]

    if player.getPos()[0] != area:
        print('CHANGE AREA')
        index = utils.getIndexArea(rpgGame.getAreas(), area)
        player.setPos([area, rpgGame.getAreas()[index].getRoom()[0].getInfo()[0]])
        player.setAction(player.getActionValue())  
    else:
        print('CHANGE ONLY ROOM')
        player.setPos([area, room])
        player.setAction(4)
    event.set()

def messageBATT(msg, client):
    action = msg[0:1].strip()

    player = rpgGame.getPlayers()[rpgGame.getTurn()]
    
    #ataque
    if action == '1':
        indexArea = utils.getIndexArea(rpgGame.getAreas(), player.getPos()[0])
        indexRoom = utils.getIndexRoom(rpgGame.getAreas()[indexArea].room, player.getPos()[1])
        
        enemy = rpgGame.getAreas()[indexArea].room[indexRoom].getEnemy()

        if len(enemy) > 0:
            enemy[0].setLife(player.getCharac().getStatus()[5])
            time.sleep(.2)
            sendMessageToAllClients(messageWrite('TEXT', "", "", f'{player.getCharac().getStatus()[0]} atacou {enemy[0].getStatus()[0]} e deixou ele com {enemy[0].getStatus()[1]} pontos de vida!'))

            if enemy[0].getStatus()[1] <= 0:
                rpgGame.getAreas()[indexArea].room[indexRoom].getEnemy().remove(enemy[0])
        else:
            sendMessageToAllClients(messageWrite('TEXT', "", "", f'{player.getCharac().getStatus()[0]} tentou atacar alguma coisa... E não acertou nada! Parece que não há inimigos lá.'))
    #defender
    elif action == '2':
        cure = player.getCharac().getStatus()[6]
        player.setCure(cure)

        sendMessageToAllClients(messageWrite('TEXT', "", "", f'{player.getCharac().getStatus()[0]} se defendeu e recuperou {cure} pontos de vida!'))
    #curar
    elif action == '3':
        cure = player.getCharac().getStatus()[6]

        for pl in rpgGame.getPlayers():
            if pl != player:
                pl.setCure(cure)

        sendMessageToAllClients(messageWrite('TEXT', "", "", f'{player.getCharac().getStatus()[0]} curou todos (exceto ele mesmo) em {cure} pontos de vida!'))    
    
    #atacar, verifica a sala se tem inimigos, pega o [0] e manda ataque baseado no dano com dados
    #defender, aumenta um pouco a vida baseado na inteligencia com dados
    #curar, cura todos os personagens baseado na inteligencia com dados

def messageBPAC(msg, client):
    #O personagem [nome] da classe [classe] está na sala [sala], na area [area], com [vida] de vida.
    sendMessageToClient(messageWrite('TEXT', "", "", 'Sua rodada'), rpgGame.getPlayers()[rpgGame.getTurn()].client)

def messagePART(client):
    #O personagem [nome] da classe [classe] está na sala [sala], na area [area], com [vida] de vida. 
    #Ele possui [strength] de força, [intelligence] de inteligência, e a mochila com espaço para [space] itens.

    msg = ''
    for p in rpgGame.getPlayers():
        msg = msg + utils.completeDescription(p)
    
     
    sendMessageToClient(messageWrite('TEXT', "", "", msg), client)

def messageNEXT():
    print("\nRECEBIDO")
    print(f'\n{rpgGame.getTurn()}')
    #for action in rpg.getPlayers():
    #    action.resetAction()
    rpgGame.nextTurn()
    print(f'\nCHANGE {rpgGame.getTurn()}')
    time.sleep(1)
    event.set()
        
#SEND PROTOCOL MESSAGES
def messageWrite(code, player, menuOption, msg):
    menu = rpgGame.menuPrint(menuOption)

    if code == 'INFO':
        #CODIGO DA MENSAGEM, MENU DO JOGO, CORPO DO TEXTO
        #count = 0
        menuRooms = ''
        indexArea = utils.getIndexArea(rpgGame.getAreas(), player.getPos()[0])
        menuAreas = ''

        for room in rpgGame.getAreas()[indexArea].getRoom():
            if room.getInfo()[0] != player.getPos()[1]:
                menuRooms = f'{menuRooms}\n{room.getInfo()[0]}'
                #count += 1

        #adicionando as areas
        menuAreas = f'{menuAreas}\n{player.getPos()[0]}'
        for a in rpgGame.getAreas():
            if player.getPos()[0] != a.getInfo()[0]:
                menuAreas = f'{menuAreas}\n{a.getInfo()[0]}'

        return (f'{code}{"{:<100}".format(menu)}{"{:<50}".format(menuAreas)}{"{:<300}".format(menuRooms)}{"{:<20}".format(player.getCharac().getStatus()[1])}{"{:<280}".format("")}{"{:<260}".format(msg)}')
    elif code == 'TEXT':
        return (f'{code}{msg}')
    elif code == 'CHARAC':
         return (f'{"INFO"}{"{:<100}".format(menu)}{"{:<50}".format("")}{"{:<300}".format("")}{"{:<20}".format("")}{"{:<100}".format("")}')

network()