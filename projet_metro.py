#-*- coding=utf-8 -*-
################################################################################
# Projet Sudoku (L2 Semestre 2)
# Matteo Rabache
################################################################################


##################################################
# Constantes/Variables

"""
Création de la couleur qui servira à dessiner
"""
noir =(0, 0, 0)
blanc = (255, 255, 255)
                    
                                             
lien_fichier = 'metro.txt'
with open(lien_fichier) as f:
    lines = f.readlines()

"""
Création du dictionnaire metroE de la forme : 'identifiant arret de metro : [[arrets que la clé dessert] , [poids correspondants au trajet]]'
Création du dictionnaire ID_metro de la forme : 'identifiant de l'arret : nom de l'arrêt'
Creation du dictionnaire Points_metro de la forme : 'identifiant arret de metro : [Cordoonnee X, Coordonnee Y]
"""

ID_metro = {}
metroE = {}

for i in lines :
    if i[0] == 'E' :
        metroE[int(i.split()[1])] = [[], []]                                #Initialise le dictionnaire metroE avec une matrice vide en valeur
        metroE[int(i.split()[2])] = [[], []]                                #et en clef l'identifiant (ID) du metro
for i in lines :
    if i[0] == 'V' :
        ID_metro[int(i[2:6])] = i[7:-1]

    elif i[0] == 'E' :
        metroE[int(i.split()[1])][0].append(int(i.split()[2]))
        metroE[int(i.split()[2])][0].append(int(i.split()[1]))
        metroE[int(i.split()[1])][1].append(int(i.split()[3]))
        metroE[int(i.split()[2])][1].append(int(i.split()[3]))



"""
Création de la liste liste_lien_metro qui permettra de construire chaque ligne de métro dans le dictionnaire dic_metro
"""

liste = []
for i in lines :                                
    if i[0] == 'E' :                            # initialise 'liste' avec l'ensemble des connections proposés dans metro.txt (numeros proposés devant la lettre E dans le fichier)
        liste.append(i[2:])                     # permet de retirer l'apparition de la lettre E dans la liste

liste_lien_metro_string = [elem[:len(elem)-2] for elem in liste]                # retire les temps de la liste l pour avoir une liste de la forme ['ID_station ID_station_suivante']
liste_lien_metro_string2 = [elem.split(" ") for elem in liste_lien_metro_string]                # sépare chaque ID_station connecté par une virgule dans une même liste
liste_lien_metro_complet = [[int(elem[0]),int(elem[1])]for elem in liste_lien_metro_string2]    # transpose les ID_station en de string à entier                       

i, precedent = 0, 0 
while liste_lien_metro_complet[i][0] >= precedent:                  # on récupère ici la variable i correspondant à l'indice à partir duquel on
    precedent = liste_lien_metro_complet[i][0]                      # atteint les liens qui concernent les mêmes stations
    i += 1                                                          # l'indice est trouvé dés que la liste suivante (de la matrice) commence par un ID_station inférieur au précédent
liste_lien_metro = liste_lien_metro_complet[:i]         # 'liste_lien_metro' = 'liste_lien_metro_complet' avec ces liens retirés 
                                                        # par exemple Châtelet correspond aux arrets 67 à 71  
                                                        # les liens entre les métros 67-68,67-69... sont retirés de la liste

pivot = []                                              # Constante utile dans le cas d'une ligne de métro contenant une boucle 


##################################################
# Fonctions

def verif_connexite():
    """
    Fonction qui vérifie la connexité entre chaque station proposé par le document metro.txt
    """
    stations = ligne([1],liste_lien_metro_complet)      # stations prend la valeur de la liste contenant chacun des liens depuis l'arret 1 avec la liste complète des liens de metro
    return len(stations) == 376                         # on vérifie qu'elle est bien égale au nb totale de station du document metro.txt


