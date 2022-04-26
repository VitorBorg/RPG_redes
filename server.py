import threading
import socket
from game.player import player
from game.actors.character import character


clients = []

def messagesTreatment(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg, client)
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
    except:
        return print('\nNão foi possível iniciar o servidor!\n')

    while True and len(clients) < 2:
        client, addr = server.accept()
        clients.append(client)

        print(f'Cliente conectado! {len(clients)}/2 usuários!\n')
        sendMessageToClient(f'Você entrou no lobby! Você é o usuário: {len(clients)}!\n', client)

        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()

        if len(clients) == 2:
            thread = threading.Thread(target=game)
            thread.start()

def game():

    sendMessageToAllClients('\n\nJOGO INICIADO!\n\n')

    players = []
    characters = []

    characters.append(character('Adalto', 'Atirador', '7', '3', '22', '1', '14', '6'))
    characters.append(character('Luizinho', 'Suporte', '11', '6', '15', '1', '7', '12'))
    characters.append(character('Dudu', 'Tanque', '6', '0', '55', '28', '9', '0'))
    characters.append(character('Nati', 'Mago', '5', '2', '25', '0', '6', '55'))

    for char in characters:
        sendMessageToAllClients(f'\nSTATUS{char.getDescription()}')
    
    sendMessageToAllClients('\n\nEscolha seu personagem: ')

    while True and len(players) != 2:
        temp = ''

    

    while True:
        temp = ''

#READING PROTOCOL MESSAGES
def message(msg):
    typeMsg = msg[0:4]

    if typeMsg == 'ACTN':
        pass
    elif typeMsg == 'GETT':
        pass
    elif typeMsg == 'SETP':
        pass
        


network()