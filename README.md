# Projet_metro_L2

Le projet consiste à écrire un programme informatique permettant de déterminer le plus court itineéraire pour aller d’une station à une autre dans le métro Parisien. 

La plupart des donneées sont à récupérer dans le fichier “metro.txt”.
Ouvrir ce fichier, le regarder en détail, comprendre comment il est organisé. Pourquoi les sommets 7 et 8 sont-ils tous deux “Arts et Métiers” ?
Ce fichier date et certaines nouvelles stations sur des lignes qui ont été rallongées n’y figurent pas. Il ne parait pas nécessaire de les rajouter. Par contre, ce fichier est incomplet et il vous faudra rajouter des données qui n’y figurent pas comme les numéros de ligne de métro et les terminus des lignes.

Il est possible que le fichier metro.txt soit incomplet et que quelques rares liaisons y aient été omises. Votre premier travail de programmation doit donc consister à développer un module qui vérifie que votre graphe est bien connexe, c’est à dire qu’il est possible d’aller de n’importe quelle station à n’importe quelle autre. S’il s’avérait que des liaisons manquaient pour assurer cette connexité, à vous bien sur de les rajouter.

C’est là le principal objectif de votre travail. Il convient de permettre à un utilisateur d’indiquer une station de départ et une station d’arrivée et que votre programme calcule et indique le meilleur itinéraire pour aller de l’une à l’autre.

- Ajout créateur :
Etant donné les liens disponible dans le fichier metro.txt, les lignes possédant des boucles telle que la ligne 10 ne peuvent pas être représenté de manière correct. En effet, il existe par exemple un lien entre l'arret Javel et Mirabeau alors qu'il ne devrait pas exister. La fonction de plus court chemin retourne donc un trajet direct entre ces deux stations. Le projet suit donc à la lettre les liens du fichier 
metro.txt . Ils ne sont pas pour autant réaliste. 