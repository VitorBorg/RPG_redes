import threading
import socket
import time

from game.utils.utils import utils

DATASIZE = 2048

def network():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('localhost', 7777))
    except:
        return print('\nNão foi possível se conectar ao servidor!\n')

    #username = input('Usuário> ')
    print('\nConectado')

    thread1 = threading.Thread(target=receiveMessages, args=[client])
    #thread2 = threading.Thread(target=sendMessages, args=['',client])

    thread1.start()
    #thread2.start()


def receiveMessages(client):
    while True:
        try:
            msg = client.recv(DATASIZE).decode('utf-8')
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
            break
        except:
            return

#READING PROTOCOL MESSAGES
def readingProtocol(msg, client):
    typeMsg = msg[0:4]
    #print(f'\n ---------------\n DATA RECEBIDA{typeMsg} \n ---------------\n')

    if typeMsg == 'INFO':
        messageINFO(msg[4:len(msg)], client)
    elif typeMsg == 'TEXT':
        messageTEXT(msg[4:len(msg)])
    elif typeMsg == 'EXIT':
        pass


#MESSAGE TO GET INFORMATION ABOUT THE CURRENT GAME STATUS - GET
#FLAGS: BOARD, AREA, ROOM, STATS, ITEMS, OTHERS PLAYERS...
def messageINFO(msg, client):
    menuMsg = msg[0:100]
    #print(f"\n MENUMSG: {menuMsg}")
    data = msg[100: len(msg)]
    #print(f"\n data = {data}")
    codes = utils.parser(menuMsg)
    #print(f"\n codes = {codes}")

    print(f'\n {data.strip()} \n')
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
                messageThreeFields(client, 'MOVE', )
                break
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

    sendMessages(f'UPDT{name}{classe}{atribute[0]}{atribute[1]}{atribute[2]}{atribute[3]}{atribute[4]}', client)

#MESSAGE TO ACTION - SET
#FLAGS:INITIAL SETUP, MOVEMENT, FIGHT, ITEMS FROM BACKPACK

#MESSAGE TO MOVE THE PLAYER - MOVE
#MESSAGE TO BATTLE MODE - BATT
#MESSAGE TO GET THE DATA OR USE SOME ITEM FROM BACKPACK
def messageThreeFields(client, code, flag, msg):
     sendMessages(f'{code}{flag}{msg}', client)

#MESSAGE TO RECEIVE INFO ABOUT THE OTHER PLAYER - PART
#MESSAGE TO FINISH THE ROUND - NEXT
def messageTwoFields(client, code):
    flagGetData = '1'
    sendMessages(f'{code}{flagGetData}', client)


network()