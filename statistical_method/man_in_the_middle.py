#------------------------------------------------------------------------
#
# @Auteurs : EV2 CHEVALLIER
#
# @Date : 06.11.20
# @Lieu : École Navale / Chaire de Cyberdéfense des systèmes navals
# @Cadre : Projet de Fin d'Études
# @Sujet : # Real time detection of cyber anomalies upon a NMEA network by using machine learning methods
#------------------------------------------------------------------------
# @Titre : Man in the Middle beetwen BridgeCommand and OpenCPN
#------------------------------------------------------------------------
# @Description : This script listen the output port of Bridge Command with a socket, intercept and alter some randomly chosen NMEA sentences.
# By the same time, the scripts prediction_v1 and prediction_v2 try to detect the modifications.
#------------------------------------------------------------------------

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import pynmea2
import json
import random as rd # internal modules
import pickle as pk

import traitement as tr # external modules
import prediction as pr

N=102 # evaluation of 100 sentences, the two first sentences are ignored

def mim():


    print("loading the model...")

    infile = open("model.sauv", 'rb') # use the model saved in the file model.sauv
    modele = pk.load(infile)
    infile.close()

    print("initialization...")

    UDP_IPrec = "127.0.0.1"
    UDP_IPenv = "127.0.0.1"
    UDP_PORTrec = 5005
    UDP_PORTenv = 10110

    sockrec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket to receive the sentences from Bridge Command 
    sockenv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket to send the sentences to Open CPN
    sockrec.bind((UDP_IPrec, UDP_PORTrec))

    l_phi,l_g,l_t,l_v,l_trame=[],[],[],[],[]
    cap_test=[0,0]
    l_faux_positif=[] # prediction=true and leurrage=false
    l_faux_negatif=[] # prediction=false and leurrage=false
    l_vrai_positif=[] # prediction=true and leurrage = true
    l_vrai_negatif=[] # prediction=false and leurrage=true
    i=0
    nb_leurrage=0

    while i<N:
        data = sockrec.recvfrom(1024)  # buffer size is 1024 bytes
        data = data[0].decode("utf-8")
        message = pynmea2.parse(data)

        flag_leurrage=False

        if (message.sentence_type == "RMC"):

            i += 1  # number of sentences

            
            alea = rd.randint(0, 10)
            
            if (alea == 1 ):  # alter randomly some sentences 
                offset_lat=0.05 # 10'  de lat
                offset_lon = 0.0
            elif (alea == 2):
                offset_lat = 0.0
                offset_lon=0.05 # 10'  de lon
            elif (alea == 3) :
                offset_lat = 0.05
                offset_lon = 0.05
                
            modif_lat = float(message.data[2]) + offset_lat 
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
                phi=float(phi_str[0:2])*60 + float(phi_str[2:]) # conversion in minutes
                l_phi.append(phi)
                trame2["phi"]=phi
            else:  # if phi is negative
                phi_str = (trame["lat"])
                phi = -float(phi_str[0:2]) * 60 + float(phi_str[2:])  # 
                l_phi.append(phi)
                trame2["phi"] = phi

            if (trame["lon_dir"] == 'W'):
                g_str=(str(trame["lon"]))
                g=float(g_str[0:3]) * 60 + float(g_str[3:]) 
                l_g.append(g)
                trame2["g"] = g


            else:
                g=(-float(g_str[0:3]) * 60 + float(g_str[3:])) # if G is negative
                l_g.append(g)
                trame2["g"] = g

            l_v.append(float(trame["spd_over_grnd"]))
            trame2["speed"] = float(trame["spd_over_grnd"])
            l_trame.append(trame2)

            if i>=3: 
                l_trame=l_trame[-3:]

                l_phi=[l_trame[0]["phi"],l_trame[1]["phi"],l_trame[2]["phi"]]
                l_g=[l_trame[0]["g"],l_trame[1]["g"],l_trame[2]["g"]]                              # keep the two last values of phi and G
                l_t=[l_trame[0]["timestamp"],l_trame[1]["timestamp"],l_trame[2]["timestamp"]]# keep the three last values of time
                l_v=[l_trame[0]["speed"],l_trame[1]["speed"],l_trame[2]["speed"]] # keep the three last values of speed
 
                cap=tr.cap(l_phi,l_g) 
                cap_test.append(cap[-1])
                cap_test.append(cap[-2])
                cap_test=cap_test[-2:]

                test = [l_phi, l_g, l_t, l_v, cap_test]

                leurrage = pr.prediction(test, modele)
                print("leurrage : ", leurrage)
                if flag_leurrage:
                    l_trame.pop()  # we get out the spoofed sentence

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
    print("vrai_negatif:",vrai_negatif)  # compute the estimation upon 100 sentences
    print("vrai_positif:",vrai_positif)
    print(nb_leurrage)
