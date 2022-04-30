import threading
import socket
import time

from game.utils.utils import utils

DATASIZE = 2048
ADDRESS = 'localhost'

def network():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((ADDRESS, 7777))
    except:
        return print(f'\nNão foi possível se conectar ao servidor!\n')

    #username = input('Usuário> ')
    print(f'\nConectado')

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
            print(f'\nNão foi possível permanecer conectado no servidor!\n')
            print(f'Pressione <Enter> Para continuar...')
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
    print(f'\n ---------------\n DATA RECEBIDA{typeMsg} \n ---------------\n')

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
    areamsg = msg[100:150]
    roommsg = msg[150:450]
    classmsg = msg[450:470]
    itemsmsg = msg[470:750]
    datamsg = msg[750:1010]
    codes = utils.parser(menuMsg)

    print(f'\n {datamsg.strip()} \n')
    writingProtocol(codes, menuMsg, classmsg, areamsg, roommsg, itemsmsg, client)

def messageTEXT(msg):
    print(f'\n{msg}')


#WRITING PROTOCOL MESSAGES
def writingProtocol(codes, menuMsg, classe, areas, rooms, itemsmsg, client):
    while True:
        print(f'MENUPRINT: {menuMsg}')
        decision = input('Selecione sua próxima ação: ')

        if decision not in codes:
            print(f'\n Ação desconhecida. Por favor, faça uma ação válida!')
        else:
            if decision == '0':
                messageUPDT(client)
                break
            elif decision == '1':
                messageMOVE(client, 'MOVE', areas, rooms)
                break
            elif decision == '2':
                messageBATT(client, 'BATT', classe)
                pass
            elif decision == '3':
                messageBPAC(client, 'BPAC') #procurar itens, usar itens [lista de itens na mochila]
            elif decision == '4':
                messageTwoFields(client, 'PART')
            elif decision == '5':
                messageTwoFields(client, 'NEXT')

#MESSAGE TO UPDATE CLIENT DATA - UPDATE
def messageUPDT(client):
    #trata aqui os dados
    atribute = []
    name = ''
    classe = ''
    
    while True:
        print(f'\nIniciando a criação de personagem...')

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

#MESSAGE BACKPACK THINGS
def messageBPAC(client, code):
    print('Você tem certeza que está de mochila? Eu acho que não...')
    sendMessages(f'{BPAC}', client)


#MESSAGE TO MOVE THE PLAYER - MOVE
def messageMOVE(client, areas, rooms, code):
    area = ''
    room = ''

    while True:
        print('\nVocê irá para onde?')

        area = input('\n1.Navegar pelas salas\n2.Mudar de área (Você não poderá retornar)')

        if area != '1' or area != '2':
            print('\n Ação inválida!')
        else: 
            break

    if area == '1':
        count = 0
        for room in rooms:
            print(f'{count}. {room[count]}')

        while True:
            room = input('\nPara qual salá você vai?')


    sendMessages(f'{code}{areas[area]}{rooms[room]}', client)

#MESSAGE TO BATTLE MODE - BATT
def messageBATT(client, code, classe):
    action = ''

    #which spell
    msg = ''

    while True:
        print('\nQue tipo de ação de combate você fará?')

        if classe == '1': #mago
            action = input('\n1.Ataque')
            
            if action != '1':
                print('\n Ação inválida!')
            else:
                break

        elif classe == '2': #tanque
            action = input('\n1.Ataque\n2.defesa')
            
            if action != '2' or action != '1':
                print('\n Ação inválida!')
            else:
                break
        
        elif classe == '3': #suporte
            action = input('\n1.Ataque\n3.cura')
            
            if action != '1' or action != '3':
                print('\n Ação inválida!')
            else:
                break


    sendMessages(f'{code}{action}{msg}', client)

#MESSAGE TO RECEIVE INFO ABOUT THE OTHER PLAYER - PART
#MESSAGE TO FINISH THE ROUND - NEXT
def messageTwoFields(client, code):
    flagGetData = '1'
    sendMessages(f'{code}{flagGetData}', client)


network()