def ligne(liste,liste_lien=liste_lien_metro,cas=0):
    """ 
    Fonction récursive qui prend en compte une liste contenant une station, et la liste de lien sur laquelle l'appliqué et 
    renvoie une liste ordonné contenant chaque lien depuis cette station (sauf cas=1). 
    """
    if cas == 0:                                        # cas=0 correspond au cas général où on emploie la dernière station de 'liste' à chaque récursion
        station_prec = liste[-1]
    else:                                               # cas=1 correspond au cas où on récupère la première station de la liste à cahque fois
        station_prec = liste[0]                         # permet de récupérer l'ensemble des liens d'une seule et même station (utile dans la fonction 'exception_')

    for [elt1,elt2] in liste_lien:
        if elt2 == station_prec and elt1 not in set(liste):     # verifie que le lien elt1 repéré n'a pas déja été ajouté dans la liste
            liste.append(elt1)
            ligne(liste,liste_lien,cas)
        elif elt1 == station_prec and elt2 not in set(liste):   # verifie que le lien elt2 repéré n'a pas déja été ajouté dans la liste
            liste.append(elt2)
            ligne(liste,liste_lien,cas)
    return liste                                                # return 'liste' après que tous les liens aient été trouvé


def dijkstra(position, destination):
    """
    Fonction qui execute l'algorithme de Dijkstra qui donne le plus court chemin pour aller
    d'un arrêt de métro à un autre.
    """
    pos_nom = (list(ID_metro.keys())[list(ID_metro.values()).index(position)])                  #Variable retournant pour l'arrêt de métro où l'on se situe, son identifiant dans le fichier.txt
    destination_nom = (list(ID_metro.keys())[list(ID_metro.values()).index(destination)])       #Variable retournant pour l'arrêt de métro où l'on va, son identifiant dans le fichier.txt
    pere = {}                           #Dictionnaire qui contiendra pour chaque arrêt son père au cours de l'algorithme -> arrêt : père
    liste_sommets = []                  #Liste contenant tous les sommets du graphe
    arborescence = []                   #Liste qui contiendra l'arborescence finale du trajet
    liste_sommets_temp = []             #Liste modifiée à chaque tour de boucle qui contient la liste des sommets à étudier (on exploitera toujours le premier sommet de la liste)
    liste_sommets_visites = []          #Liste sommets qu'on visite plus
    poids_total = 0

