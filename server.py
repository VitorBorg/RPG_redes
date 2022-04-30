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

DATASIZE = 2048
ADDRESS = 'localhost'
#'localhost'

def messagesTreatment(client):
    while True:
        try:
            msg = client.recv(DATASIZE)
            readingProtocol(msg.decode('utf-8'), client)
        except:
            deleteClient(client)
            break


def sendMessageToAllClients(msg):
    for clientItem in clients:
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
    #sendMessageToAllClients(messageWrite('CHARAC', '', 'characters', ''))

    #loop da criacao de personagem
    while len(rpgGame.getPlayers()) < 2:
        time.sleep(5)
        print(f'Aguardando jogadores... {len(rpgGame.getPlayers())} de 2 players prontos.')

    
    #inicio real do jogo
    print('Jogadores cadastrados...')
    time.sleep(2)

    #storytext = rpgGame.story()

    #for line in storytext:
    #    sendMessageToAllClients(messageWrite('TEXT', "", "", line[0]))
    #    time.sleep(line[1])

    while True:
        turn = rpgGame.getTurn()

        if turn == 0 or turn == 1:
            sendMessageToAllClients(messageWrite('TEXT', "", "", 'Rodada de algum jogador'))
            #sendMessageToClient(messageWrite('TEXT', "", "", 'Sua rodada'), rpgGame.getPlayers()[turn].client)
            while True:
                sendMessageToClient(messageWrite('INFO', '', 'default', rpgGame.dataPrint('default', turn)), rpgGame.getPlayers()[turn].client)
        else:
            sendMessageToAllClients(messageWrite('TEXT', "", "", 'Rodada de inimigos'))
            rpgGame.enemyTurn()

            charac = [rpgGame.getPlayers()[0].getCharac(), rpgGame.getPlayers()[1].getCharac()]
            sendMessageToAllClients(messageWrite('TEXT', "", "", f'Os inimigos jogaram...\nO {charac[0].getStatus[0]} está com {charac[0].getStatus[4]} de vida!\nO {charac[1].getStatus[0]} está com {charac[1].getStatus[4]} de vida!'))

        time.sleep(20)
        print('\nJOGO RODANDO')

#READING PROTOCOL MESSAGES
def readingProtocol(msg, client):
    typeMsg = msg[0:4]

    if typeMsg == 'UPDT':
        messageUPDT(msg[4:len(msg)], client)
    elif typeMsg == 'TEXT':
        messageTEXT(msg[4:len(msg)])
    elif typeMsg == 'EXIT':
        pass

def messageUPDT(msg, client):
    name = msg[0:20]
    classe = msg[20:40]
    action = msg[40:42]
    space = msg[42:44]
    life = msg[44:46]
    strength = msg[46:48]
    intelligence = msg[48:50]

    newPlayer = player(character(name, classe, action, space, life, strength, intelligence), client)
    rpgGame.addPlayer(newPlayer)
    #writingProtocol(codes, menuMsg, client)

def messageMOVE(msg, client):
    area = msg[0:100]
    room = msg[100:200]

    player = rpgGame.findPlayer(client)
    player.setPos([area, room])
    player.setAction(5)

def messageBATT(msg, client):
    action = msg[0:1]

    #atacar, verifica a sala se tem inimigos, pega o [0] e manda ataque baseado no dano com dados
    #defender, aumenta um pouco a vida baseado na inteligencia com dados
    #curar, cura todos os personagens baseado na inteligencia com dados

def messageBPAC(msg):
    #O personagem [nome] da classe [classe] está na sala [sala], na area [area], com [vida] de vida.
    sendMessageToClient(messageWrite('TEXT', "", "", 'Sua rodada'), rpgGame.getPlayers()[turn].client)

def messagePART(msg):

    #O personagem [nome] da classe [classe] está na sala [sala], na area [area], com [vida] de vida.
    sendMessageToClient(messageWrite('TEXT', "", "", 'Sua rodada'), rpgGame.getPlayers()[turn].client)

def messageNEXT(msg):
    rpgGame.nextTurn()
        
#SEND PROTOCOL MESSAGES
def messageWrite(code, player, menuOption, msg):
    menu = rpgGame.menuPrint(menuOption)

    if code == 'INFO':
        #CODIGO DA MENSAGEM, MENU DO JOGO, CORPO DO TEXTO
        count = 0
        menuRooms = ''
        indexArea = utils.getIndexArea(rpgGame.getAreas(), player.getPos()[0])

        for room in rpgGame.getAreas()[indexArea]:
            if room.getInfo()[0] != player.getPos()[1]:
                menuRooms = f'{menuRooms}\n{count}. {room.getInfo()[0]}'
                count += 1
#       return (f'{code}{"{:<100}".format(menu)}{"{:<50}".format('')}{"{:<300}".format(menuRooms)}{"{:<20}".format(player.getCharac().getStatus()[1])}{"{:<100}".format('')}')
        return (f'{code}{"{:<100}".format(menu)}{"{:<50}".format("")}{"{:<300}".format(menuRooms)}{"{:<20}".format(player.getCharac().getStatus()[1])}{"{:<100}".format("")}{"{:<260}".format(msg)}')
    elif code == 'TEXT':
        return (f'{code}{msg}')
    elif code == 'CHARAC':
         return (f'{"INFO"}{"{:<100}".format(menu)}{"{:<50}".format("")}{"{:<300}".format("")}{"{:<20}".format("")}{"{:<100}".format("")}')

network()