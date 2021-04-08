# PROGRAMMÉ PAR JOSEPH BOT #
#--------------------------#

from random import*
import time

personnages = ["11Petyr Baelish", "12Varys", "21Ned Stark", "22Robert Baratheon", "31Joffrey", "32Tyrion", "41Le Limier", "42La Montagne", "51Daenerys", "52Joras Mormont", "61Tormund", "62Jon Snow", 
"71Syrio Forel", "72Jaqen H'ghar", "81Olenna Tyrell", "82Tywin Lannister", "91Cercei Lannister", "92Jaime Lannister", "a1Sammuel Tarly", "a2Ramsey", "b1Euron Greygoy", "b2Oberyn", "c1Bronn", "c2Brienne de Torth"]
personnagesJoues = []
personnagesMorts = []

P1, P2, P3 = "", "", ""

alliances = 100

#Definition du tableau contenant les infos des joueurs
infoPerso = [[personnages[x]] for x in range(len(personnages))]
for i in range(len(infoPerso)):
      infoPerso[i].append(0) #Kills
      infoPerso[i].append(0) #JoursAvantFaim
      infoPerso[i].append(0) #JoursAvantSoif
      infoPerso[i].append(0) #JoursAvantMortBlessé
      infoPerso[i].append(False) #Faim
      infoPerso[i].append(False) #Soif
      infoPerso[i].append(False) #Blessé
      infoPerso[i].append(False) #Armé
      infoPerso[i].append(i) #Team

actionsKill = [ "à tué",
                "à décapité",
                "à poignardé dans le dos",
                "à tiré une flêche dans le dos de",
                "à abattu",
                "à poussé",
                "à tué" ]
actionsKill2ePart = ["",
                     "avec une épée",
                     "avec sa dague",
                     "",
                     "", 
                     "du haut d'une fallaise", 
                     "d'un trait d'arbalète"]
actionsKillInverse =  ["à été tué par",
                      "s'est fait abattre par",
                      "à été poignardé dans le dos par",
                      "s'est fait décapité par",
                      "s'est fait abattre d'un trait d'arbalète par",
                      "à été poussé du haut du falaise par"]
actionsKillInverse2ePart = ["", 
                           "", 
                           "avec sa dague", 
                           "avec une épée", 
                           "",
                           ""]
actionsBlesse = ["à blessé",
                 "à blessé",
                 "à blessé",
                 "à planté",
                 "à planté",
                 "à blessé gravement" ]
actionsBlesse2ePart = ["en lui tirant une flêche dessus.",
                       "en le poignardant pendant qu'il avait le dos tourné.",
                       "en lui jetant un couteau dans le dos.",
                       "avec une lance et le blesse gravement.",
                       "avec une épée mais il arrive à s'enfuir.", 
                       "mais le laisse partir."]
actionsKill3Perso = [ "ont tué", 
                      "ont abattu" ]
actionsKill3Perso1vs2 = ["à tué", 
                         "à abattu"]

actions = [ "est affamé.",
            "à très faim.",
            "à soif.", 
            "est assoiffé.",
            "à trouvé de l'eau.",
            "chasse pour se nourrir.",
            "grimpe dans un arbre pour mieux voir les alentours.",
            "à trouvé une grotte et décide de l'explorer."
            "se cache dans une caverne.",
            "se cache dans un arbre." ]
actionSponsor = [ "reçois de l'eau d'un sponsor.",
                  "reçois de la nourriture d'un sponsor.",
                  "reçois une arme d'un sponsor.",
                  "reçois du soin d'un sponsor." ]
actionsMortNaturelle = ["meurt de faim.", 
                        "meurt de soif.", 
                        "meurt de déshydratation.",  
                        "explore une grotte mais celle-ci s'effondre malheureusement sur lui.",
                        "meurt tué par la zone.", 
                        "glisse d'une fallaise et s'écrase au sol.", 
                        "meurt d'empoisonement après avoir mangé des baies.",
                        "se fait manger par des loups" ]
actionsMortBlessure = [ "meurt de ses blessures.", 
                        "succombe a ses blessures.", 
                        "se vide de son sang et meurt a cause de ses blessures." ]

actionsPersosBlessesSAC = ["essaye de se soigner avec des bandages qu'il avait récupéré à la corne d'abondance.",
                            "soigne ses blessures avec un kit de soin qu'il avait récupéré à la corne d'abondance."]

actionsPersosBlesses = ["Essaye de se soigner comme il peut",
                        "Se fabrique un bandage avec un morceau de son t-shirt",
                        "Se soigne avec des herbes médicinales"] 


#Actions Alliances
actionsAlliances2Perso = [ "et", 
                           "s'est allié avec", 
                           "et", 
                           "à fait alliance avec" ]
actionsAlliances2Perso2ePart = [ "ont fait alliance.", 
                                 "", 
                                 "se sont alliés.", 
                                 "" ]