#On place tous les sommets dans la liste 'sommets'
    for line in lines :
        if line[0] =='V' and int(line.split()[1]) not in liste_sommets:
            liste_sommets.append(int(line.split()[1]))

    poids = {}
    for i in liste_sommets :        #Pour chaque sommet du graphe :
        poids[i] = 0                #On initialise son poids à 0

    liste_sommets_temp.append(pos_nom)          #On ajoute dans la liste des sommets à visiter le sommet de départ
    for i in liste_sommets :                    #Pour chaque sommet i du graphe on fait :
        if i != liste_sommets_temp[0] and i in metroE[liste_sommets_temp[0]][0] :                       #Si le sommet est déjà en première position et qu'il est en destination du sommet qu'on étudie
            poids[liste_sommets_temp[0]] = 0    #On initialise le poids du sommet de départ à 0
            poids[i] = metroE[liste_sommets_temp[0]][1][metroE[liste_sommets_temp[0]][0].index(i)]      #Le poids du sommet i devient le poids entre le sommet i et le sommet de départ
            pere[i] = liste_sommets_temp[0]     #Le père de i devient alors le sommet de départ
            liste_sommets_temp.append(i)        #On ajoute alors le sommet i dans la liste de sommets à visiter
    del liste_sommets_temp[0]                   #A la fin de la boucle on supprime le sommet de départ de la liste de sommets à visiter car on ne le visitera plus
    liste_sommets_visites.append(pos_nom)       #On ajoute le sommet de départ dans la liste des sommets déjà visités

    while liste_sommets_temp != []:                             #Tant que la liste de sommets à visiter n'est pas vide le programme continue :
        poids_temp = [poids[i] for i in liste_sommets_temp]     #Récupere les poids correspondant aux sommets de la liste temporaire
        min_val = min(poids_temp)                               #Variable prenant le poids minimum dans la liste poids_temp
        min_cle = [k for k in poids if k in liste_sommets_temp and poids[k] == min_val]                                         #On récupère le sommet avec le poids minimum dans la liste de sommets à visiter dans une liste
        cle_min = min_cle[0]                                    #On met ce poids minimum dans une variable pour une utilisation plus simple
        liste_sommets_visites.append(cle_min)                   #On ajoute dans la liste de sommets visités le sommet avec le poids minimum car à la fin de la boucle nous ne l'utiliserons plus


        if cle_min in metroE :                                  #Si le sommet se trouve bien dans metroE -> Si il a bien au moins une station en destination :
            for i in liste_sommets :                            
                if i != pos_nom and i in metroE[cle_min][0] :   #Si le sommet i étudié est différent de la station de départ et qu'il est en destination du sommet que l'on visite :


                    if poids[i] != 0 and poids[i] < poids[cle_min] + metroE[cle_min][1][metroE[cle_min][0].index(i)]:       #Si le poids déjà existant est plus petit que celui proposé
                        pass                                #On laisse le poids déjà existant qui est donc le podis minimum
                    elif poids[i] != 0 and poids[i] > poids[cle_min] + metroE[cle_min][1][metroE[cle_min][0].index(i)]:     #Sinon si le poids déjà existant est supérieur à celui proposé
                        poids[i] = poids[cle_min] + metroE[cle_min][1][metroE[cle_min][0].index(i)]                         #Poids du sommet i étudié devient le poids du père de i + le poids entre le père et le sommet i étudié
                        pere[i] = cle_min                   #Le père du sommet i devient alors le sommet que l'on visite actuellement
                    elif poids[i] == 0 :                    #Sinon si le poids est toujours égal à 0 -> pas encore étudié
                        poids[i] = poids[cle_min] + metroE[cle_min][1][metroE[cle_min][0].index(i)]                         #Poids du sommet étudié devient le poids du pere + le poids entre pere et sommet étudié
                        pere[i] = cle_min                   #Le père du sommet i étudié devient le sommet que l'on visite actuellement

                    if i not in liste_sommets_visites and i not in liste_sommets_temp:      #Si ce sommet n'est pas dans la liste de sommets à visiter et qu'il n'a pas déjà été visité
                        liste_sommets_temp.append(i)                    #Alors on l'ajoute à laliste de sommets à visiter
        del liste_sommets_temp[liste_sommets_temp.index(cle_min)]       #Puis on supprime le sommet que l'on à visité à la liste des sommest à visiter

    arborescence.append(destination_nom)                #On ajoute d'abord à l'arborescence finale le sommet de destination
    while arborescence[-1] != pos_nom :                 #Tant que le dernier élément de l'arborescence n'est pas à la position de départ
        arborescence.append(pere[arborescence[-1]])     #On ajoute le sommet père du dernier élément ajouté
    arborescence.reverse()                              #Une fois que la liste est remplie, on l'inverse pour avoir l'arborescence dans le bon sens

    poids_total = poids[destination_nom]                #Variable de poids total contenant le poids de la destination 
    
    return arborescence, poids_total                    #Enfin, on retourne l'arborescence et le poids total obtenus


def pluriel(nb,string):
    """
    Fonction qui met au pluriel un mot si sa quantité est supérieur à 1.
    """
    if nb > 1:
        return '{} {}'.format(nb, string+'s')           # renvoie le mot au pluriel si son nombre est supérieur à 1          
    elif nb == 0:                                      
        return ''                                       # renvoie une chaîne de caractère vide si son nombre est égal à 0
    return '{} {}'.format(nb, string)                   # renvoie le mot si ni >= 1 ni = O
  

def duree(temps): 
    """
    Fonction qui conblancit une durée en seconde, en un temps en heure(s), minute(s), seconde(s). 
    Puis affiche ce temps.
    """
    min, sec = divmod(temps, 60)                        # conblancit le temps en minutes et secondes
    heure, min = divmod(min, 60)                        # conblancit les minutes en heures et minutes
    return '{} {} {}'.format(pluriel(heure,'heure'), pluriel(min,'minute'), pluriel(sec,'seconde'))


