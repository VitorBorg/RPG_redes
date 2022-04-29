from ast import While
import threading
import socket
import time
from game.system.player import player
from game.actors.character import character
from game.system.rpg import rpg
from game.utils.utils import utils


clients = []
rpgGame = rpg('O castelo')

DATASIZE = 2048

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
        server.bind(('localhost', 7777))
        server.listen()
        print('\nServidor iniciado. Aguardando jogadores.\n')
        sentence = 'testando a porra do split'
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
    sendMessageToAllClients(messageWrite('INFO', '', 'characters', ''))

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
            sendMessageToClient(messageWrite('TEXT', "", "", 'Sua rodada'), rpgGame.getPlayers()[turn].client)
            while True:
                sendMessageToClient(messageWrite('INFO', '', 'default', rpgGame.dataPrint('default', turn)), rpgGame.getPlayers()[turn].client)
        else:
            sendMessageToAllClients(messageWrite('TEXT', "", "", 'Rodada de inimigos'))

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
        
#SEND PROTOCOL MESSAGES
def messageWrite(code, flags, menuOption, msg):
    menu = rpgGame.menuPrint(menuOption)

    if code == 'INFO':
        #CODIGO DA MENSAGEM, MENU DO JOGO, CORPO DO TEXTO
        return (code + ('{:<100}'.format(menu)) + ('{:<500}'.format(msg)))
    elif code == 'TEXT':
        return (code + msg)

network()