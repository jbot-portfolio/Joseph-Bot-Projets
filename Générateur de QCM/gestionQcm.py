# PROGRAMMÉ PAR JOSEPH BOT #
#--------------------------#

#Importation du module random
from random import*

b = '\33[1m' #gras
s = '\33[4m' #souligné
i = '\33[3m' #italic
n = '\33[0m' #normal
r = '\33[31m' #rouge
v = '\33[92m' #vert

#Dictionnaire pour stocker le score
score = 0

def interrogation(q,nbr):
    global score
    """
    Recoit en entrée une liste de dictionnaire (le qcm) et un entier (choix de la question)
    Cette fonction | affiche la question,
                   | affiche les 2 propositions aléatoirement,
                   | lit la réponse de l’utilisateur,
                   | affiche 'Bonne réponse' ou 'Mauvaise réponse'
    """
    r = randint(0, 1)
    print(f"{b}{q[nbr]['question']}")
    #Affichage des deux propositions aléatoirement
    if r == 0:
        print(f"1> {n}{q[nbr]['exacte']}{b}")
        print(f"2> {n}{q[nbr]['inexacte']}{b}")
        reponse = input(f"\n{i}Entrez votre réponse : {n}{b}") #Récupération de la réponse de l'utilisateur
        if reponse == '1':
            print(f"{v}Bonne réponse ! {n}(+2 pts)")
            score += 2
        else:
            print(f"{r}Mauvaise réponse ! {n}(-1 pts)")
            score -= 1
    else:
        print(f"1> {n}{q[nbr]['inexacte']}{b}")
        print(f"2> {n}{q[nbr]['exacte']}{b}")
        reponse = input(f"\n{i}Entrez votre réponse : {n}{b}") #Récupération de la réponse de l'utilisateur
        if reponse == '2':
            print(f"{v}Bonne réponse ! {n}(+2 pts)")
            score += 2
        else:
            print(f"{r}Mauvaise réponse ! {n}(-1 pts)")
            score -= 1

def questionnaire(q,i=0):
    global score
    #On importe l'instruction 'shuffle' du module random afin de mélanger le numero des questions de la liste 'questions'
    from random import shuffle
    questions = []
    for qcm in range(len(q)):
        questions.append(qcm)
    shuffle(questions)
    stock = [] #Liste 'stock' stockant les réponses de l'utilisateur
    #On affiche le QCM en entier
    if i == 0:
        for i in range(len(q)):
            choix = choice(questions) #On choisi une question au hasard dans la liste 'questions'
            print(f"\n{s}{b}Question {i+1}:{n}\n")
            interrogation(q, choix)
            stock.append(q[choix]['exacte']) #On ajoute la réponse de l'utilisateur à la liste 'stock'
            questions.remove(choix) #On supprime la question 'choix' qui vient d'être choisie au hasard dans la liste 'questions'
    #On affiche qu'une seule question
    else:
        print(f"\n{s}{b}Question {i + 1}:{n}\n")
        interrogation(q, i)
        stock.append(q[i]['exacte']) #On ajoute la réponse de l'utilisateur à la liste 'stock'
    print(f"{b}{s}\nFin du questionnaire.{n}")

    #Affichage du score
    if score < 0: #On fait en sorte que le score soit toujours positif
        score = 0
    print(f"{b}Votre score est de {score}/{len(q)*2} !")
    score = 0