def nom(ID_arret):
    """
    Fonction qui renvoie le nom de la station à partir de son identifiant (ID).
    """
    for clef,val in ID_metro.items():                   # rappel : ID_metro est de la forme : 'nom de l'arret : identifiant de l'arret'
        if clef == ID_arret:
            return val


def terminus(metro,station,station_suivante):
    """
    Fonction qui renvoie le terminus associé à partir de la station actuelle et la suivante dans le métro concerné.
    """
    
    if dic_metro[metro][1] == dic_metro[metro][-1]:     # si l'élément à l'indice 1 dans dic_metro à la clef metro est égal au dernier élément du dictionnaire à la même clef 
        exception = 1                                   # il'agit d'une exception. On donne alors la valeur 1 à la variable exception
        liste_metro = dic_metro[metro][0]               # (permet de simplifier les indices dans la fonction)
    else:
        exception = 0                                   # exception prend la valeur 0 si il ne s'agit pas d'une exception
        liste_metro = dic_metro[metro]                  # (permet de simplifier les indices dans la fonction)

    if exception == 0:                                  # si il n'y a pas d'exception
        for i in range(len(liste_metro)-1):
            if station == liste_metro[i] and station_suivante == liste_metro[i+1]:          # si station correspond à un élément de la ligne liste_metro et station_suivante correspond à l'élément suivant 
                return nom(liste_metro[-1])                                                 # on retourne le dernier élément de la ligne liste_metro
        return nom(liste_metro[0])                                                          # si à la fin de la boucle cette condition n'a pas été validé on retourne le premier élément de la ligne liste_metro

    else:                                                                                   # si on a affaire à une exception 
        term2 = dic_metro[metro][1]                                                         # term2 prend la valeur de terminus selon la ligne de metro
        term = exception_(liste_metro,station,station_suivante,term2)           
        if type(term) == int:                                                               # si l'élément retourné est un terminus simple (un entier)
            return nom(term)                                                                # on return le nom de ce terminus
        else:                                                                               # si l'élément retourné est un terminus double (une liste de deux terminus) : cas de la fourchette
            return '{} / {}'.format(nom(term[0]),nom(term[1]))                              # on retourne alors les deux possibilités de terminus


