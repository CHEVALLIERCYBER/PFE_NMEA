#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import pynmea2
import traitement as tr
import json
import prediction as pr
import pickle as pk
import numpy as np
import random as rd

N = 50000


# lecture tps reel des trames et entrainement

def mid():
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

    l_phi, l_g, l_t, l_dc, l_v = [], [], [], [], []

    X = []  # recupere les données w,y,z
    Y = []  # recupere 0 ou 1

    i = 0
    nb_leurrage = 0

    while i < N:
        data = sockrec.recvfrom(1024)  # buffer size is 1024 bytes
        data = data[0].decode("utf-8")
        message = pynmea2.parse(data)
        alea = rd.randint(0, 5)  #

        flag_leurrage = False

        if (message.sentence_type == "RMC"):

            i += 1  # compte le nombre de trames

            if (alea == 1):  # modifie aléatoirement des trames, 20% de trames fausses
                modif_lat = float(message.data[2]) + (1. / 50) * (
                            2 * (rd.random() - 0.5))  # rajoute un offset aléatoire entre -20 et 20 yards de latitude
                modif_lon = float(message.data[4]) + (1. / 50) * (2 * (rd.random() - 0.5))  # offset en longitude
                message.data[2] = str(modif_lat)
                message.data[4] = str(modif_lon)
                print("spoofing !!!")
                flag_leurrage = True
                Y.append(1)
                nb_leurrage += 1

            else:
                Y.append(0)
                trame = json.loads(tr.dissect(message))
                l_t.append(float(trame["timestamp"]))

                if (trame["lat_dir"] == 'N'):
                    phi_str = (trame["lat"])
                    phi = float(phi_str[0:2]) * 60 + float(phi_str[2:])  # en minutes d'angle
                    l_phi.append(phi)
                else:
                    phi_str = (trame["lat"])
                    phi = -float(phi_str[0:2]) * 60 + float(phi_str[2:])  # en minutes de phi
                    l_phi.append(phi)

                if (trame["lon_dir"] == 'W'):
                    g_str = (str(trame["lon"]))
                    g = float(g_str[0:3]) * 60 + float(g_str[3:])  # en minute de g
                    l_g.append(g)

                else:
                    g = (-float(g_str[0:3]) * 60 + float(g_str[3:]))
                    l_g.append(g)

                l_v.append(float(trame["spd_over_grnd"]))

            if i >= 3:
                l_phi = l_phi[-3:]
                l_g = l_g[-3:]  # conserve les deux dernières valeurs de phi et g
                l_t = l_t[-3:]

                cap = tr.cap(l_phi, l_g)  # en minutes

                if (len(cap) > 1):
                    t_test = l_t[-2:]
                    g_test = l_g[-2:]
                    phi_test = l_phi[-2:]
                    v_test = l_v[-2:]
                    cap_test = np.array(cap[-2:])
                    test = [phi_test, g_test, t_test, v_test, cap_test]

                    leurrage = pr.prediction(test, modele)[1]  # calcule les valeurs de w,y,z

                    X.append(leurrage)

                    print(leurrage)

    return [X, Y]


mid()

