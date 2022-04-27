import threading
import socket
import time

from game.utils.utils import utils


def network():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('localhost', 7777))
    except:
        return print('\nNão foi possível se conectar ao servidor!\n')

    #username = input('Usuário> ')
    print('\nConectado')

    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=['',client])

    thread1.start()
    thread2.start()


def receiveMessages(client):
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            #print(msg)
            readingProtocol(msg, client)
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            client.close()
            break
            
def sendMessages(msg, client):
    while True:
        try:
            client.send(msg.encode('utf-8'))
        except:
            return

#READING PROTOCOL MESSAGES
def readingProtocol(msg, client):
    typeMsg = msg[0:4]

    if typeMsg == 'INFO':
        messageINFO(msg[4:len(msg)-1], client)
    elif typeMsg == 'TEXT':
        messageTEXT(msg[4:len(msg)-1])
    elif typeMsg == 'EXIT':
        pass


#MESSAGE TO GET INFORMATION ABOUT THE CURRENT GAME STATUS - GET
#FLAGS: BOARD, AREA, ROOM, STATS, ITEMS, OTHERS PLAYERS...
def messageINFO(msg, client):
    menuMsg = msg[0:100]
    #print(f"\n MENUMSG: {menuMsg}")
    data = msg[100: len(msg)-1]
    #print(f"\n data = {data}")
    codes = utils.parser(menuMsg)
    #print(f"\n codes = {codes}")

    print('\n' + data + 'n')
    writingProtocol(codes, menuMsg, client)

def messageTEXT(msg):
    print(msg)


#WRITING PROTOCOL MESSAGES
def writingProtocol(codes, menuMsg, client):
    while True:
        print(menuMsg)
        decision = input('Selecione sua próxima ação: ')

        if decision not in codes:
            print('\n Ação desconhecida. Por favor, faça uma ação válida!')
        else:
            if decision == '0':
                messageUPDT(client)
                break
            elif decision == '1':
                pass
            elif decision == '2':
                pass
            elif decision == '3':
                pass
            elif decision == '4':
                pass
            elif decision == '5':
                pass

#MESSAGE TO UPDATE CLIENT DATA - UPDATE
def messageUPDT(client):
    #trata aqui os dados
    atribute = []
    name = ''
    classe = ''
    
    while True:
        print('\nIniciando a criação de personagem...')

        print('\n.')
        time.sleep(1)
        print('\n.')
        time.sleep(1)
        print('\n.')
        time.sleep(1)
        
        name = input('\nQual o nome do seu personagem? ')

        while classe != '1' and classe != '2' and classe != '3':
            print('\nQual a classe do ser personagem?')
            classe = input('\n1.Mago\n2.Tanque\n3.Suporte\n')
        
        print('\nGerando atributos...')
        print('\n.')
        time.sleep(1)
        print('\n.')
        time.sleep(1)

        if classe == '1':
            atribute = utils.createAtrib([2, 5], [0, 1], [12, 25], [18, 29], [0, 4])
        elif classe == '2':
            atribute = utils.createAtrib([1, 3], [0, 0], [50, 79], [4, 11], [0, 2])
        elif classe == '3':
            atribute = utils.createAtrib([4, 7], [0, 3], [11, 22], [3, 15], [8, 19])

        print('\nQuase tudo pronto...\n')
        time.sleep(1)
        break

    sendMessages('UPDT' + name + classe + atribute, client)

#MESSAGE TO ACTION - SET
#FLAGS:INITIAL SETUP, MOVEMENT, FIGHT, ITEMS FROM BACKPACK
def messageGAME(msg):
    return ('ACTN' + msg)


network()