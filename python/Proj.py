import remote_play as r_p,colored,random,sys


data = {'range':4 , 'storage':600,'move':10,'regeneration':25}
data1  = {'range':4 , 'storage':600,'move':10,'regeneration':25}

cost = {'cruiser' :750,
        'tanker':1000}
        
Upgrades = {'regeneration': {'value':5,'energiecost':750,'max':500}
            , 'storage':{'value':100,'energiecost':600,'max':900}
            ,'range':{'value':1,'energiecost':400,'max':9}
            ,'move':{'value':-1,'energiecost':500,'max':5}
          }
J1 = {}
J2 = {}
peaks = {}

def create_ship(name,category,clan):
        """
        funct to create a ship in the data base and so on the board

        Parameters
        ---------
        name : the name we want to attribute to our ship (str)
        category : create a tank or a dmg   (str)
        clan : choose in wich clan it will be created (str)

        return
        ------
        J1,J2 : the new data base

        specification
        ------------
        Salvio v2   23/03/20

        implementation
        -------------
        Salvio V3   23/03/20
        """
        if name not in J2 and name not in J1:       # test si le vaisseau existe déjà ou pas
            if clan == 'J2':                           #test si on a decidé J2 comme clan
                if category =='cruiser' :                       #test si c'est un cruiser qu'on veux
                    if J2['hub2']['energie'] - cost['cruiser'] >= 0:        #test si on a assez d'energie pour le créer
                        J2[name]= {'pts_struct':100, 'energie':400,'maxenergy':400,'range':data1['range'],'temporary_state':0, 'energycost':10,'move':data1['move'],'groupforce':1,'type':1,'state':0} #crée le cruiser
                        J2[name]['coox']=J2['hub2']['coox']        #fait spawn le vaisseau sur le hub
                        J2[name]['cooy']=J2['hub2']['cooy']         
                        J2['hub2']['energie'] -= cost['cruiser']   #baisse l'energie du hub ayant crée le vaisseau (cruiser)


                elif category =='tanker':                           #test si c'est un tanker qu'on veux
                    if J2['hub2']['energie'] - cost['tanker'] >= 0:                 # fait le même qu'au dessus
                        J2[name]= {'pts_struct': 50, 'energie': 600,'storage': data1['storage'],'type':0,'state2':0, 'state1':0,'state':0}
                        J2[name]['coox']=J2['hub2']['coox']
                        J2[name]['cooy']=J2['hub2']['cooy']
                        J2['hub2']['energie'] -= cost['tanker']




            if clan =='J1':                                   #test si on a pris J1 comme clan
                if category =='cruiser' :                   #fait le meme qu'au dessus pour les cruisers
                    if J1['hub1']['energie'] - cost['cruiser'] >= 0:
                        J1[name]= {'pts_struct':100, 'energie':400,'maxenergy':400,'range':data['range'],'temporary_state':0, 'energycost':10,'move':data['move'],'groupforce':1,'type':1,'state':0}
                        J1[name]['coox']=J1['hub1']['coox']
                        J1[name]['cooy']=J1['hub1']['cooy']
                        J1['hub1']['energie'] -= cost['cruiser']


                elif category =='tanker':                                   #fait le même qu'au dessus pour les tanker 
                    if J1['hub1']['energie'] - cost['tanker'] >= 0:
                        J1[name]= {'pts_struct': 50, 'energie': 600,'storage': data['storage'],'type':0, 'state2':0,'state1':0,'state':0}
                        J1[name]['coox']= J1['hub1']['coox']
                        J1[name]['cooy']= J1['hub1']['cooy']
                        J1['hub1']['energie'] -= cost['tanker']



        return J1,J2

def createpeak(file):
    """
    funct to create peaks data base (db)

    return
    ------
    peaks: dict of peak

    speci
    -----
    Salvio V1

    imple
    -----
    Salvio V4
    """
    f = open(file,"r+")                #read the board file

    map = f.readline()
    map1 = f.readline()
    hubs = f.readline()
    hub1 = f.readline()
    hub2 = f.readline()
    peakz = f.readline()

    ma= len(f.readlines(-1))            #recolte le nombre de peak a créer
    f.close()               #close de file

    peaks = {}              #fait la db des peaks

    f = open(file,"r")                 #read board file to find peaks coordinate and energie level
    for useless in range(6):
        useless= f.readline()

    for line in range(ma):              #prend les infos des peaks pour créer un dictionaire avec (en bouclant les lignes du fichier)
        peak = f.readline()
        peak = peak.split()
        peaks[line]= {}                 #fait la db de chaque peak qui se retrouvera dans la grande db de tout les peaks
        peaks[line]['coox']= int(peak[0])               #prend les info de coox du peak
        peaks[line]['cooy'] = int(peak[1])                  #prend les info de cooy du peak
        peaks[line]['energie'] = int(peak[2])               #prend les info d'energie du peak
    f.close()                                           #close le file
    return peaks


