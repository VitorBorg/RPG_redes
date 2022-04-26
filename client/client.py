import threading
import socket

def network():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('localhost', 7777))
    except:
        return print('\nNão foi possívvel se conectar ao servidor!\n')

    #username = input('Usuário> ')
    print('\nConectado')

    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client])

    thread1.start()
    thread2.start()


def receiveMessages(client):
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            print(msg+'\n')
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            client.close()
            break
            
def sendMessages(client):
    while True:
        try:
            msg = input('\n')

            if msg == 2:
                send = messageGETT(msg)
            elif msg == 1:
                send = messageGAME(msg)
            elif msg == 0:
                while msg == 0:
                    msg = input('\n')
                send = messageINIT(msg)

            client.send(send.encode('utf-8'))
        except:
            return

#WRITING PROTOCOL MESSAGES
#MESSAGE TO UPDATE CLIENT DATA - UPDATE
def messageUPDT(msg):
    return ('UPDT' + msg)

#MESSAGE TO ACTION - SET
#FLAGS:INITIAL SETUP, MOVEMENT, FIGHT, ITEMS FROM BACKPACK
def messageGAME(msg):
    return ('ACTN' + msg)

#MESSAGE TO GET INFORMATION ABOUT THE CURRENT GAME STATUS - GET
#FLAGS: BOARD, AREA, ROOM, STATS, ITEMS, OTHERS PLAYERS...
def messageINFO(msg):
    return ('INFO' + msg)

network()