def exception_(liste_metro,station,station_suivante,term2):
    global pivot
    """
    Cas où la ligne de métro correspond à une exception.
    Prends en ompte une ligne de métro, la station où l'on va et la station suivante, ainsi que le(s) terminus de la ligne. 
    """
    pivot.clear()
    if type(term2) == list:                                                     # cas où le terminus est une liste de deux terminus (fourchette)
        indice1 = liste_metro.index(term2[0])                                   # indice1 = indice dans liste_metro du premier terminus (de term2)
        pivot.append(lien(liste_metro[indice1+1],liste_metro[indice1+2]))          # pivot = station qui fait le lien entre les deux branches de terminus
        indice2 = liste_metro.index(pivot[0])                                      # indice2 = indice dans liste_metro du pivot

        liste_metro_1 = liste_metro[:indice1+1]                                 # liste_metro_1 correspond à une liste contenant les stations allant du terminus (unique) jusqu'au terminus de indice1
        liste_metro_0 = liste_metro[:indice2+1]                                 # liste_metro_0 correspond à une liste contenant les stations allant du terminus (unique) jusqu'au pivot (point commun des deux lignes)
        liste_metro_2 = liste_metro[:indice2+1] + liste_metro[indice1+1:]       # liste_metro_2 correspond à une liste contenant liste_metro_0 + les éléments non compris dans liste_metro_1

        if station in liste_metro_0 and station_suivante in liste_metro_0:      # dans le cas où la station, et la station suivante sont dans la liste_metro commune 
            for i in range(len(liste_metro_0)-1):                               
                if station == liste_metro_0[i] and station_suivante == liste_metro_0[i+1]:  
                    return term2                                                # retourne la liste contenant les deux terminus car le terminus n'a pas d'importance ici
            return liste_metro_0[0]                                             # reste de l'explication similaire au début de la fonction terminus

    else:                                                                       # cas où le terminus est un entier (boucle) 
        for elem in liste_metro:                                                # sépare les éléments de liste_metro
            if len(ligne([elem],cas=1)) == 4 or ( len(ligne([elem],cas=1)) == 3 and elem == term2 ):     # si la taille de la liste correspondant aux connections de elem est de 4,
                pivot.append(elem)                                                                                          # ou si la taille est de 3 et elem correspond au terminus, il s'agit d'un pivot

        indice1 = liste_metro.index(pivot[0])                                   # indice1 = indice dans liste_metro du premier pivot
        indice2 = liste_metro.index(pivot[1])                                   # indice2 = indice dans liste_metro du second pivot
        indice3 = liste_metro.index(term2)                                      # indice3 = indice dans liste_metro du terminus

        debut = liste_metro[:indice1+1]                                         # debut = ligne commune allant du premier teminus jusqu'au premier pivot
        boucle1 = [lien(liste_metro[i],liste_metro[i-1]) for i in range(indice1,indice2-1)]     # boucle1 est construit à partir des liens entre chaque arrêts compris entre indice1 et indice2 (inclus)
        fin = [liste_metro[indice2], liste_metro[indice3]]                                      # fin = liste correspondant au pivot et au terminus
        liste_metro_1 = debut + boucle1 + fin                                   # liste_metro_1 correspond au debut commun + une des deux boucles (celle dans le sens du parcours) + la fin commune 

        debut.reverse()                                                         # inverse le debut pour respecter le sens de la ligne
        boucle2 = [statio for statio in liste_metro if statio not in liste_metro_1]     # boucle2 est une liste construit à partir des éléments non commun à liste_metro_2 
        fin.reverse()                                                           # inverse la fin pour respecter le sens de la ligne
        liste_metro_2 = fin + boucle2 + debut                                   # liste_metro_2 correspond au debut commun + une des deux boucles (celle dans l'autre sens du parcours) + la fin commune 

    if station in liste_metro_1 and station_suivante in liste_metro_1:                              # vérifie que les deux stations consécutives sont sur la même ligne de métro
        for i in range(len(liste_metro_1)-1):                                                       # si station correspond à un élément de la ligne liste_metro et station_suivante correspond à l'élément suivant 
            if station == liste_metro_1[i] and station_suivante == liste_metro_1[i+1]:              # on retourne le dernier élément de la ligne liste_metro
                return liste_metro_1[-1]                                                            # si à la fin de la boucle cette condition n'a pas été validé on retourne le premier élément de la ligne liste_metro
        return liste_metro_1[0]                                                                     #
                                                                                                    # 
    elif station in liste_metro_2 and station_suivante in liste_metro_2:                            #
        for i in range(len(liste_metro_2)-1):                                                       #
            if station == liste_metro_2[i] and station_suivante == liste_metro_2[i+1]:              #
                return liste_metro_2[-1]                                                            #
        return liste_metro_2[0]                                                                     #


def lien(station,station_connecte):
    """
    Retourne un élément(une station) qui a un lien avec station mais qui ne correspond pas à une station qui y est déjà connecté (station_connecte).
    """
    for [elt1,elt2] in liste_lien_metro:
        if elt1 == station and elt2 != station_connecte:
            return elt2
        if elt2 == station and elt1 != station_connecte:
            return elt1

        

