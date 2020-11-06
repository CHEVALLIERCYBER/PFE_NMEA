#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import pynmea2
import random

def mid():

    UDP_IPrec = "127.0.0.1"
    UDP_IPenv = "127.0.0.1"
    UDP_PORTrec = 5005
    UDP_PORTenv = 5006

    sockrec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockenv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockrec.bind((UDP_IPrec, UDP_PORTrec))
    i = 0

    #test_spoofing = open("/home/guillaume/PFE/DATA/RMC/test_RMC_hacked.json")

    while 1:
        data = sockrec.recvfrom(1024)  # buffer size is 1024 bytes
        data = data[0].decode("utf-8")
        # print(data)
        message = pynmea2.parse(data)

        alea = random.randint(0, 10)

        if message.sentence_type == "RMC" and alea == 1:  # modifie aléatoirement des trames, 10% de trames fausses
            print()
            print("message : ", str(message))
            modif_lat = float(message.data[2]) + (1. / 100) * (2 * (random.random() - 0.5))  # rajoute un offset aléatoire entre -10 et 10 yards de latitude
            modif_lon= float(message.data[4]) + (1. / 100) * (2 * (random.random() - 0.5)) # offset en longitude
            message.data[2] = str(modif_lat)
            message.data[4] = str(modif_lon)
            print("jamming : ", str(message))
            print()
        elif message.sentence_type == "RMC":
            print("message", message)

        else:
            pass
        data = bytes(str(message), 'utf-8')
        sockenv.sendto(data, (UDP_IPenv, UDP_PORTenv))


mid()