def createhub(file):
    """
    set up hub on random coord by looking at the board info and place hub in J1,J2 playing db

    return
    ------
    J1,J2 : new data base with hub in it

    speci
    ------
    Salvio V1   25/03/20

    imple
    -----
    Salvio V3       25/03/20
    """
    f = open(file,"r+")             #open board file
    map = f.readline()
    map1 = f.readline()
    hubs = f.readline()
    hub1 = f.readline()
    hub1 = hub1.split()                 #crée une list avec les stats du hub1
    hub2 = f.readline()
    hub2 = hub2.split()                 #crée une list avec les stats du hub2
    f.close()                       #ferme le board file
    J1['hub1'] = {}                 #crée le dictio de hub1
    J1['hub1']['coox']=int(hub1[0])             #x
    J1['hub1']['cooy']=int(hub1[1])                 #y
    J1['hub1']['pts_struct'] = int(hub1[2])             #points de stucture
    J1['hub1']['energie'] = int(hub1[3])                #l'energie
    J1['hub1']['maxenergy'] = int(hub1[3])              #la capacité maximale
    J1['hub1']['regeneration'] = int(hub1[4])           #le taux de regeneration
    J1['hub1']['type'] = 2                  #donne une valeur de type pour éviter des erreurs plus tard
    J2['hub2'] = {}                 #crée le dictio de hub2
    J2['hub2']['coox']=int(hub2[0])             #tout le même qu'au dessus
    J2['hub2']['cooy']=int(hub2[1])
    J2['hub2']['pts_struct'] = int(hub2[2])
    J2['hub2']['energie'] = int(hub2[3])
    J2['hub2']['maxenergy'] = int(hub2[3])
    J2['hub2']['regeneration'] = int(hub2[4])
    J2['hub2']['type']=2
    return J1,J2

def charge_board_starting(file):

    """ funct to charge the board,hubs and peaks

    speci
    -----
    Salvio v1.2  23/03/20

    imple
    -----
    Salvio v3 23/03/20

    """

    f = open(file,"r+")                 #open board file
    map = f.readline()
    map1 = f.readline()
    map1 = map1.split()                 #create a list with the board columns and rows in it
    nb_rows = map1[1]                   
    nb_cols = map1[0]
    nb_rows = int(nb_rows)          #set string to int
    nb_cols = int(nb_cols)
    f.close()               #close board file

    fill = ' '             #defini fill sur du vide pour avoir juste le background
    s = ''                                #defini s en str
    for row in range(nb_rows):                      #boucle pour créer chaque case en fonction de la taille du board demandé
        for col in range(nb_cols):
            if col%2==0 and row%2!=0:       #en x1 y2 x1 y4 c'est bleu 'clair'
                s += colored.bg(80)
            elif col%2!=0 and row%2==0:     #en x2 y1 x2 y3 c'est bleu 'clair'
                s += colored.bg(80)
            elif col%2!=0 and row%2!=0:     #en x1 y1 x1 y3 x3 y3 c'est bleu 'foncé'
                s += colored.bg(33)
            else:
                s+= colored.bg(33)          # le reste (x2 y2 x2 y4) c'est bleu 'foncé'

            if row == J1['hub1']['cooy'] and col ==J1['hub1']['coox'] :                 #test à chaque coordonnée pour savoir si on doit afficher le hub là
                fill = 'Ω'                                                      #met un symbole pour le hub trouvé
                s += colored.bg(124)                                #met une couleur de background pour le hub trouvé
            elif row ==J2['hub2']['cooy'] and col ==J2['hub2']['coox'] :  #test à chaque coordonnée pour savoir si on doit afficher le hub là             
                fill = 'Ω'                              #met un symbole pour le hub trouvé  
                s+= colored.bg(99)                      #met une couleur de background pour le hub trouvé
            else:
                fill = ' '                      #si pas de hub on met un champ vide sans symbole
            for peak in peaks:                      #on boucle le dictionaire de peaks
                if row == peaks[peak]['cooy'] and col == peaks[peak]['coox'] and fill == ' ':           #on regarde si un peak est au coordonnée x,y bouclée (comme pour hub)
                    fill = '೦'                          #on met un symbole
                    s +=colored.attr(0)                 #on reset la couleur du background
                    s+= colored.bg(2)                   #on met le background en vert à l'emplacement du peak
                    
            for ship in J1:                                                                 #on boucle les données du joueur 1
                if (row == J1[ship]['cooy'] and col == J1[ship]['coox']) and fill == ' ' :          #on regarde si il existe en tel coordonée
                    if J1[ship]['type'] != 2:                   #on verifie que c'est tout sauf un hub
                        if J1[ship]['type'] ==1:                #si c'est un cruiser 
                            fill = '♞'                 #symbole
                            s+= colored.fg(160)         #couleur du symbole
                        if J1[ship]['type'] ==0:        #si tanker  
                            fill = '∎'                  #symbole
                            s+= colored.fg(211)             #couleur symbole

            for ship in J2:                                     #même qu'en haut pour J2
                if (row == J2[ship]['cooy'] and col == J2[ship]['coox']) and fill == ' ' :
                    if J2[ship]['type'] != 2 :
                        if J2[ship]['type'] ==1:
                            fill = '♞'
                            s+= colored.fg(208)
                        if J2[ship]['type'] ==0:
                            fill = '∎'
                            s+= colored.fg(226)


            s += fill           #chaque x1 y1 x1 y2 x1 y3 ça met un vide ou une entité
            s += colored.attr('reset')        #empeche de faire un truc bizarre
        s +=  '\n'            #à chaque bordure de board on descend le curseur 
    print(s)