def affichage(liste_arret):
    global pivot
    """
    Fonction qui permet d'afficher la ligne à suivre et les changements de ligne (si il y en a).
    """
    l = []                                      # liste vide qui aura pour but de repérer si on change de ligne de metro

    for arret in liste_arret:                   # sépare les éléments contenu dans la liste des stations à parcourir (liste_arret)

        if arret != liste_arret[-1]:            # si l'arret ne correspond pas à la dernière station (la destination) de liste_arret (pour éviter les out of range)
            i = liste_arret.index(arret)+1      # i prend la valeur de l'indice correspondant à l'arrêt suivant dans liste_arret
            indice_debut = i
            if nom(arret) == nom(liste_arret[i]):       # si le nom de l'arret correspond à celui du suivant on passe directement à l'arret suivant
                continue                                # par exemple: pour éviter d'avoir à anlyser 67 et 68 qui correspondent tous deux à Chatelet
        if nom(arret) == nom(liste_arret[-1]):  # si le nom de l'arret analysé correspond à celui de la destination alors on sort de la boucle 
            break                               # pour éviter de proposer  un changement de ligne à l'utilisateur alors qu'il a atteint sa destination

        for metro, info in dic_metro.items():
            if dic_metro[metro][1] == dic_metro[metro][-1]:     # si l'élément à l'indice 1 dans dic_metro à la clef metro est égal au dernier élément du dictionnaire à la même clef, il s'agit d'une exception
                liste_m = info[0]                               # liste_m correspond à la ligne de metro (obtenu dans dic_metro à l'indice 0 du métro associé)
            else: 
                liste_m = info                      

            if arret in liste_m and l == []:                # si l'arret est toujours dans la même ligne de métro et si il n'y a pas encore de métro dans l
                while liste_arret[i] != liste_arret[-1] and liste_arret[i] in liste_m:
                    i += 1                                  # permet de modifier i pour récupérer l'indice du dernier arret de cette même ligne de métro et indiqué directement la direction
                if liste_arret[i] == liste_arret[-1]:       # dans le cas où le dernier élément de liste_arret est celui a utilisé dans les autres fonctions 
                    i+=1                                    # il faut ajouter +1 à l'indice pour pouvoir l'employer en tant que station_suivante dans la fonction terminus
                
                if terminus(metro,liste_arret[indice_debut-1],liste_arret[indice_debut]) != terminus(metro,liste_arret[i-2],liste_arret[i-1]):              # Si le terminus des deux premiers arrêts est différent  
                                                                                                                                                            # de celui des deux derniers arrêts de liste_arret (cas d'une boucle)
                    print('Prenez la ligne', metro, 'direction', terminus(metro,liste_arret[indice_debut-1],liste_arret[indice_debut]))
                    for elem in liste_arret:
                        for piv in pivot:
                            if elem == piv:                                                             # alors on récupère le bon pivot (celui dans liste_arret)
                                etape = elem 
                    print('Puis prenez la ligne dans le sens inverse à', nom(etape))                    # on indique alors un changement de direction au sein d'une même ligne
                    l.append(metro)
                    continue                                                                            # permet de passer directement à l'arret suivant

                print('Prenez la ligne', metro, 'direction', terminus(metro,liste_arret[i-2],liste_arret[i-1]))  # première phrase à indiquer à l'utilisateur
                l.append(metro)

            elif arret in liste_m and metro not in l:       # permet d'éviter d'analyser tous les arrets appartenant à une ligne de métro déjà vu
                while liste_arret[i] != liste_arret[-1] and liste_arret[i] in liste_m:
                    i += 1
                if liste_arret[i] == liste_arret[-1]:    
                    i+=1    

                if terminus(metro,liste_arret[indice_debut-1],liste_arret[indice_debut]) != terminus(metro,liste_arret[i-2],liste_arret[i-1]):

                    print('A', nom(arret), 'changez et prenez la ligne', metro, ', direction', terminus(metro,liste_arret[indice_debut-1],liste_arret[indice_debut]))
                    for elem in liste_arret:
                        for piv in pivot:
                            if elem == piv:
                                etape = elem 
                                print('Puis prenez la ligne dans le sens inverse à', nom(etape))
                    l.append(metro)
                    continue

                print('A', nom(arret), 'changez et prenez la ligne', metro, ', direction', terminus(metro,liste_arret[i-2],liste_arret[i-1]))
                l.append(metro)


