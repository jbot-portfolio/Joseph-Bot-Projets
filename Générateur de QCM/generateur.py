# PROGRAMMÉ PAR JOSEPH BOT #
#--------------------------#

#Importation du module pickle
import pickle
import time
import os

#Stock des codes de traitement de texte dans des variables pour faciliter leur utilisation
b = '\33[1m' #gras
s = '\33[4m' #souligné
i = '\33[3m' #italic
n = '\33[0m' #normal
r = '\33[31m' #rouge
v = '\33[92m' #vert

#Fonction permettant de créer des QCM
def CreerQcm():
    """ Fonction permettant de créer un QCM et l'enregistrer """
    # Création d'un dictionnaire qui va contenir les dictionnaires qu'on créera ci-dessous afin de les enregistrer.
    qcm = []
    nom = input(str(f"{b}Saisir le nom de votre QCM:{n} "))
    nom = nom + '.txt'
    Fichier = open(nom, 'wb')
    nQuestion = input(str(f'\n{b}{s}Nouvelle Question ?{n} (O/N)\n{b}> {n}')).upper()

    #On repose la question tant que la réponse est autre que O ou N
    while nQuestion != 'O': 
        if nQuestion == 'N':
            print(f"{r}{b}Erreur{n}{r}, le QCM doit avoir au moins une question !{n}")
            nQuestion = input(str(f'\n{b}{s}Nouvelle Question ?{n} (O/N)\n{b}> {n}')).upper()
        else:
            print(f"{r}{b}Erreur{n}{r}, vous n'avez pas entré un choix valide !{n}")
            nQuestion = input(str(f'\n{b}{s}Nouvelle Question ?{n} (O/N)\n{b}> {n}')).upper()

    while nQuestion == 'O': #Tant que l'utilisateur continue de rajouter des questions
            question = input(f'\n{i}Saisir votre question : ')
            rCorrect = input('Saisir la réponse correcte : ')
            rIncorrect = input('Saisir la réponse incorrecte : ')
            qcm.append({'question':question, 'exacte':rCorrect,'inexacte':rIncorrect}) #Enregistrement de la question & des réponses

            nQuestion = input(str(f'\n{b}{s}Nouvelle Question ?{n} (O/N)\n{b}> {n}'))
            while nQuestion != 'O' and nQuestion != 'N': #On redemande, tant que la réponse est autre que O ou N
                print(f"{r}{b}Erreur{n}{r}, vous n'avez pas entré un choix valide !{n}")
                nQuestion = input(str(f'\n{b}{s}Nouvelle Question ?{n} (O/N)\n{b}> {n}')).upper()

    #Enregistrement du dictionnaire dans un fichier
    pickle.dump(qcm, Fichier)  #Serialisation
    Fichier.close()


#CreerQcm()

def lectureQcm(nom_fichier):
    """
    Fonction prenant en argument un QCM sous la forme ".txt"
    Lance le QCM
    """
    Fichier = open(nom_fichier,"rb")
    Fichier_ouvert = pickle.load(Fichier) #Déserialisation

    #On appelle les fonctions "interrogation" et "questionnaire" du script "gestion_qcm.py"
    from gestionQcm import interrogation, questionnaire

    #On démarre le QCM enregistré
    return questionnaire(Fichier_ouvert)


#lecture_qcm('nom.txt)