def move(name,x,y,clan,file):
    """
        funct to move in a certain direction a ship 

        parameters
        ----------
        name : name of the ship(str)
        x : x coordinate you want to go(int)
        y : y coordinate you want to go(int)
        clan : player data base to change (str)

        speci
        -----
        Salvio V2    08/04/20   

        imple
        ------
        Salvio V3 08/04/20
    """   
    f = open(file,"r")             #open le board file
    map = f.readline()
    map1 = f.readline()
    map1 = map1.split()             #fait une structure contenant les limites du board
    f.close()               #ferme le board file
    if clan == 'J1':        #si J1
        if name in J1:      #si J1 existe
            if J1[name]['type'] != 2:                      #si pas un hub
                if J1[name]['state']==0:        #si pas encore excecuté d'action ce tour
                    if 0<= abs(J1[name]['coox'] - x) <2 and 0<= abs(J1[name]['cooy'] - y) < 2 and (abs(J1[name]['coox'] - x) + abs(J1[name]['cooy'] - y))!=0:      #def dist total
                        distance = max(abs(J1[name]['coox'] - x),abs(J1[name]['cooy'] - y))     #evalue la distance parcourue
                        if J1[name]['type'] == 1:       #si c'est un cruiser
                            energy_cost = J1[name]['move']            # def le cout energetique pour bouger d'une case
                            if distance * energy_cost  <= J1[name]['energie']:              #test si assez d'energie pour bouger autant
                                if 0 < x < int(map1[0])  and 0 < y < int(map1[1]):            #bordure
                                    J1[name]['energie'] -= (distance*energy_cost)         #baisse energie consommé
                                    J1[name]['coox'],J1[name]['cooy'] = x,y             #met les coordonnées du vaisseau à jour
                                    J1[name]['state'] = 1                       #met l'état à 1 donc déjà fait un action ce tour
                #montre le board
                              
                        if J1[name]['type'] == 0:                   #si c'est un tanker
                            if 0 < x < int(map1[0])  and 0 < y < int(map1[1]):          #bordure
                                J1[name]['coox'],J1[name]['cooy'] = x,y             #nouvelle coo
                                J1[name]['state'] = 1               #met l'état à 1
                                     #charge le board


    if clan == 'J2':            #si J2
        if name in J2:          #si le ship existe dans J2
            if J2[name]['type'] != 2:                      #le même qu'en haut
                if J2[name]['state']==0:

                    if 0<= abs(J2[name]['coox'] - x) <2 and 0<= abs(J2[name]['cooy'] - y) < 2 and (abs(J2[name]['coox'] - x) + abs(J2[name]['cooy'] - y))!=0:      #def dist total
                        distance = max(abs(J2[name]['coox'] - x),abs(J2[name]['cooy'] - y))
                        if J2[name]['type'] == 1: 
                            energy_cost = J2[name]['move']            
                            if distance * energy_cost  <= J2[name]['energie']:              
                                if 0 < x < int(map1[0])  and 0 < y < int(map1[1]):            
                                    J2[name]['energie'] -= (distance*energy_cost)        
                                    J2[name]['coox'],J2[name]['cooy'] = x,y
                                    J2[name]['state'] = 1
                                    
                        if J2[name]['type'] == 0:
                            if 0 < x < int(map1[0])  and 0 < y < int(map1[1]):
                                J2[name]['coox'],J2[name]['cooy'] = x,y
                                J2[name]['state'] = 1
                                
                            
    return J1,J2

def attack(x,y,name,qtt,clan):
    """
    funct to attack entities

    parameters
    ----------  
    x,y : x,y coordinate to attack (int,int)
    name : name of the cruiser that is attacking (str)
    qtt : quantity of dmg we want to deal (int)
    clan : db to change (str)

    return
    -------
    J1,J2: new values of the data base due to structure point and energy changes

     speci
    -----
    Louis,Salvio v2   23/03/20

    imple
    -----
    Louis,Salvio v2   23/03/20

    """
    if clan == 'J1':            #si J1
        if qtt > 0:         #si qtt positive
            if name in J1 and name != 'hub1' and J1[name]['type']==1 and J1[name]['state'] ==0: #si c'est un cruiser qui attaque,qu'il peut attaquer et qu'il existe sans être le hub
                if max(abs(J1[name]['coox'] - x),abs(J1[name]['cooy'] - y)) <= J1[name]['range']:   #si le cruiser à la range pour attaquer en x,y
                    if J1[name]['energie'] >= qtt* J1[name]['energycost'] :             #si il a assez d'energie pour faire autant de dégats
                        for entities in J2:                                             #boucle les entités en J2
                            if J2[entities]['coox'] == x and J2[entities]['cooy'] == y: #si une entité de J2 est sur les coo d'attaque
                                J2[entities]['pts_struct'] -= qtt                   #l'entité subis les degats
                                if J2[entities]['pts_struct'] <=0 and J2[entities]['type']!=2:              #si l'entité n'a plus de point de vie et n'est pas un hub
                                    del J2[entities]                    #on supprime l'entité
                                    charge_board_starting()     #on charge le board
                        for entities in J1:                 #pour les entités dans J1 on boucle
                            if J1[entities]['coox'] == x and J1[entities]['cooy'] == y and J1[name]['coox'] != x and J1[name]['cooy'] !=y:           #si une entité de J1 est sur les coo attaqué et si c'est pas l'entité qui attaque (empeche de s'auto tuer car ça bug la boucle)
                                J1[entities]['pts_struct'] -= qtt           #fait perdre des points de vie en fonctions de l'attaque
                                if J1[entities]['pts_struct'] <=0 and J1[entities]['type']!=2:      #si l'entité n'a plus de point de vie et n'est pas un hub
                                    del J1[entities]            #on supprime
                                    charge_board_starting()     #charge le board
                        J1[name]['energie'] -= J1[name]['energycost'] * qtt   #fait perdre l'energie d'attaque à l'attaquant  
                        J1[name]['state']=1             #bloque l'état du vaisseau
    if clan == 'J2':        #si J2, même qu'en haut
        if qtt > 0:
            if name in J2 and name != 'hub2' and J2[name]['type']==1 and J2[name]['state'] ==0:
                if max(abs(J2[name]['coox'] - x),abs(J2[name]['cooy'] - y)) <= J2[name]['range']:
                    if J2[name]['energie'] >= qtt * J2[name]['energycost']:
                        for entities in J1:
                            if J1[entities]['coox'] == x and J1[entities]['cooy'] == y:
                                J1[entities]['pts_struct'] -= qtt
                                if J1[entities]['pts_struct'] <=0 and J1[entities]['type']!=2:
                                    del J1[entities]
                                    charge_board_starting()
                        for entities in J2:
                            if J2[entities]['coox'] == x and J2[entities]['cooy'] == y and J2[name]['coox'] != x and J2[name]['cooy'] !=y:               #empeche de s'auto tuer
                                J2[entities]['pts_struct'] -= qtt
                                if J2[entities]['pts_struct'] <=0 and J2[entities]['type']!=2:
                                    del J2[entities]
                                    charge_board_starting()
                        J2[name]['energie'] -= J2[name]['energycost'] * qtt
                        J2[name]['state']=1
    return J1,J2

