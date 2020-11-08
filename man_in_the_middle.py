------------------------------------------------------------------------

#

# @Auteurs : EV2 CHAVELLIER & EV2 LEBIGRE

#

# @Date : 06.11.20

# @Lieu : École Navale / Chaire de Cyberdéfense des systèmes navals

# @Cadre : Projet de Fin d'Études

# @Sujet : # Détection temps-réel d’anomalies cyber # sur un réseau NMEA par l’utilisation de # techniques d’apprentissage automatique.

#

#------------------------------------------------------------------------

# @Titre : Man in the Middle entre BridgeCommand et OpenCPN

#------------------------------------------------------------------------

# @Description : Ce script écoute sur le port de sortie de BridgeCommand via un socket, intercepte les trames et en modifie certaines à la volée.
# En parallèle, l'appel au script du module prediction permet de detecter via la méthode statistique si un leurrage a lieu  

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import pynmea2
import json
import random as rd # modules internes
import pickle as pk

import traitement as tr # modules externes
import prediction as pr

N=100 # pour l'évaluation des résultats du modele

#lecture tps reel des trames

def mim():


    print("loading the model...")

    infile = open("model.sauv", 'rb') # recupere le modele sauvegard dans le fichier objet model.sauv
    modele = pk.load(infile)
    infile.close()

    print("initialization...")

    UDP_IPrec = "127.0.0.1"
    UDP_IPenv = "127.0.0.1"
    UDP_PORTrec = 5005
    UDP_PORTenv = 10110

    sockrec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket pour recevoir les données issues de BridgeCommand
    sockenv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket pour renvoyer les trames vers OpenCPN
    sockrec.bind((UDP_IPrec, UDP_PORTrec))

    l_phi,l_g,l_t,l_v,l_trame=[],[],[],[],[]
    cap_test=[0,0]
    l_faux_positif=[] # prediction=true et leurrage=false
    l_faux_negatif=[] # prediction=false et leurrage=false
    l_vrai_positif=[] # prediction=true et leurrage = true
    l_vrai_negatif=[] # prediction=false et leurrage=true
    i=0
    nb_leurrage=0

    while i<N:
        data = sockrec.recvfrom(1024)  # buffer size is 1024 bytes
        data = data[0].decode("utf-8")
        message = pynmea2.parse(data)

        flag_leurrage=False

        if (message.sentence_type == "RMC"):

            i += 1  # compte le nombre de trames

            alea = 0#rd.randint(0, 3)
            if (alea == 1):  # modifie aléatoirement des trames, 33% de trames fausses
                offset_lat=0.00050 + 0.0045 # 10'  de lat
                offset_lon=0.00050 + 0.0045 # 10'  de lon
                modif_lat = float(message.data[2]) + offset_lat #
                modif_lon = float(message.data[4]) + offset_lon
                message.data[2] = str(modif_lat)
                message.data[4] = str(modif_lon)
                print("jamming : offset_lon=",offset_lon,"offset_lat=",offset_lat)
                flag_leurrage = True
                nb_leurrage += 1

            trame=json.loads(tr.dissect(message))
            trame2={}

            l_t.append(float(trame["timestamp"]))

            trame2["timestamp"]=float(trame["timestamp"])

            if (trame["lat_dir"] == 'N'):
                phi_str=(trame["lat"])
                phi=float(phi_str[0:2])*60 + float(phi_str[2:]) # réalise des conversions en minutes d'angle
                l_phi.append(phi)
                trame2["phi"]=phi
            else:  # si Phi est négatif 
                phi_str = (trame["lat"])
                phi = -float(phi_str[0:2]) * 60 + float(phi_str[2:])  # en minutes de phi
                l_phi.append(phi)
                trame2["phi"] = phi

            if (trame["lon_dir"] == 'W'):
                g_str=(str(trame["lon"]))
                g=float(g_str[0:3]) * 60 + float(g_str[3:]) # réalise des conversions en minute de g
                l_g.append(g)
                trame2["g"] = g


            else:
                g=(-float(g_str[0:3]) * 60 + float(g_str[3:])) # si G est négatif
                l_g.append(g)
                trame2["g"] = g

            l_v.append(float(trame["spd_over_grnd"]))
            trame2["speed"] = float(trame["spd_over_grnd"])
            l_trame.append(trame2)

            if i>=3: # il faut au moins 3 trames 
                l_trame=l_trame[-3:]

                l_phi=[l_trame[0]["phi"],l_trame[1]["phi"],l_trame[2]["phi"]]
                l_g=[l_trame[0]["g"],l_trame[1]["g"],l_trame[2]["g"]]                              # conserve les deux dernières valeurs de phi et g
                l_t=[l_trame[0]["timestamp"],l_trame[1]["timestamp"],l_trame[2]["timestamp"]]# conserve les 3 dernières valeurs connues de temps
                l_v=[l_trame[0]["speed"],l_trame[1]["speed"],l_trame[2]["speed"]] # conserve les 3 dernières valeurs connues de vitesse
 
                cap=tr.cap(l_phi,l_g) # en minutes
                cap_test.append(cap[-1])
                cap_test.append(cap[-2])
                cap_test=cap_test[-2:]

                test = [l_phi, l_g, l_t, l_v, cap_test]

                leurrage = pr.prediction(test, modele)
                print("leurrage : ", leurrage)
                if flag_leurrage:
                    l_trame.pop()  # on retire la trame leurrée

                if (leurrage and flag_leurrage):
                    l_vrai_positif.append(1)


                elif (leurrage and not flag_leurrage):

                    l_faux_positif.append(1)

                elif (not leurrage and flag_leurrage):

                    l_vrai_negatif.append(1)

                else:

                    l_faux_negatif.append(1)

        data = bytes(str(message), 'utf-8')
        sockenv.sendto(data, (UDP_IPenv, UDP_PORTenv))

    faux_positif = len(l_faux_positif)
    faux_negatif = len(l_faux_negatif)
    vrai_positif = len(l_vrai_positif)
    vrai_negatif = len(l_vrai_negatif)

    print("faux_negatif:",faux_negatif)
    print("faux_positif:",faux_positif)
    print("vrai_negatif:",vrai_negatif)  # on réalise les estimations sur 100 trames RMC
    print("vrai_positif:",vrai_positif)
    print(nb_leurrage)