actionsAlliances3Perso1erPart = [ ", ", 
                                  ", ", 
                                  " et ", 
                                  " et " ]
actionsAlliances3Perso = [ "et", 
                           "et", 
                           "se sont alliés avec", 
                           "ont décidé de faire alliance avec" ]
actionsAlliances3Perso2ePart = [ "ont fait alliance.", 
                                 "se sont alliés.", 
                                 "", 
                                 "" ]

stockActionsAlliances2Perso = [""]
stockActionsAlliances3Perso = [""]



#CORNE D'ABONDANCE :
actionCombatCornucopia = ["court à la corne d'abondance mais", 
                          "court vers la corne d'abondance mais ce fait poignarder dans le dos par", 
                          "court à la corne d'abondance mais ce prend un couteau de lancé dans le dos par", 
                          "cours vers la corne d'abondance mais hésite et ce fait tué par"]
actionCombatCornucopia2ePart = ["arrive avant lui et le plante avec une lance.", 
                                "pendant qu'il s'équipe.",
                                "après s'être enfui avec de l'équipement",
                                "pendant qu'il essayait de fuir."]
stockActionsCombatCornucopia = [""]
actionBlesseCornucopia = ["blesse gravement", 
                          "blesse", ]
actionBlesseCornucopia2ePart = ["en lui tirant une flêche dans le dos pendant qu'il s'enfuiait de la corne d'abondance.", 
                                "en lui tirant une flêche dans le pied pendant qu'il s'enfuiait" ]
actionBlesseCornucopiaSAC = ["blesse",
                             "se bat pour un sac avec"]
actionBlesseCornucopiaSAC2ePart = ["en se battant avec lui pour un sac.",
                                   "et l'emporte en le blessant gravement."]
stockActionsBlesseCornucopia = [""]
stockActionsBlesseCornucopiaSAC = [""]
actionKillCornucopia = ["court vers la corne d'abondance et tue", 
                        "court à la corne d'abondance, prend un arc et tire une flêche dans le dos de", 
                        "court vers la corne d'abondance et tue"]
actionKillCornucopia2ePart = ["avec une lance.", 
                              "qui essayait de s'enfuir après avoir pris une arme.", 
                              "avec des couteaux de lancer."]
stockActionsKillCornucopia = [""]
actionFuiteCornucopia = ["court a l'opposé de la corne d'abondance et s'engoufre dans la forêt.", 
                         "s'enfuit de la corne d'abondance mais n'arrive malheureusement pas a attraper de sac."]
actionFuiteCornucopiaSAC = ["s'enfuit de la corne d'abondance et prend un sac au passage.", 
                            "court vers la forêt en prenant un sac.", ]
stockActionsFuiteCornucopia = [""]
stockActionsFuiteCornucopiaSAC = [""]
actionFuiteCornucopiaMort = ["s'enfuit de la corne d'abondance mais explose en déclanchant une mine."]

stockActionsKill3Perso = [""]
stockActionsKill3Perso1vs2 = [""]
stockActionsKill = [""]
stockActionsKillInverse = [""]
stockActionsBlesse = [""]
stockActionsMortNaturelle = [""]
stockActionsMortBlessure = [""]
stockActions = [""]
stockActionsPersosBlesses = [""]
stockActionsPersosBlessesSAC = [""]
stockSponsor = [""]

persoBlesse = []
persoArme = []
persoCornBag = []

rngPerso = 0
rngPerso2 = 0
rngPerso3 = 0
rngInfoPerso = 0
rngActions = 0
rngActionsPersosBlesses = 0
rngActionsPersosBlessesSAC = 0
rngActionsKill = 0
rngActionsKillInverse = 0
rngActionsKill3Perso = 0
rngActionsKill3Perso1vs2 = 0
rngActionsBlesse = 0
rngActionMortNaturelle = 0
rngActionMortAuto = 0
rngActionMortBlessure = 0
rngSponsor = 0
rngActionAlliance2Perso = 0
rngActionAlliance3Perso = 0

repartition = 0
repartitionKill = 0
repartitionRecoiSoin = 0
repartitionAlly = 0

#Corne d'abondance
rngActionCombatCornucopia = 0
rngActionBlesseCornucopia = 0
rngActionBlesseCornucopiaSAC = 0
rngActionKillCornucopia = 0
rngActionFuiteCornucopia = 0
rngActionFuiteCornucopiaSAC = 0
rngActionFuiteCornucopiaMort = 0

#Pourcentages corne d'abondance
rep = 9
rep1 = 18
rep2 = 30
rep3 = 96
rep4 = 101

repAlly = 26
repAlly3P = 9

persoDejaBlesse = False
days = 0
kills = 0
nbrPerso = len(personnages) - 1
persoGagne = False
nbrPersoBlesse = 0
repArme = 0