def give_energy(name,name2,clan):
    """
    funct to give energy to friendly entities

    parameters
    ---------
    name : name of the tanker that gives (str)
    name2 : name of the ship or hub that recieve (str)
    clan : db to change (str)

    return
    ------
    J1,J2 : new values of the data base due to energy manipulation

     speci
    -----
    Salvio v2  23/03/20   

    imple
    -----
    Salvio v4       24/04/20
    """
    if clan == 'J1':                    #si J1
        if name in J1 and name2 in J1:      #si les 2 entités sont dans J1 / existent
            if J1[name]['type']==0:         #si le donneur est un tanker
                if J1[name]['energie'] >0:      #si l'energie du donneur est superieur à 0
                    if J1[name]['energie'] + J1[name2]['energie'] <= J1[name2]['maxenergy'] or J1[name]['energie'] + J1[name2]['energie'] <= J1[name2]['storage'] :        #si le receveur n'atteindra pas son max d'energie en recevant celle ci
                        qtt = J1[name]['energie']           #simplification
                    else:
                        if J2[name2]['type'] ==2:
                            qtt = J1[name2]['maxenergy'] - J1[name2]['energie']
                        else:
                            qtt = J1[name2]['storage'] - J1[name2]['energie']
                            if qtt !=0:
                                if max(abs(J1[name]['coox'] - J1[name2]['coox']),abs(J1[name]['cooy']- J1[name2]['cooy'])) <=4 : #si dans cette range il y a le vaisseau devant recevoir
                                    if J1[name]['state2'] == 0:          #si le donneur peut donner
                                        J1[name]['energie'] -= qtt          #le donneur perd l'energie donnée
                                        J1[name2]['energie'] += qtt         #le receveur la recois
                                        J1[name]['state2'] =1                #le donneur devient incapable d'autre action ce tour

    if clan == 'J2':        #si J2 même qu'en haut
        if name in J2 and name2 in J2:
            if J2[name]['type']==0:
                if J2[name]['energie'] >0:
                    if J2[name]['energie'] + J2[name2]['energie'] <= J2[name2]['maxenergy'] or J2[name]['energie'] + J2[name2]['energie'] <= J2[name2]['storage']:
                        qtt = J2[name]['energie']
                    else:
                        if J2[name2]['type'] ==2:
                            qtt = J2[name2]['maxenergy'] - J2[name2]['energie']
                        else:
                            qtt = J2[name2]['storage'] - J2[name2]['energie']
                            if qtt !=0:
                                if max(abs(J2[name]['coox'] - J2[name2]['coox']),abs(J2[name]['cooy']- J2[name2]['cooy'])) <=4 :
                                    if J2[name]['state2'] == 0:
                                        J2[name]['energie'] -= qtt
                                        J2[name2]['energie'] += qtt
                                        J2[name]['state2'] =1
    
    return J1,J2

