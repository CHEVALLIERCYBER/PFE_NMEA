#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import pynmea2
import json
import random as rd # modules internes
import pickle as pk

import traitement as tr # modules externes
import prediction as pr

N=100

#lecture tps reel des trames

def mim():


    print("loading the model...")

    infile = open("model.sauv", 'rb')
    modele = pk.load(infile)
    infile.close()

    print("initialization...")

    UDP_IPrec = "127.0.0.1"
    UDP_IPenv = "127.0.0.1"
    UDP_PORTrec = 5005
    UDP_PORTenv = 10110

    sockrec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockenv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
                offset_lat=0.00050 + 0.0045 # 10  de lat
                offset_lon=0.00050 + 0.0045 # 10  de lon
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
                phi=float(phi_str[0:2])*60 + float(phi_str[2:]) # en minutes d'angle
                l_phi.append(phi)
                trame2["phi"]=phi
            else:
                phi_str = (trame["lat"])
                phi = -float(phi_str[0:2]) * 60 + float(phi_str[2:])  # en minutes de phi
                l_phi.append(phi)
                trame2["phi"] = phi

            if (trame["lon_dir"] == 'W'):
                g_str=(str(trame["lon"]))
                g=float(g_str[0:3]) * 60 + float(g_str[3:]) # en minute de g
                l_g.append(g)
                trame2["g"] = g


            else:
                g=(-float(g_str[0:3]) * 60 + float(g_str[3:]))
                l_g.append(g)
                trame2["g"] = g

            l_v.append(float(trame["spd_over_grnd"]))
            trame2["speed"] = float(trame["spd_over_grnd"])
            l_trame.append(trame2)

            if i>=3:
                l_trame=l_trame[-3:]

                l_phi=[l_trame[0]["phi"],l_trame[1]["phi"],l_trame[2]["phi"]]
                l_g=[l_trame[0]["g"],l_trame[1]["g"],l_trame[2]["g"]]                              # conserve les deux dernières valeurs de phi et g
                l_t=[l_trame[0]["timestamp"],l_trame[1]["timestamp"],l_trame[2]["timestamp"]]
                l_v=[l_trame[0]["speed"],l_trame[1]["speed"],l_trame[2]["speed"]]

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
    print("vrai_negatif:",vrai_negatif)  # on réalise les estimations sur 100 captures
    print("vrai_positif:",vrai_positif)
    print(nb_leurrage)
