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
            #print(f'RECEIVE DATA: \n{msg}')
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
    areamsg = msg[100:150]
    roommsg = msg[150:450]
    classmsg = msg[450:470]
    itemsmsg = msg[470:750]
    datamsg = msg[750:1010]
    codes = utils.parser(menuMsg)

    #print(f'\n@@@@@@@@@@@@@@@@@@@@\n{classmsg}\n{datamsg}\n@@@@@@@@@@@@@@@@@@@@')

    print(f'\n{datamsg.strip()} \n')

    #print(f'\n##################\n')
    writingProtocol(codes, menuMsg.strip(), classmsg.strip(), areamsg.strip(), roommsg.strip(), itemsmsg.strip(), client)

def messageTEXT(msg):
    print(f'\n{msg}')


#WRITING PROTOCOL MESSAGES
def writingProtocol(codes, menuMsg, classe, areas, rooms, itemsmsg, client):
    print('[Custo de pontos de ação]')
    while True:
        print(f'{menuMsg}')
        decision = input('\nSelecione sua próxima ação: ')

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

        print('\n...')
        #time.sleep(1)
        
        name = input('\nQual o nome do seu personagem? ')

        while classe != '1' and classe != '2' and classe != '3':
            print('\nQual a classe do seu personagem?')
            classe = input('\n1.Mago\n2.Tanque\n3.Suporte\nQual classe você escolhe? ')
        
        print('\nGerando atributos...')
        print('\n...')
        #time.sleep(1)

        if classe == '1':
            atribute = utils.createAtrib([4, 7], [0, 1], [12, 25], [18, 29], [0, 4])
        elif classe == '2':
            atribute = utils.createAtrib([4, 5], [0, 0], [50, 79], [4, 11], [0, 2])
        elif classe == '3':
            atribute = utils.createAtrib([4, 8], [0, 3], [11, 22], [3, 15], [8, 19])

        print('\nQuase tudo pronto...\n')
        time.sleep(1)
        break

    sendMessages(f'UPDT{"{:<20}".format(name)}{"{:<20}".format(classe)}{"{:<2}".format(atribute[0])}{"{:<2}".format(atribute[1])}{"{:<2}".format(atribute[2])}{"{:<2}".format(atribute[3])}{"{:<2}".format(atribute[4])}', client)

#MESSAGE BACKPACK THINGS
def messageBPAC(client, code):
    print('Você tem certeza que está de mochila? Eu acho que não...')
    sendMessages(f'{BPAC}', client)


#MESSAGE TO MOVE THE PLAYER - MOVE
def messageMOVE(client, code, areas, rooms):
    area = ''
    listRoom = rooms.splitlines()
    listareas = areas.splitlines()
    choiceArea = 0
    choiceRoom = 0

    #print(f'#####################\n{areas}\n##################')

    while True:
        print('\nVocê irá para onde?')

        area = input('\n0.Navegar pelas salas\n1.Mudar de área (Você não poderá retornar)\n')

        if area != '0' and area != '1':
            print('\n Ação inválida!')
        else: 
            break

    print('\n')

    if area == '0':
        count = 0
        for r in listRoom:
            print(f'{count}. {r}')
            count += 1
        
        #precisa fazer a verificacao do valor
        choiceRoom = input('\nPara qual sala voce vai?\n')
    elif area == '1':
        count = 0
        for r in listareas:
            print(f'{count}. {r}')
            count += 1
        
        #precisa fazer a verificacao do valor
        choiceArea = input('\nPara qual área voce vai?\n')


    #print('\n##############\n')
    #print(f'\n!!    {(choiceArea)} and  {(choiceRoom)}      !!n')
    #print(f'\n{listareas[int(choiceArea)]} and {listRoom[int(choiceRoom)]}\n')
    #{"{:<100}".format(menu)}
    sendMessages(f'{code}{"{:<100}".format(listareas[int(choiceArea)])}{"{:<100}".format(listRoom[int(choiceRoom)])}', client)

#MESSAGE TO BATTLE MODE - BATT
def messageBATT(client, code, classe):
    action = ''

    #which spell
    msg = ''

    while True:
        print('\nQue tipo de ação de combate você fará?')

        if classe == '1': #mago
            action = input('\n1.Ataque [4]')
            
            if action != '1':
                print('\n Ação inválida!')
            else:
                break

        elif classe == '2': #tanque
            action = input('\n1.Ataque[4] \n2.defesa [todos os pontos]')
            
            if action != '2' or action != '1':
                print('\n Ação inválida!')
            else:
                break
        
        elif classe == '3': #suporte
            action = input('\n1.Ataque [4]\n3.curar[3 pontos]')
            
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