def pump(name,x,y,clan):
        """
        funct to take energy from peak

        parameters
        ---------
        name : name of the tanker that take energy(str) 
        x,y : coordinate to pump (int)
        clan : db to change (str)

        return
        ------
        J1,J2 : new value of data base due to addition of energy
        peaks : new value of peaks due to substraction of energy

         speci
        -----
        Salvio v2       08/04/20

        imple
        -----
        Salvio v3       25/03/20
        """
        if clan == 'J1':            #si j1
            if name in J1:          #si name existe dans j1
                if J1[name]['type'] == 0:       #si j1 est un tanker
                    if J1[name]['storage'] - J1[name]['energie'] >0:        #si le tanker n'est pas plein
                        qtt = J1[name]['storage'] - J1[name]['energie']     #fixe la qtt d'energie possible de prendre sans overflow
                        for peak in peaks:              #boucle la db des peaks
                                if J1[name]['state1']== 0:           #si l'etat d'action du vaisseau voulant pump est ok
                                    if peaks[peak]['coox'] ==x and peaks[peak]['cooy'] ==y and max(abs(J1[name]['coox'] - x),abs(J1[name]['cooy'] - y)) <= 4 :  #si le tanker à un peak dans sa range
                                        if (peaks[peak]['energie'] - qtt) > 0:      #si le peak à assez d'energie à donner
                                            peaks[peak]['energie'] -=qtt            #la perd
                                            J1[name]['energie'] +=qtt           #le tanker la recois
                                            J1[name]['state1'] = 1           #le tanker devient incapacité ce tour
                                        else: 
                                            peaks[peak]['energie'] -= peaks[peak]['energie']    #si le peak n'a plus assez d'energie (negatif)
                                            J1[name]['energie'] +=peaks[peak]['energie']           #le tanker la recois
                                            J1[name]['state1'] = 1           #le tanker devient incapacité ce tour
                                            del peaks[peak]       #on le met out of boarder pour pas l'afficher
                                            charge_board_starting()     #affiche le board

        if clan =='J2':     #même pour J2
            if name in J2:
                if J2[name]['type'] == 0:
                    if J2[name]['storage'] - J2[name]['energie']  >0:
                        qtt = J2[name]['storage'] - J2[name]['energie']
                        for peak in peaks:
                                if J2[name]['state1']== 0:
                                    if peaks[peak]['coox'] ==x and peaks[peak]['cooy'] ==y and max(abs(J2[name]['coox'] - x),abs(J2[name]['cooy'] - y)) <= 4 :
                                        if (peaks[peak]['energie'] - qtt) > 0:
                                            peaks[peak]['energie'] -=qtt
                                            J2[name]['energie'] +=qtt
                                            J2[name]['state1'] = 1  
                                        else: 
                                            peaks[peak]['energie'] -= peaks[peak]['energie']
                                            J2[name]['energie'] +=peaks[peak]['energie']           #le tanker la recois
                                            J2[name]['state1'] = 1           #le tanker devient incapacité ce tour
                                            del peaks[peak]
                                            charge_board_starting()

        return peaks,J1,J2

def upgrade(up,clan):
    """
    funct to upgrade entities stats

    parameters
    ----------
    up : value to upgrade (str)
    clan : db to change (str)

    return
    ------
    J1,J2 : new db due to basic stats change

     speci
    -----
    Louis,Salvio v1     02/03/20 

    imple
    -----
    Louis,Salvio v1       10/03/20
    """

    if up in Upgrades:      #si l'update demandé existe
        if clan == 'J1':        #si J1
                for entities in J1:     #boucle les entites dans J1
                    if up in J1[entities]:      #si le up possible dans l'entité 
                        if J1[entities][up] != Upgrades[up]['max'] and J1['hub1']['energie'] - Upgrades[up]['energiecost'] >=0 :        #si assez d'energie pour up et maximum non atteint
                            J1[entities][up] += Upgrades[up]['value']       #up l'entité
                            if data[up] != Upgrades[up]['max']:     #si la structure de base n'est pas au max (utile pour create ship)
                                data[up] += Upgrades[up]['value']       #on up la structure de base pour le up demandé(data)
                            J1['hub1']['energie'] -= Upgrades[up]['energiecost']        #baisse l'energie du hub

        elif clan == 'J2':      #même pour J2
            for entities in J2:
                if up in J2[entities]:
                        if J2[entities][up] != Upgrades[up]['max'] and J2['hub2']['energie'] - Upgrades[up]['energiecost'] >=0 :
                            J2[entities][up] += Upgrades[up]['value']
                            if data1[up] != Upgrades[up]['max'] and up != 'regeneration':
                                data1[up] += Upgrades[up]['value'] #on up la structure de base pour le up demandé(data1)
                            J2['hub2']['energie'] -= Upgrades[up]['energiecost']

  
    return J1,J2

