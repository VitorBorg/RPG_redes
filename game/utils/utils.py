import random


class utils():
    def getDice(atrib, size):
        return (atrib + random.randint(0, size))
    
    def createAtrib(action, space, life, strength, intel):
        atribute = []

        print('\n INSIDE ATRIB' + action[0] + ', '+ action[1])
        #action points
        act = random.randint(action[0],action[1])
        if act < 10:
            act = '0' + act
        atribute.append(act + '')

        #inventorySpace
        invt = random.randint(space[0],space[1])
        if invt < 10:
            invt = '0' + invt
        atribute.append(invt + '')

        #life
        lf = random.randint(life[0],life[1])
        if lf < 10:
            lf = '0' + lf
        atribute.append(lf + '')

        #strength
        str = random.randint(strength[0],strength[1])
        if stre < 10:
            stre = '0' + stre
        atribute.append(stre + '')

        #intelligence
        inte = random.randint(intel[0],intel[1])
        if inte < 10:
            inte = '0' + inte
        atribute.append(inte + '')

        return atribute

    def parser(msg):
        data = msg.splitlines()
        code = []

        for c in data:
            code.append(c[0])
        
        return code