P1Team = 0
P2Team = -1

def randomChoice():
      global repartition, P1, P2, P3, repartitionKill, rngActions, rngActionsPersosBlesses, rngActionsPersosBlessesSAC, rngActionsKill, rngActionsKillInverse,rngActionsKill3Perso, rngPerso, rngPerso2, rngPerso3, rngSponsor, rngActionsBlesse, rngActionCombatCornucopia, rngActionFuiteCornucopia, rngActionFuiteCornucopiaSAC, rngActionKillCornucopia, rngActionBlesseCornucopia, rngActionBlesseCornucopiaSAC, rngActionFuiteCornucopiaMort, rngActionMortNaturelle, rngActionMortAuto, rngActionMortBlessure, repartitionAlly, rngActionAlliance2Perso, rngActionAlliance3Perso, rngActionsKill3Perso1vs2, rngInfoPerso

      rngInfoPerso = randint(0, nbrPerso)

      P1 = personnages[randint(0, len(personnages) - 1)]
      P2 = personnages[randint(0, len(personnages) - 1)]
      P3 = personnages[randint(0, len(personnages) - 1)]

      rngActions = randint(0, len(actions) - 1)
      rngActionsPersosBlesses = randint(0, len(actionsPersosBlesses) - 1)
      rngActionsPersosBlessesSAC = randint(0, len(actionsPersosBlessesSAC) - 1)
      rngActionsKill = randint(0, len(actionsKill) - 1)
      rngActionsKillInverse = randint(0, len(actionsKillInverse) - 1)
      rngActionsKill3Perso = randint(0, len(actionsKill3Perso) - 1)
      rngActionsKill3Perso1vs2 = randint(0, len(actionsKill3Perso1vs2) - 1)
      rngActionsBlesse = randint(0, len(actionsBlesse) - 1)
      rngActionMortNaturelle = randint(0, len(actionsMortNaturelle) - 1)
      rngActionMortBlessure = randint(0, len(actionsMortBlessure) - 1)
      rngActionAlliance2Perso = randint(0, len(actionsAlliances2Perso) - 1)
      rngActionAlliance3Perso = randint(0, len(actionsAlliances3Perso) - 1)
      
      repartition = randint(0, 100)
      repartitionKill = randint(0, 100)
      repartitionRecoiSoin = randint(0, 100)
      repartitionAlly = randint(0, 100)

      #Corne d'abondance : 
      rngActionCombatCornucopia = randint(0, len(actionCombatCornucopia) - 1)
      rngActionBlesseCornucopia = randint(0, len(actionBlesseCornucopia) - 1)
      rngActionBlesseCornucopiaSAC = randint(0, len(actionBlesseCornucopia) - 1)
      rngActionKillCornucopia = randint(0, len(actionKillCornucopia) - 1)
      rngActionFuiteCornucopia = randint(0, len(actionFuiteCornucopia) - 1)
      rngActionFuiteCornucopiaSAC = randint(0, len(actionFuiteCornucopia) - 1)
      rngActionFuiteCornucopiaMort = randint(0, len(actionFuiteCornucopiaMort) - 1)

def checkSameActions():
      while actionsKill[rngActionsKill] == stockActionsKill[-1] or actionsKill3Perso[rngActionsKill3Perso] == stockActionsKill3Perso[-1]:
            randomChoice()

def ajouteNbrStatus(nK, s, perso):
      global infoPerso
      for x in range(len(infoPerso)):
            if infoPerso[x][0] == perso:
                  infoPerso[x][s] += nK

def ajouteStatusPerso(s, status, perso):
      global infoPerso
      for x in range(len(infoPerso)):
            if infoPerso[x][0] == perso:
                  infoPerso[x][s] = status

def killBlesse():
      global P2
      if len(persoBlesse) >= 1 and repartitionKill > 75:
            shuffle(persoBlesse)
            for p in persoBlesse:
                  for x in range(len(infoPerso)):
                        if infoPerso[x][0] == p and p in personnages and p != P1:
                              P2 = p
                              break

def killForSponsor():
      global rep, rep1, rep2, rep3, rep4
      for x in range(len(infoPerso)):
            if infoPerso[x][0] == P1:
                  rep += (infoPerso[x][1]*0.25)
                  rep1 += (infoPerso[x][1]*0.67)
                  rep2 += (infoPerso[x][1]*0.7)
                  rep3 += (infoPerso[x][1]*0.36)
                  rep4 -= (infoPerso[x][1]*2.2)

def progressionJoursRepartition():
      global rep, rep1, rep2, rep3, rep4
      rep += (days*0.5)
      rep1 += (days*1)
      rep2 += (days*0.85)
      rep3 += (days*0.70)
      rep4 -= (days*1)