def orders(connect,file):
    """ funct to receive and store orders

    parameters
    ----------
    clan : db to change (str)

    return
    -------
    order: all order
    Afunct: all attack order
    Mfunct: all move order
    Pfunct: all pump order
    Gfunct: all give order
    Upgrade_order: all upgrade order
    Shiper: all create ship order

    speci
    -----
    Salvio  13/04/20

    imple
    -----
    Salvio  14/04/20
    """
    orderz =''
    orderz = get_AI_sentence(file)
    J2orders = r_p.get_remote_orders(connect)
    orderz += J2orders
    #orderz += 'poubelle:@0-0'

    orderz = orderz.split('.')


    order = orderz[0].split(' ')       #les ordres sont séparé par ordre (order)


    Afunct =[]      #liste de chaque type d'ordre
    Mfunct= []
    Pfunct= []
    Gfunct= []
    Upgrade_order= []
    Shiper=[]
    for action in order:     #pour tout les 'réel' action dans la liste d'order
        action = action.split(':')        #on sépare l'action pour l'analyser
        if action[0] != '':

            test = action[1].split('*')      #on test le split *
            if test[0] == '':       #si le 1er éléments est vide ça à marché donc c'est une attaque(*)

                attack = test       #on simplifie
                separer = attack[1].split('=')      #on sépare pour avoir les donnée de dmg à droite de la list et les coo non traduite à gauche
                coord = separer[0].split('-')       #on sépare les coo pour les traduire
                qttA = separer[1]       #les degats demandé
                xA = coord[0]           #le x
                yA = coord[1]           # le y
                nameA = action[0]        # le nom du vaisseau attaquant
                Afunct += [[nameA,xA,yA,qttA]]  #on stock 
            else:
                test = action[1].split('@')      #on test @

                if test[0] =='':            #si c'est bien @ c'est un move
                    move = test     #simplification
                    coord = move[1].split('-')      #on sépare/traduit les coo
                    xm = coord[0]       #x 
                    ym = coord[1]       #y
                    namem = action[0]    #nom du vaisseau qui bouge
                    Mfunct += [[namem,xm,ym]]   #on stock

                else:
                    test = action[1].split('<')  #on test 

                    if test[0]=='':     #si c'est vide c'est une demande de pump
                        pump=test   #simpli
                        coord= pump[1].split('-')   #on sépare les coo de pump
                        namep = action[0]        # le nom du pompeur
                        xp = coord[0]       #x
                        yp = coord[1]       #y
                        Pfunct += [[namep,xp,yp]]   #on stock

                    else:
                        test=action[1].split('>')    #test

                        if test[0]=='':                     #si c'est vide c'est give
                            name2g = test[1]        #le nom du donneur
                            nameg = action[0]        #le nom du receveur
                            Gfunct += [[nameg,name2g]]  #on stock
                        else:
                            if action[0] == 'upgrade':   #si c'est pas un nom mais un 'upgrade' en premier de la liste apres le split(:)
                                up = action[1]       #le 2 eme de la liste est le type d'upgrade
                                Upgrade_order += [[up]] #on stock
                            else:
                                if action[1]== 'tanker':     #si le 2eme élément de la liste apres séparaion en ':' est le mot tanker
                                    name = action[0]     #le nom du tanker à créer
                                    category = action[1]     #le type de ship
                                    Shiper += [[name,category]] #on stock
                                elif action[1] == 'cruiser':     #si le 2eme élément de la liste apres séparaion en ':' est le mot cruiser
                                    name = action[0]     #le nom du cruiser à créer
                                    category = action[1] #le type de ship
                                    Shiper += [[name,category]] #on stock
        
    orderJ2=orderz[1].split(' ')
    Afunct2 =[]      #liste de chaque type d'ordre
    Mfunct2= []
    Pfunct2= []
    Gfunct2= []
    Upgrade_order2= []
    Shiper2=[]
    for action1 in orderJ2:     #pour tout les 'réel' action dans la liste d'order
        action1 = action1.split(':')        #on sépare l'action pour l'analyser
        if action1[0] != '':

            test = action1[1].split('*')      #on test le split *
            if test[0] == '':       #si le 1er éléments est vide ça à marché donc c'est une attaque(*)

                attack = test       #on simplifie
                separer = attack[1].split('=')      #on sépare pour avoir les donnée de dmg à droite de la list et les coo non traduite à gauche
                coord = separer[0].split('-')       #on sépare les coo pour les traduire
                qttA = separer[1]       #les degats demandé
                xA = coord[0]           #le x
                yA = coord[1]           # le y
                nameA = action1[0]        # le nom du vaisseau attaquant
                Afunct2 += [[nameA,xA,yA,qttA]]  #on stock 
            else:
                test = action1[1].split('@')      #on test @

                if test[0] =='':            #si c'est bien @ c'est un move
                    move = test     #simplification
                    coord = move[1].split('-')      #on sépare/traduit les coo
                    xm = coord[0]       #x 
                    ym = coord[1]       #y
                    namem = action1[0]    #nom du vaisseau qui bouge
                    Mfunct2 += [[namem,xm,ym]]   #on stock

                else:
                    test = action1[1].split('<')  #on test 

                    if test[0]=='':     #si c'est vide c'est une demande de pump
                        pump=test   #simpli
                        coord= pump[1].split('-')   #on sépare les coo de pump
                        namep = action1[0]        # le nom du pompeur
                        xp = coord[0]       #x
                        yp = coord[1]       #y
                        Pfunct2 += [[namep,xp,yp]]   #on stock

                    else:
                        test=action1[1].split('>')    #test

                        if test[0]=='':                     #si c'est vide c'est give
                            name2g = test[1]        #le nom du donneur
                            nameg = action1[0]        #le nom du receveur
                            Gfunct2 += [[nameg,name2g]]  #on stock
                        else:
                            if action1[0] == 'upgrade':   #si c'est pas un nom mais un 'upgrade' en premier de la liste apres le split(:)
                                up = action1[1]       #le 2 eme de la liste est le type d'upgrade
                                Upgrade_order2 += [[up]] #on stock
                            else:
                                if action1[1]== 'tanker':     #si le 2eme élément de la liste apres séparaion en ':' est le mot tanker
                                    name = action1[0]     #le nom du tanker à créer
                                    category = action1[1]     #le type de ship
                                    Shiper2 += [[name,category]] #on stock
                                elif action1[1] == 'cruiser':     #si le 2eme élément de la liste apres séparaion en ':' est le mot cruiser
                                    name = action1[0]     #le nom du cruiser à créer
                                    category = action1[1] #le type de ship
                                    Shiper2 += [[name,category]] #on stock

    return order,Afunct,Mfunct,Pfunct,Gfunct,Upgrade_order,Shiper,orderJ2,Afunct2,Mfunct2,Pfunct2,Gfunct2,Upgrade_order2,Shiper2
  
