import random


class utils():
    def getDice(atrib, size):
        return (atrib + random.randint(0, size))
    
    def createAtrib(action, space, life, strength, intel):
        atribute = []


        #action points
        act = random.randint(action[0],action[1])
        if act < 10:
            act = f'0{act}'
        atribute.append(f'{act}')

        #inventorySpace
        invt = random.randint(space[0],space[1])
        if invt < 10:
            invt = f'0{invt}'
        atribute.append(f'{invt}')

        #life
        lf = random.randint(life[0],life[1])
        if lf < 10:
            lf = f'0{lf}'
        atribute.append(f'{lf}')

        #strength
        strength = random.randint(strength[0],strength[1])
        if strength < 10:
            strength = f'0{strength}'
        atribute.append(f'{strength}')

        #intelligence
        intel = random.randint(intel[0],intel[1])
        if intel < 10:
            intel = f'0{intel}'
        atribute.append(f'{intel}')

        return atribute

    def parser(msg):
        data = msg.splitlines()
        code = []

        for c in data:
            code.append(c[0])
        
        return code

    def getIndexArea(area, name):
        index = 0

        for a in area:
            if a.getInfo()[0] == name:
                return index
            index += 1

    def getIndexRoom(room, name):
        index = 0

        for a in room:
            if a.getInfo()[0] == name:
                return index
            index += 1

    def nameClass(msg):
        if msg == '1':
            return ('mago')
        elif msg == '2':
            return ('tanque')
        elif msg == '3':
            return ('suporte')

    def completeDescription(player):
        #O personagem [nome] da classe [classe] está na sala [sala], na area [area], com [vida] de vida. 
        #Ele possui [strength] de força, [intelligence] de inteligência, e a mochila com espaço para [space] itens.
        msg = ''
        atrib = player.getCharac().getStatus()
        msg = msg + (f'O personagem {atrib[0]} da classe {atrib[1]} está na sala {player.getPos()[1]}, na area {player.getPos()[0]}, com {player.getLife()} de vida.\n')
        msg = msg + (f'Ele possui {atrib[5]} de força, {atrib[6]} de inteligência, a mochila com espaço para {atrib[3]} itens, e o total de {atrib[2]} pontos de ação!\n\n')

        return (msg)