def menuQCM(QCMs):
    """ Menu de gestion des QCMs """

    print(f"\n{b}1>{n} Lancer un QCM")
    print(f"{b}2>{n} Supprimer un QCM")
    print(f"{b}3>{n} Retour au menu principal\n")

    #On demande a l'utilisateur de choisir
    choixQCMsaved = input(f"{b}Que voulez-vous faire ?\n{b}> {n}")
    while choixQCMsaved != "1" and choixQCMsaved != "2" and choixQCMsaved != "3": #Tant que la réponse est incorrecte on redemande
        time.sleep(0.25)
        print(f"{r}{b}\nErreur{n}{r}, vous n'avez pas entré un choix valide !{n}")
        choixQCMsaved = input(f"{b}Que voulez-vous faire ?\n{b}> {n}")

    if choixQCMsaved == '1': #Lancer un QCM
        choixQCM = input(str(f"{b}Quel QCM voulez-vous lancer ? \n> {n}"))
        #On redemande a l'utilisateur le QCM si celui donné n'existe pas
        while choixQCM not in QCMs:
                time.sleep(0.25)
                print(f"{r}{b}Erreur{n}{r}, ce QCM n'existe pas ! Veuillez reéssayer :{n}\n")
                choixQCM = input(str(f"{b}Quel QCM voulez-vous lancer ? \n> {n}"))

        choixQCM = choixQCM + '.txt'
        lectureQcm(choixQCM)
        time.sleep(0.5)
        print("\nRetour au menu principal..")
        time.sleep(1)
        return menu()

    elif choixQCMsaved == '2': #Supprime un QCM
        choixQCMsuppr = input(str(f"{b}Quel QCM voulez-vous supprimer ? \n> {n}"))
        #On redemande a l'utilisateur le QCM si celui donné n'existe pas
        while choixQCMsuppr not in QCMs:
                time.sleep(0.25)
                print(f"{r}{b}Erreur{n}{r}, ce QCM n'existe pas ! Veuillez reéssayer :{n}\n")
                choixQCMsuppr = input(str(f"{b}Quel QCM voulez-vous supprimer ? \n> {n}"))

        choixQCMsuppr = choixQCMsuppr + '.txt'
        os.remove(choixQCMsuppr)
        time.sleep(1)
        print(f"\n{r}{b}QCM supprimé !{n}\n")
        time.sleep(0.5)
        return menuQCM(QCMs)

    else: #Retour au main menu
        time.sleep(0.5)
        print("\nRetour au menu principal..")
        time.sleep(1)
        return menu()

def menu():
    """
    Fonction permettant de voir et de selectionner les différents QCM crées
    """

    #On récupère tous les fichiers situés à la racine du fichier .py donc là ou sont les QCM enregistrés
    QCMsaved = []
    from os import walk
    for dirpath, dirnames, filesname in walk('generateur.py\..'):
        for filesname in filesname:
            if filesname.endswith('.txt'):
                QCMsaved.append(filesname[:len(filesname)-4]) #On enlève les 4 derniers charactères des noms des QCM pour enlever le '.txt'

    print(f"{b}\n---------------------------------------------------------------------------------")
    print("|                               Générateur de QCM                               |")
    print(f"---------------------------------------------------------------------------------")
    print(f"Bonjour, que souhaitez-vous faire ?\n\n1>{n}{i} Créer un QCM\n{n}{b}2>{n}{i} Voir mes QCM enregistrés\n{n}{b}3>{n}{i} Faire un QCM{n}\n")
    choix = input(f"{b}Votre choix : {n}")
    
    if choix == '1':
        CreerQcm()
        print(f"\n{b}{v}QCM enregistré avec succès !{n}")
        time.sleep(0.75)
        print(f"{s}Redirection vers le menu principal..{n}")
        time.sleep(1.25)
        return menu()

    elif choix == '3':
        selectQCM = input(str("Quel QCM voulez-vous faire ? \n> "))

        #On redemande a l'utilisateur le QCM si celui donné n'existe pas
        while selectQCM not in QCMsaved:
                time.sleep(0.5)
                print(f"{r}{b}Erreur{n}{r}, ce QCM n'existe pas ! Veuillez reéssayer :{n}\n")
                selectQCM = input(str("Quel QCM voulez-vous faire ? \n> "))

        selectQCM = selectQCM + '.txt'
        lectureQcm(selectQCM)
        time.sleep(0.5)
        print("\nRetour au menu principal..")
        time.sleep(1)
        return menu()

    elif choix == '2':
        print(f"\n{b}{s}Voici tous vos QCM enregistrés :{n}")
        #On affiche les QCMs
        for elmt in QCMsaved:
            print(f"{n}{b}>{n}{i}", elmt)
        menuQCM(QCMsaved)

    else: #Si l'utilisateur n'a pas entré un choix valide, on relance le menu
        time.sleep(0.5)
        print(f"{r}{b}Erreur{n}{r}, vous n'avez pas entré un choix valide !{n}")
        return menu()
menu()