def order_exec(connect,file):
    """
    recieve all order by cat and execute them

    parameters
    ----------
    clan : db to change (str)

    return
    ------
    J1,J2: players db
    peaks: peaks db

    speci
    ------
    Salvio  05/04/20

    imple
    ------
    Salvio  05/04/20

    """
    
    order_list = orders(connect,file)           #stock la liste d'ordre


    create_name=[]      #db pour être plus clean
    create_type=[]
    for order in range(len(order_list[6])):     #boucle les ordres de cat create
        create_name.append(order_list[6][order][0])     #ajoute à la liste pour être clean
        create_type.append(order_list[6][order][1])

        create_ship(create_name[order],             #appel de funct
        create_type[order],'J1')


    move_name = []      #db clean
    move_x=[]
    move_y=[]
    for order in range(len(order_list[2])):     #boucle cat move
        move_name.append(order_list[2][order][0])       #add to list
        move_x.append(order_list[2][order][1])
        move_y.append(order_list[2][order][2])

        move(               #call funct
        move_name[order],
        int(move_x[order]),
        int(move_y[order]),
        'J1',file)


    attacker_name = []      #db clean
    attacker_x= []
    attacker_y=[]
    attacker_qtt=[]
    for order in range(len(order_list[1])):         #boucle cat attack
        attacker_name.append(order_list[1][order][0])       #add to list
        attacker_x.append(order_list[1][order][1])
        attacker_y.append(order_list[1][order][2])
        attacker_qtt.append(order_list[1][order][3])

        attack(int(attacker_x[order]),          #call funct
        int(attacker_y[order]),attacker_name[order],
        int(attacker_qtt[order]),
        'J1')


    pump_name=[]        #db clean
    pump_x=[]
    pump_y=[]
    for order in range(len(order_list[3])):         #boucle cat pump
        pump_name.append(order_list[3][order][0])       #add to list
        pump_x.append(order_list[3][order][1])
        pump_y.append(order_list[3][order][2]) 

        pump(pump_name[order],      #call funct
        int(pump_x[order]),
        int(pump_y[order]),
        'J1')


    give_name=[]            #db clean
    give_name2=[]
    for order in range(len(order_list[4])):     #boucle cat give
        give_name.append(order_list[4][order][0]) 
        give_name2.append(order_list[4][order][1]) 

        give_energy(give_name[order],           #call give
        give_name2[order],
        'J1')


    up_name=[]      #db clean
    for order in range(len(order_list[5])): #boucle cat upgrade
        up_name.append(order_list[5][order][0])

        upgrade(up_name[order],'J1')        #call funct




    create_name2=[]      #db pour être plus clean
    create_type2=[]
    for order in range(len(order_list[13])):     #boucle les ordres de cat create
        create_name2.append(order_list[13][order][0])     #ajoute à la liste pour être clean
        create_type2.append(order_list[13][order][1])

        create_ship(create_name2[order],             #appel de funct
        create_type2[order],'J2')


    move_name2 = []      #db clean
    move_x2=[]
    move_y2=[]
    for order in range(len(order_list[9])):     #boucle cat move
        move_name2.append(order_list[9][order][0])       #add to list
        move_x2.append(order_list[9][order][1])
        move_y2.append(order_list[9][order][2])

        move(               #call funct
        move_name2[order],
        int(move_x2[order]),
        int(move_y2[order]),
        'J2',file)


    attacker_name2 = []      #db clean
    attacker_x2= []
    attacker_y2=[]
    attacker_qtt2=[]
    for order in range(len(order_list[8])):         #boucle cat attack
        attacker_name2.append(order_list[8][order][0])       #add to list
        attacker_x2.append(order_list[8][order][1])
        attacker_y2.append(order_list[8][order][2])
        attacker_qtt2.append(order_list[8][order][3])

        attack(int(attacker_x2[order]),          #call funct
        int(attacker_y2[order]),attacker_name2[order],
        int(attacker_qtt2[order]),
        'J2')


    pump_name2=[]        #db clean
    pump_x2=[]
    pump_y2=[]
    for order in range(len(order_list[10])):         #boucle cat pump
        pump_name2.append(order_list[10][order][0])       #add to list
        pump_x2.append(order_list[10][order][1])
        pump_y2.append(order_list[10][order][2]) 

        pump(pump_name2[order],      #call funct
        int(pump_x2[order]),
        int(pump_y2[order]),
        'J2')

    give_name1=[]            #db clean
    give_name3=[]
    for order in range(len(order_list[11])):     #boucle cat give
        give_name1.append(order_list[11][order][0]) 
        give_name3.append(order_list[11][order][1]) 

        give_energy(give_name1[order],           #call give
        give_name3[order],
        'J2')

    up_name1=[]      #db clean
    for order in range(len(order_list[12])): #boucle cat upgrade
        up_name1.append(order_list[12][order][0])

        upgrade(up_name1[order],'J2')        #call funct


    return J1,J2,peaks

