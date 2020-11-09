#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 11:37:12 2020

@author: guillaum
"""

import pickle as pk

import entrainement as ent
import modele as md
import prediction as pr
import traitement as tr
import man_in_the_middle as mim

################### TEST STATIQUE ####################
# on teste le modele sur une capture existante

#test=open("/home/guillaume/PFE/DATA/RMC/test_RMC.json") # capture de trames RMC uniquement

test=open("/home/guillaume/PFE/DATA/RMC/test_RMC_jamming.json")

test = tr.load(test)

#dict=md.modele()
#modele=ent.entrainement(dict) # calcule les valeurs de µ et sigma pour les différentes valeurs de vitesse et cap et cree un fichier modele.sauv

modele_sauv=open("/home/guillaume/PFE/pythonProject/model.sauv","rb")

modele=pk.load(modele_sauv)

resultat_prediction=pr.prediction(test,modele) 

print(resultat_prediction) # retourne une liste de booleens en fonction d'un leurrage detecté ou non

############### TEST DYNAMIQUE #####################
# on test le modele en temps reel

#mim.mim()
