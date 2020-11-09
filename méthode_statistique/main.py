#------------------------------------------------------------------------

#

# @Auteurs : EV2 CHEVALLIER 

#

# @Date : 06.11.20

# @Lieu : École Navale / Chaire de Cyberdéfense des systèmes navals

# @Cadre : Projet de Fin d'Études

# @Sujet : # Détection temps-réel d’anomalies cyber # sur un réseau NMEA par l’utilisation de # techniques d’apprentissage automatique.

#

#------------------------------------------------------------------------

# @Titre : Main

#------------------------------------------------------------------------

# @Description : # Ce programme execute les différentes scripts necessaires au fonctionnement de l'algorithme et réalise un calcule de score.
# Ces test ont lieu sur un fichier statique et en temps réél

#------------------------------------------------------------------------

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle as pk

import entrainement as ent
import modele as md
import prediction as pr
import prediction2 as pr2
import traitement as tr
import man_in_the_middle as mim

################### TEST STATIQUE ####################
# on teste les modeles sur une capture existante


test=open("/home/guillaume/PFE/DATA/RMC/test_RMC_jamming.json")

test = tr.load(test)

modele_sauv=open("/home/guillaume/PFE/pythonProject/model.sauv","rb")

modele=pk.load(modele_sauv)

resultat_prediction=pr.prediction(test,modele) 
resultat_prediction2=pr2.prediction(test,modele) 


print(resultat_prediction) # retourne une liste de booleens en fonction d'un leurrage detecté ou non

############### TEST DYNAMIQUE #####################
# on test le modele en temps reel

mim.mim()