def Main(maxturn,file,your_group,other_group=0,other_IP='127.0.0.1', verbose=True):
    """
    main game funct

    parameters
    ----------
    maxturn : nmb of loop ia (int)

    speci
    -----
    Salvio  05/04/20

    imple
    -----
    Salvio  14/04/20
    """
    print('ooookk')
    createhub(file)     #créé les hubs selon le board file
    peaks = createpeak(file)            #stock la db de peak reçue
    while maxturn >0 and J1['hub1']['pts_struct']>0 and J2['hub2']['pts_struct']>0:      #boucle tant qu'on a pas atteint le nombre de tour max ou qu'un des hub est mort
        connect = r_p.create_connection(your_group,other_group,other_IP,verbose)
        r_p.notify_remote_orders(connect,get_AI_sentence(file))
        order_exec(connect,file)
        r_p.close_connection(connect)
        for ship in J1:     #boucle les entités de J1
            if 'state' in J1[ship]:     #si l'entité à le terme state
                J1[ship]['state']=0     #le met à 0 (pour pouvoir être capable d'action)
                J1[ship]['state1']=0
                J1[ship]['state2']=0
                J1[ship]['temporary_state'] =0

        for ship in J2: #boucle les entités de J2
            if 'state' in J2[ship]:         #si l'entité à le terme state
                J2[ship]['state']=0     #le met à 0 (pour pouvoir être capable d'action)
                J2[ship]['state1']=0
                J2[ship]['state2']=0
                J2[ship]['temporary_state'] =0

        
        
        
        J1['hub1']['energie'] += J1['hub1']['regeneration']     #régénére le hub en énergie 
        J2['hub2']['energie'] += J2['hub2']['regeneration']     #régénére le hub en énergie
        maxturn -=1     #décremente le nombre de tour
    return J1,J2

def get_AI_sentence(file):
    
    """Returns orders from naive AI.
    Parameters

    ----------
    ...

    Returns
    ------
    orders: orders of the AI (str)

    speci
    -----
    Salvio v1 13/04/20

    Imple
    -----
    Salvio  v1 08/04/20
    """


    orders = ''     #set as a strings


    f = open(file,"r")                 #open board file
    map = f.readline()
    map1 = f.readline()
    map1 = map1.split()                 #create a list with the board columns and rows in it

    f.close()               #close board file

    if random.random() < .9:
        name = str(random.randint(1, 10000000))
        if random.random() < .5:
            orders += '%s:cruiser ' % name
        else:
            orders += '%s:tanker ' % name
        


    if random.random() < .05:
        orders += 'upgrade:%s ' % random.choice(('regeneration', 'storage', 'range', 'move'))
    for entities in J1:       #on boucle le nombre de fois qu'une entité existe dans le clan désigné
        if 'state' in J1[entities]:       #si l'entité à un terme state
            
            # move should be much more likely
            if random.random() < .9:
                # move ship to a random location (one of the 8 possibilities)
                
                    locationx = J1[entities]['coox'] +random.randint(-1,1)
                    locationy = J1[entities]['cooy'] + random.randint(-1,1)
                    if 0 < locationx < int(map1[0])  and 0 < locationy < int(map1[1]):
                        orders += '%s:@%d-%d ' % (entities,locationx,locationy)

            else:
                # attack a random location (in range of the ship)
                locationx = J1[entities]['coox']+random.randint(1,7)
                locationy = J1[entities]['cooy']+random.randint(1,7)
                qtt = random.randint(10,40)
                orders += '%s:*%d-%d=%d ' % (entities,locationx,locationy,qtt)
            # do not forget to remove last space ' '

    orders += '.'

 
    
    return orders

def talk(group_1, type_1, group_2, type_2):
    """Make two players talk (demo of remote_play).
    
    Parameters
    ----------
    group_1: group id of the first player (int)
    type_1: type of the first player (str)
    group_2: group id of the second player (int)
    type_2: type of the second player (str)    
    
    
    Notes
    -----
    A player is either 'AI' or 'remote', there can be at most one remote player.
    
    If there is a referee, set group id to 0 for remote player.
    
    Each player will run until one of the players says "Stop".
    
    """
    
    # create connection
    if type_1 == 'remote':
        connection = remote_play.create_connection(group_2, group_1, verbose=True)
    if type_2 == 'remote':
        connection = remote_play.create_connection(group_1, group_2, verbose=True)

    # get player types
    types = {1:type_1, 2:type_2}

    # main loop (until one of both players says "stop")
    sentences = {1:'', 2:''}
    while sentences[1] != 'Stop' and sentences[2] != 'Stop':
        # get player sentences
        for player_id in (1, 2):
            # get player sentence
            if types[player_id] == 'AI':
                sentences[player_id] = get_AI_sentence()
            else:
                sentences[player_id] = remote_play.get_remote_orders(connection)

            # notify other player, if necessary
            if types[3-player_id] == 'remote':
                remote_play.notify_remote_orders(connection, sentences[player_id])
            

            
        # use player sentences
        for player_id in (1, 2):
            print('Player %d said "%s".' % (player_id, sentences[player_id]))
            



        # wait 3 seconds
        time.sleep(3)
        print('\n------------------------\n')   
    # close connection
    remote_play.close_connection(connection)






'''
if random.random() < .9:
        name = str(random.randint(1, 10000000))
        if random.random() < .05:
            orders += '%s:cruiser ' % name
        else:
            orders += '%s:tanker ' % name
        

    if random.random() < .05:
        orders += 'upgrade:%s ' % random.choice(('regeneration', 'storage', 'range', 'move'))
    for entities in J2:       
        if 'state' in J2[entities]:      
            

            if random.random() < .9:


                    locationx1 = J2[entities]['coox'] +random.randint(-1,1)
                    locationy1 = J2[entities]['cooy']+ random.randint(-1,1)
                    if 0 < locationx1 < int(map1[0])  and 0 < locationy1 < int(map1[1]):
                        orders += '%s:@%d-%d ' % (entities,locationx1,locationy1)

            else:

                locationx1 = J2[entities]['coox'] +random.randint(1,7)
                locationy1 = J2[entities]['coox'] +random.randint(1,7)
                qtt = random.randint(10,40)
                orders += '%s:*%d-%d=%d ' % (entities,locationx1,locationy1,qtt)
'''


