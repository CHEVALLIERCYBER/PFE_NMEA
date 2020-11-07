#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 11:37:12 2020

@author: guillaum
"""

import entrainement as ent
import modele as md
import prediction as pr
import traitement as tr
import mim 
from sklearn import tree

################### TEST STATIQUE ####################
# on teste le modele sur une capture existante

#test=open("/home/guillaume/PFE/DATA/RMC/test_RMC.json") # capture de trames RMC uniquement

test=open("/home/guillaume/PFE/DATA/RMC/test_RMC_jamming.json")

test = tr.load(test)

dict=md.modele()
modele=ent.entrainement(dict) # calcule les valeurs de µ et sigma pour les différentes valeurs de vitesse et cap

resultat_prediction=pr.prediction(test,modele)[0] #retourne une lisye de w

############### TEST DYNAMIQUE #####################
# on test le modele en temps reel

mim.mim()