def chemin():
    """
    Fonction principal du programme. Elle lance toutes les fonctions à la suite pour obtenir le meilleur 
    trajet à partir de la position et la destination de l'utilisateur. Elle indique ensuite le chemin à suivre.
    """
    destination = input('A quel arrêt de métro souhaitez-vous allez ? (Nom de la station de métro)\n')
    while destination not in ID_metro.values() :
        print('Veuillez choisir une station de métro valide')
        destination = input('A quel arrêt de métro souhaitez-vous allez ? (Nom de la station de métro)\n')

    position = input('Quel est votre position ? (Nom de la station de métro)\n')
    while position not in ID_metro.values() :
        print('Veuillez choisir une station de métro valide')
        position = input('Quel est votre position ? (Nom de la station de métro)\n')

    print()                                                                 # Créer un espace pour mieux différencier la création des variables et le chemin à prendre

    if position == destination:                                             # Cas où l'utilisateur indique le même arrêt pour la destination et la position
        print('Vous êtes arrivé à destination !')

    else:   
        liste_arret, temps = dijkstra(position, destination)
        print('Vous êtes à', position)
        affichage(liste_arret)

        t = duree(temps)
        while t[0] == ' ':                                                      # Permet de retirer les espaces dans l'affichage dans le cas où le temps n'est qu'en seconde
            t = t[1:]
        print('Vous devriez arriver à', destination, 'dans', t)
 

##################################################
# Constante (qui nécessite une fonction)

"""
Création dictionnaire dic_metro contenant chaque ligne de métro de la forme : 'métro : liste de métro, terminus opposé (si exception)'
Une exception est affilée aux lignes possédant une boucle (terminus=int) ou une fourchette aux terminus (terminus=list contenant les deux terminus opposé au premier) 
"""

dic_metro = {
'1' : ( ligne([130]) ),                 # 130 : Grande Arche de la Défense = terminus ligne 1

'2' : ( ligne([256]) ),                 # 256 : Porte Dauphine = terminus ligne 2

'3' : ( ligne([251]) ),                 # 251 : Pont de Levallois, Bécon = terminus ligne 3

'3bis': ( ligne([116]) ),               # 116 : Gambetta = terminus ligne 3bis

'4' : ( ligne([268]) ),                 # 268 : Porte de Clignancourt = terminus ligne 4

'5' : ( ligne([28]) ),                  # 28 : Bobigny, Pablo Picasso = terminus ligne 5

'6' : ( ligne([57]) ),                  # 57 : Charles de Gaulle, Étoile = terminus ligne 6

'7' : (ligne([152]), [363,179]),        # 152 : La Courneuve, 8 Mai 1945 = terminus ligne 7
                                        # 363 : Villejuif, Louis Aragon = 3e terminus ligne 7
                                        # 179 : Mairie d'Ivry = 2e terminus ligne 7

'7bis' : (ligne([170]), 280),           # 170 : Louis Blanc = terminus ligne 7bis
                                        # 280 : Pré-Saint-Gervais = terminus ligne 7bis

'8' : ( ligne([240]) ),                 # 240 : Place Balard = terminus ligne 8

'9' : ( ligne([253]) ),                 # 253 : Pont de Sevres = terminus ligne 9

'10' : (ligne([117]), 37),              # 117 : Gare d'Austerlitz = terminus ligne 10
                                        # 37 : Boulogne, Pont de Saint-Cloud, Rond Point Rhin et Danube = terminus ligne 10


'11' : ( ligne([183]) ),                # 183 : Mairie des Lilas = terminus ligne 11

'12' : ( ligne([178]) ),                # 178 : Mairie d'Issy = terminus ligne 12 

'13' : (ligne([72]), [112,319]),        # 72 : Châtillon-Montrouge = terminus ligne 13
                                        # 112 : Gabriel Péri, Asnières-Gennevilliers = 3e terminus ligne 13
                                        # 319 : Saint-Denis-Université = 2e terminus ligne 13

'14' : ( ligne([24]) ),                 # 24 : Bibliothèque François Mitterand = terminus ligne 14
}



##################################################
# Lancement

if verif_connexite():
    chemin()