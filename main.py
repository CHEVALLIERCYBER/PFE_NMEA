#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 11:37:12 2020

@author: guillaume
"""

import entrainement as ent
import modele as md
import prediction as pr
import traitement as tr
from sklearn import tree

#test=open("/home/guillaume/PFE/DATA/RMC/test_RMC.json") # capture de trames RMC uniquement
#test_jamming=open("/home/guillaume/PFE/GNSS_LOG/GPS/01_09_2020_jamming_gps_rmc.log.json")
test=open("/home/guillaume/PFE/DATA/RMC/test_RMC_jamming.json")
test = tr.load(test)

dict2=md.modele()
modele=ent.entrainement(dict2) # calcule les valeurs de µ et sigma pour les différentes valeurs de vitesse et cap

resultat_prediction=pr.prediction(test,modele)[0] #retourne une lisye de w,y,z



X=resultat_prediction[1]

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)

#l= float(len(detection_jamming))
#jamming= float(detection_jamming.count(True))

#print("brouillage détécté : ", 100*jamming/l, "%")