def ajoutePersoArme(perso):
      global repArme, persoArme
      repArme = randint(0,100)
      if repArme > 30:
            persoArme.append(perso)
            ajouteStatusPerso(8, True, perso)

def supprimePersoBlesse(perso):
      global persoBlesse
      for x in range(len(infoPerso)):
            if infoPerso[x][0] == perso and perso in persoBlesse:
                  persoBlesse.remove(perso)

def addAlliance(perso, perso2, perso3, cbPerso):
      global infoPerso, alliances
      for i in range(len(infoPerso)):
            if infoPerso[i][0] == perso:
                  infoPerso[i][9] = alliances

            if infoPerso[i][0] == perso2:
                  infoPerso[i][9] = alliances

            if infoPerso[i][0] == perso3 and cbPerso == 3:
                  infoPerso[i][9] = alliances

      alliances += 100

print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\33[4m\33[97m\33[1mBAIN DE SANG :\n\33[0m")

while days == 0:
      randomChoice()
      if P1 != P2 or len(personnages) == 1:
            time.sleep(0.01)
            if repartition <= rep and actionCombatCornucopia[rngActionCombatCornucopia] != stockActionsCombatCornucopia[-1] and len(personnages) > 1:
                  print(f"\33[91m\33[1m {P1[2:]}\33[0m {actionCombatCornucopia[rngActionCombatCornucopia]}\33[1m\33[97m {P2[2:]}\33[0m {actionCombatCornucopia2ePart[rngActionCombatCornucopia]}")
                  stockActionsCombatCornucopia.append(actionCombatCornucopia[rngActionCombatCornucopia])
                  ajoutePersoArme(P2)
                  ajouteNbrStatus(1, 1, P2)
                  persoCornBag.append(P2)
                  supprimePersoBlesse(P1)
                  personnages.remove(P1), personnages.remove(P2)
                  personnagesMorts.append(P1), personnagesJoues.append(P2)
                  
            elif repartition > rep and repartition <= rep1 and actionKillCornucopia[rngActionKillCornucopia] != stockActionsKillCornucopia[-1] and len(personnages) > 1:
                  print(f"\33[1m\33[97m {P1[2:]}\33[0m {actionKillCornucopia[rngActionKillCornucopia]}\33[1m\33[91m {P2[2:]}\33[0m {actionKillCornucopia2ePart[rngActionKillCornucopia]}")
                  stockActionsKillCornucopia.append(actionKillCornucopia[rngActionKillCornucopia])
                  ajoutePersoArme(P1)
                  ajouteNbrStatus(1, 1, P1)
                  persoCornBag.append(P1)
                  supprimePersoBlesse(P2)
                  personnages.remove(P1), personnages.remove(P2)
                  personnagesMorts.append(P2), personnagesJoues.append(P1)

            elif repartition > rep1 and repartition <= rep2 and actionBlesseCornucopia[rngActionBlesseCornucopia] != stockActionsBlesseCornucopia[-1] and len(personnages) > 1:
                  if repartitionKill < 50:
                        print(f"\33[1m\33[97m {P1[2:]}\33[0m {actionBlesseCornucopia[rngActionBlesseCornucopia]}\33[1m\33[93m {P2[2:]}\33[0m {actionBlesseCornucopia2ePart[rngActionBlesseCornucopia]}")
                        stockActionsBlesseCornucopia.append(actionBlesseCornucopia[rngActionBlesseCornucopia])
                  elif actionBlesseCornucopiaSAC[rngActionBlesseCornucopiaSAC] != stockActionsBlesseCornucopiaSAC[-1]:
                        print(f"\33[1m\33[97m {P1[2:]}\33[0m {actionBlesseCornucopiaSAC[rngActionBlesseCornucopiaSAC]}\33[1m\33[93m {P2[2:]}\33[0m {actionBlesseCornucopiaSAC2ePart[rngActionBlesseCornucopiaSAC]}")
                        stockActionsBlesseCornucopiaSAC.append(actionBlesseCornucopiaSAC[rngActionBlesseCornucopiaSAC])
                        persoCornBag.append(P1)
                  persoBlesse.append(P2)
                  ajouteStatusPerso(7, True, P2)
                  ajouteNbrStatus(4, 4, P2)
                  ajoutePersoArme(P1)
                  personnages.remove(P1), personnages.remove(P2)
                  personnagesJoues.append(P1), personnagesJoues.append(P2)


            elif repartition > rep2 and repartition < rep3 and actionFuiteCornucopia[rngActionFuiteCornucopia] != stockActionsFuiteCornucopia[-1]:
                  if repartitionKill < 50:
                        print(f"\33[1m\33[97m {P1[2:]}\33[0m {actionFuiteCornucopia[rngActionFuiteCornucopia]}")
                        stockActionsFuiteCornucopia.append(actionFuiteCornucopia[rngActionFuiteCornucopia])
                  elif actionFuiteCornucopiaSAC[rngActionFuiteCornucopiaSAC] != stockActionsFuiteCornucopiaSAC[-1]:
                        print(f"\33[1m\33[97m {P1[2:]}\33[0m {actionFuiteCornucopiaSAC[rngActionFuiteCornucopiaSAC]}")
                        stockActionsFuiteCornucopiaSAC.append(actionFuiteCornucopiaSAC[rngActionFuiteCornucopiaSAC])
                        persoCornBag.append(P1)
                  personnages.remove(P1), personnagesJoues.append(P1)

            elif repartition >= rep3:
                  print(f"\33[1m\33[91m {P1[2:]}\33[0m {actionFuiteCornucopiaMort[rngActionFuiteCornucopiaMort]}")
                  supprimePersoBlesse(P1)
                  personnages.remove(P1), personnagesMorts.append(P1)
      else:
            randomChoice()

      if len(personnages) == 0: 
            days += 1

time.sleep(1)
print(f"\n\n\n\n\33[4m\33[97m\33[1mDAY {days} :\n\33[0m")

#Réinitialisation de la liste des personnages dans l'ordre
for perso in personnagesJoues:
      personnages.append(perso)
personnages.sort()
for perso in range(len(personnagesJoues)):
      del personnagesJoues[0]

#Pourcentages reste de la partie
rep = 6
rep1 = 15
rep2 = 40
rep3 = 45
rep4 = 94

UnPersoRestant = False

while len(personnagesMorts) < nbrPerso: 
      randomChoice()
      checkSameActions()

      #Meurt naturelle a cause des bléssures
      for x in range(len(infoPerso)):
            if infoPerso[x][0] == P1 and infoPerso[x][4] == 1 and days <= 4 and len(personnages) != 1 and repartition <= 70:
                  while stockActionsMortBlessure[-1] == actionsMortBlessure[rngActionMortBlessure]:
                        rngActionMortBlessure = randint(0, len(actionsMortBlessure) - 1)
                  print(f"\33[1m\33[91m {P1[2:]}\33[0m {actionsMortBlessure[rngActionMortBlessure]}")
                  stockActionsMortBlessure.append(actionsMortBlessure[rngActionMortBlessure])
                  if len(personnagesMorts) == nbrPerso:
                        persoGagne = True

                  kills += 1
                  personnagesMorts.append(P1), personnages.remove(P1), supprimePersoBlesse(P1)
                  if len(personnages) > 0:
                        randomChoice()
                  
      #Si il ne reste qu'un personnage a jouer
      if len(personnages) == 1:
                  rep = -1
                  rep1 = -1
                  rep2 = -1
                  rep3 = 0
                  rep4 = 90
                  UnPersoRestant = True

      #Plus de chances de faire alliance si P1 et P2 sont dans le même district
      if P1[0] == P2[0] and len(personnages) > 3:
            repAlly = 55
            repAlly3P = 15

      #Si les personnages choisi sont éligibles
      if len(personnages) != 0 and P1 != P2 and P2 != P3 and persoGagne == False or UnPersoRestant == True and persoGagne == False and len(personnages) != 0:

            if P1 in persoArme and UnPersoRestant == False:
                  rep = 7
                  rep1 = 19
                  rep2 = 41
                  rep3 = 44
                  rep4 = 93

            if len(personnagesMorts) < (nbrPerso - 4) and UnPersoRestant == False:
                  rep = 7
                  rep1 = 35
                  rep2 = 50
                  rep3 = 54
                  rep4 = 95

            if len(personnagesMorts) == (nbrPerso-1) and UnPersoRestant == False:
                  rep = -1
                  rep1 = 95
                  rep2 = 95
                  rep3 = 100
                  rep4 = -1

            if len(personnagesMorts) < (nbrPerso - 2) and UnPersoRestant == False:
                  progressionJoursRepartition()

            if P2 in persoBlesse:
                  persoDejaBlesse = True

            killForSponsor()

            #Si il n'y a pas de kill alors plus de chances de faire des kills
            if kills == 0 and len(personnages) >= 3 or kills == 0 and days >= 5 and len(personnages) >= 3 or kills <= 1 and len(personnages) >= 4:
                  rep = 10
                  rep1 = 60
                  rep2 = 75
                  rep3 = 80
                  rep4 = 97
            
            if kills == 0 and len(personnages) == 2 and len(personnagesMorts) < 21:
                  rep = -1
                  rep1 = 65
                  rep2 = 70
                  rep3 = 75
                  rep4 = 98 

            #print(rep, rep1, rep2, rep3, rep4)

            #Action kill avec 3 personnages
            for x in range(len(infoPerso)):
                  if infoPerso[x][0] == P1:
                        P1Team = infoPerso[x][9]
                  if infoPerso[x][0] == P2:
                        P2Team = infoPerso[x][9]
                  
            if P1[0] == P2[0] and len(personnages) > 3 and P1 != P3 or repartition <= rep and len(personnages) >= 3 and P1 != P3 or P1Team == P2Team and len(personnages) >= 3 and P1 != P3:
                  UnVsDeux = randint(0, 100) 

                  #Plus de chances de faire un double kill si P3 est armée et en fonction de ses kills
                  for x in range(len(infoPerso)):
                        if infoPerso[x][0] == P3 and infoPerso[x][8] == True:
                              UnVsDeux = randint(0, 100-15*infoPerso[x][1])

                  if UnVsDeux <= 30: #1vs2
                        print(f"\33[1m\33[97m {P3[2:]}\33[0m {actionsKill3Perso1vs2[rngActionsKill3Perso1vs2]}\33[91m\33[1m {P1[2:]}\33[0m et \33[91m\33[1m{P2[2:]}\33[0m")
                        stockActionsKill3Perso1vs2.append(actionsKill3Perso1vs2[rngActionsKill3Perso1vs2])
                        
                        ajouteNbrStatus(2, 1, P3)
                        kills += 2
                        if randint(0, 100) < 60:
                              ajoutePersoArme(P3)

                        supprimePersoBlesse(P1), supprimePersoBlesse(P2)
                        personnagesMorts.append(P1), personnagesMorts.append(P2), personnagesJoues.append(P3)
                        personnages.remove(P1), personnages.remove(P2), personnages.remove(P3)

                  else: #2vs1
                        print(f"\33[1m\33[97m {P1[2:]}\33[0m et \33[1m\33[97m{P2[2:]}\33[0m {actionsKill3Perso[rngActionsKill3Perso]} \33[91m\33[1m{P3[2:]}\33[0m")
                        stockActionsKill3Perso.append(actionsKill3Perso[rngActionsKill3Perso])
                        
                        ajouteNbrStatus(1, 1, P1), ajouteNbrStatus(1, 1, P2)
                        kills += 2
                        if randint(0, 100) < 35:
                              ajoutePersoArme(P1)
                        if randint(0, 100) < 25:
                              ajoutePersoArme(P2)

                        supprimePersoBlesse(P3)
                        personnagesJoues.append(P1), personnagesJoues.append(P2), personnagesMorts.append(P3)
                        personnages.remove(P1), personnages.remove(P2), personnages.remove(P3)

            
            #Action kill entre 2 personnages
            elif repartition > rep and repartition <= rep1 and P1 != P2 and len(personnages) >= 2:
                  if repartitionKill <= 50:
                        killBlesse()
                        print(f"\33[1m\33[97m {P1[2:]}\33[0m {actionsKill[rngActionsKill]} \33[1m\33[91m{P2[2:]}\33[0m {actionsKill2ePart[rngActionsKill]}")
                        stockActionsKill.append(actionsKill[rngActionsKill])
                        
                        ajouteNbrStatus(1, 1, P1)
                        kills += 1

                        if randint(0, 100) < 35:
                              ajoutePersoArme(P1)

                        supprimePersoBlesse(P2)
                        personnagesJoues.append(P1), personnagesMorts.append(P2)
                        personnages.remove(P1), personnages.remove(P2)
                  else:
                        killBlesse()
                        print(f"\33[1m\33[91m {P2[2:]}\33[0m {actionsKillInverse[rngActionsKillInverse]} \33[1m\33[97m{P1[2:]}\33[0m {actionsKillInverse2ePart[rngActionsKillInverse]}")
                        stockActionsKillInverse.append(actionsKillInverse[rngActionsKillInverse])

                        ajouteNbrStatus(1, 1, P1)
                        kills += 1

                        if randint(0, 100) < 35:
                              ajoutePersoArme(P1)

                        supprimePersoBlesse(P2)
                        personnagesJoues.append(P1), personnagesMorts.append(P2)
                        personnages.remove(P1), personnages.remove(P2)


            #Action personnage blesse un autre      
            elif repartition > rep1 and repartition < rep2 and actionsBlesse[rngActionsBlesse] != stockActionsBlesse[-1] and len(personnages) > 2 and persoDejaBlesse == False:
                  print(f"\33[1m\33[97m {P1[2:]}\33[0m {actionsBlesse[rngActionsBlesse]} \33[1m\33[93m{P2[2:]}\33[0m {actionsBlesse2ePart[rngActionsBlesse]}")
                  stockActionsBlesse.append(actionsBlesse[rngActionsBlesse])

                  persoBlesse.append(P2)
                  ajouteStatusPerso(7, True, P2)
                  ajouteNbrStatus(4, 4, P2)

                  if randint(0, 100) < 35:
                        ajoutePersoArme(P1)

                  personnages.remove(P1), personnages.remove(P2)
                  personnagesJoues.append(P1), personnagesJoues.append(P2)
                  nbrPersoBlesse += 1


            #Action Mort naturelle
            elif repartition >= rep2 and repartition <= rep3 and actionsMortNaturelle[rngActionMortNaturelle] != stockActionsMortNaturelle[-1] and len(personnages) >= 2:
                  print(f"\33[1m\33[91m {P1[2:]}\33[0m {actionsMortNaturelle[rngActionMortNaturelle]}")
                  stockActionsMortNaturelle.append(actionsMortNaturelle[rngActionMortNaturelle])

                  kills += 1
                  personnages.remove(P1)
                  supprimePersoBlesse(P1)
                  personnagesMorts.append(P1)


            #Alliances & Actions inutiles/faim/soif..
            elif repartition >= rep3 and repartition <= rep4 and actions[rngActions] != stockActions[-1] or UnPersoRestant == True and actions[rngActions] != stockActions[-1] and repartition >= rep3 and repartition < rep4:
                  
                  if repartitionAlly <= repAlly and repartitionAlly > repAlly3P and len(personnages) >= 2 and days <= 5 and len(personnages) >= 4: #Alliances 2 Personnages
                        
                        while actionsAlliances2Perso[rngActionAlliance2Perso] == stockActionsAlliances2Perso[-1] or P1 == P2:
                              randomChoice()
                        print(f"\33[1m\33[94m {P1[2:]}\33[0m {actionsAlliances2Perso[rngActionAlliance2Perso]} \33[1m\33[94m{P2[2:]}\33[0m {actionsAlliances2Perso2ePart[rngActionAlliance2Perso]}")
                        stockActionsAlliances2Perso.append(actionsAlliances2Perso[rngActionAlliance2Perso])
                        
                        addAlliance(P1, P2, P3, 2)
                        personnages.remove(P1), personnages.remove(P2)
                        personnagesJoues.append(P1), personnagesJoues.append(P2)

                  elif repartitionAlly <= repAlly3P and len(personnages) >= 3 and days <= 5 and len(personnages) >= 6: #Alliances 3 Personnages
                        
                        while actionsAlliances3Perso[rngActionAlliance3Perso] == stockActionsAlliances3Perso[-1] or P1 == P2 or P2 == P3 or P1 == P3:
                              randomChoice()
                        print(f"\33[1m\33[94m {P1[2:]}\33[0m{actionsAlliances3Perso1erPart[rngActionAlliance3Perso]}\33[1m\33[94m{P2[2:]}\33[0m {actionsAlliances3Perso[rngActionAlliance3Perso]} \33[94m\33[1m{P3[2:]}\33[0m {actionsAlliances3Perso2ePart[rngActionAlliance3Perso]}")
                        stockActionsAlliances3Perso.append(actionsAlliances3Perso[rngActionAlliance3Perso])
                        
                        addAlliance(P1, P2, P3, 3)
                        personnages.remove(P1), personnages.remove(P2), personnages.remove(P3)
                        personnagesJoues.append(P1), personnagesJoues.append(P2), personnagesJoues.append(P3)
                  
                  elif P1 in persoBlesse: #Actions jouées pas les blessés
                        if P1 in persoCornBag:
                              while actionsPersosBlessesSAC[rngActionsPersosBlessesSAC] == stockActionsPersosBlessesSAC[-1]:
                                    rngActionsPersosBlessesSAC = randint(0, len(actionsPersosBlessesSAC) - 1)
                                    print("while PB 1")
                              print(f"\33[1m\33[93m {P1[2:]}\33[0m {actionsPersosBlessesSAC[rngActionsPersosBlessesSAC]}")
                              stockActionsPersosBlessesSAC.append(actionsPersosBlessesSAC[rngActionsPersosBlessesSAC])
                        else:
                              while actionsPersosBlesses[rngActionsPersosBlesses] == stockActionsPersosBlesses[-1]:
                                    rngActionsPersosBlesses = randint(0, len(actionsPersosBlesses) - 1)
                                    print("while PB 2")
                              print(f"\33[1m\33[93m {P1[2:]}\33[0m {actionsPersosBlesses[rngActionsPersosBlesses]}")
                              stockActionsPersosBlesses.append(actionsPersosBlesses[rngActionsPersosBlesses])
                        personnages.remove(P1)
                        personnagesJoues.append(P1)

                  else: #Actions faim/soif.....
                        for x in range(len(infoPerso)):
                              if infoPerso[x][0] == P1:
                                    while days <= 2 and actions[rngActions] == actions[0] or days <= 2 and actions[rngActions] == actions[1] or days == 1 and actions[rngActions] == actions[2] or days == 1 and actions[rngActions] == actions[3]:
                                          randomChoice()

                        print(f"\33[1m\33[97m {P1[2:]}\33[0m {actions[rngActions]}")
                        stockActions.append(actions[rngActions])
                  
                        if actions[rngActions] == actions[0] or actions[rngActions] == actions[1]:
                              ajouteStatusPerso(5, True, P1)
                              ajouteNbrStatus(3, 2, P1)
                        if actions[rngActions] == actions[2] or actions[rngActions] == actions[3]:
                             ajouteStatusPerso(6, True, P1)
                             ajouteNbrStatus(3, 3, P1) 

                        if actions[rngActions] == actions[5]:
                              ajouteStatusPerso(5, False, P1)
                        if actions[rngActions] == actions[4]:
                              ajouteStatusPerso(6, False, P1)

                        personnages.remove(P1)
                        personnagesJoues.append(P1)


            #Action Sponsor
            elif repartition >= rep4 and actionSponsor[rngSponsor] != stockSponsor[-1] or UnPersoRestant == True and repartition >= rep4 and actionSponsor[rngSponsor] != stockSponsor[len(stockSponsor)-1]:
                  while P1 in persoArme and actionSponsor[rngSponsor] == actionSponsor[2] or P1 not in persoBlesse and actionSponsor[rngSponsor] == actionSponsor[3]:
                        randomChoice()

                  #Si personnage blessé => Plus de chances de recevoir du soin
                  repSoin = 35
                  if P1 in persoBlesse:
                        for i in range(len(infoPerso)):
                              if infoPerso[i][0] == P1:
                                    if infoPerso[i][1] > 0:
                                          repSoin += infoPerso[i][1]*5
                                    if repartitionRecoiSoin <= repSoin:
                                          rngSponsor = 3
                                    if actionSponsor[rngSponsor] == actionSponsor[3]:
                                          infoPerso[i][4] = 0

                  for i in range(len(infoPerso)):
                        if infoPerso[i][0] == P1:
                              if infoPerso[i][2] == 1:
                                    rngSponsor = 0
                              if infoPerso[i][3] == 1:
                                    rngSponsor = 1
                              if infoPerso[i][8] == True:
                                    rngSponsor = 2


                  print(f"\33[1m\33[97m {P1[2:]}\33[0m {actionSponsor[rngSponsor]}")
                  stockSponsor.append(actionSponsor[rngSponsor])

                  if actionSponsor[rngSponsor] == actionSponsor[1]:
                        ajouteStatusPerso(5, False, P1)
                  if actionSponsor[rngSponsor] == actionSponsor[0]:
                        ajouteStatusPerso(6, False, P1)
                  if actionSponsor[rngSponsor] == actionSponsor[3]:
                        ajouteStatusPerso(7, False, P1)
                  if actionSponsor[rngSponsor] == actionSponsor[2]:
                        ajoutePersoArme(P1)

                  personnagesJoues.append(P1)
                  personnages.remove(P1)

            time.sleep(0.01)

      elif len(personnages) != 0:
            randomChoice()

      if len(personnagesMorts) == nbrPerso:
            for perso in personnagesJoues:
                  personnages.append(perso)
            for perso in range(len(personnagesJoues)):
                  del personnagesJoues[0]
            break #Sortie du while

      if len(personnages) == 0:
            time.sleep(1)

            kills = 0
            days = days + 1
            print(f"\n\n\n\33[4m\33[97m\33[1mDAY {days} :\n\33[0m")
           
            for perso in personnagesJoues:
                  personnages.append(perso)
            personnages.sort()
            for perso in range(len(personnagesJoues)):
                  del personnagesJoues[0]
            
            for x in range(len(infoPerso)):
                  if infoPerso[x][2] > 0:
                        infoPerso[x][2] -= 1
                  if infoPerso[x][3] > 0:
                        infoPerso[x][3] -= 1
                  if infoPerso[x][4] > 0:
                        infoPerso[x][4] -= 1

      if days >= 30:
            for perso in personnages:
                  personnagesMorts.append(perso)
                  personnages.remove(perso)
            print("Pas de chance")

      #Re-équilibrage de la repartition      
      rep = 6
      rep1 = 15
      rep2 = 40
      rep3 = 45
      rep4 = 94

      repAlly = 26
      repAlly3P = 9

      UnPersoRestant = False
      persoDejaBlesse = False

time.sleep(1)
print(f"\n\n\33[1m\33[97mBRAVO ! \33[92m{personnages[0][2:].upper()}\33[0m \33[1m\33[97mA GAGNÉ LES HUNGER GAMES !\n\n")

for perso in personnagesMorts:
      personnages.append(perso)
personnages.sort()

KillsPersoFinal = []
for perso in range(len(infoPerso)):
      KillsPersoFinal.append(infoPerso[perso][1 ])

time.sleep(0.5)
print("Calcul du score...\n")
time.sleep(1.5)

for i in range(len(personnages)):
      print(personnages[i][2: ],"\33[1m- \33[0m\33[91mKills :\33[0m\33[1m", KillsPersoFinal[i])
      time.sleep(0.1)